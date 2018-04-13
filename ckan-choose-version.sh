#!/bin/bash

set -e

get_versions() {
    # Usage: VERSIONS=( $(get_versions) )

    # Get our official list of releases
    BUILDS_JSON=$(wget -q -O - https://raw.githubusercontent.com/KSP-CKAN/CKAN/master/Core/builds.json)

    # Get just the MAJOR.MINOR.PATCH strings, without trailing \r characters
    echo $BUILDS_JSON \
        | jq --raw-output '[.builds[] | sub("\\.[0-9]+$"; "")] | unique | reverse | .[]' \
        | dos2unix
}

versions_less_or_equal() {
    # Usage: versions_less_or_equal major1.minor1.patch1 major2.minor2.patch2
    # Returns: 0=true, 1=false, 2=error
    VER1=$1
    VER2=$2

    if [[ -z $VER1 || -z $VER2 ]]
    then
        # Null means unbounded, so always match
        return 0
    elif [[ $VER1 =~ ^([0-9]+)\.([0-9]+) ]]
    then
        MAJOR1=${BASH_REMATCH[1]}
        MINOR1=${BASH_REMATCH[2]}
        if [[ $VER2 =~ ^([0-9]+)\.([0-9]+) ]]
        then
            MAJOR2=${BASH_REMATCH[1]}
            MINOR2=${BASH_REMATCH[2]}
            if   (( $MAJOR1 < $MAJOR2 )); then return 0
            elif (( $MAJOR1 > $MAJOR2 )); then return 1
            elif (( $MINOR1 < $MINOR2 )); then return 0
            elif (( $MINOR1 > $MINOR2 )); then return 1
            else
                # First two numbers match, check for a third
                if [[ $VER1 =~ ^[0-9]+\.[0-9]+\.([0-9]+) ]]
                then
                    PATCH1=${BASH_REMATCH[1]}
                    if [[ $VER2 =~ ^[0-9]+\.[0-9]+\.([0-9]+) ]]
                    then
                        PATCH2=${BASH_REMATCH[1]}
                        if   (( $PATCH1 < $PATCH2 )); then return 0
                        elif (( $PATCH1 > $PATCH2 )); then return 1
                        else
                            # All are equal
                            return 0
                        fi
                    else
                        # No third digit, accept it
                        return 0
                    fi
                else
                    # No third digit, accept it
                    return 0
                fi
            fi
        else
            # Second version not valid
            return 2
        fi
    else
        # First version not valid
        return 2
    fi
}

matching_versions() {
    # ASSUMES: We have done VERSIONS=( $(get_versions) ) globally
    # Usage: matching_versions ksp_version_min ksp_version_max
    MIN=$1
    MAX=$2

    if [[ ( -z "$MIN" && -z "$MAX" ) || ( "$MIN" = any && "$MAX" = any ) ]]
    then
        echo "${VERSIONS[@]}"
    else
        declare -a MATCHES
        MATCHES=()
        for VER in "${VERSIONS[@]}"
        do
            if versions_less_or_equal "$MIN" "$VER" && versions_less_or_equal "$VER" "$MAX"
            then
                MATCHES+=($VER)
            fi
        done
        echo "${MATCHES[@]}"
    fi
}

ckan_matching_versions() {
    # Usage: ckan_matching_versions modname-version.ckan
    CKAN="$1"

    # Load the metadata
    JSON=$(cat "$CKAN")

    # Get min and max versions
    MIN=$(echo $JSON | jq --raw-output '.ksp_version // .ksp_version_min // ""')
    MAX=$(echo $JSON | jq --raw-output '.ksp_version // .ksp_version_max // ""')

    matching_versions "$MIN" "$MAX"
}

ckan_max_real_version() {
    # Usage: ckan_max_real_version modname-version.ckan
    CKAN="$1"

    VERS=( $(ckan_matching_versions "$CKAN") )
    echo "${VERS[0]}"
}

declare -a VERSIONS
VERSIONS=( $(get_versions) )

CKANS=(
    SmartTank/SmartTank-v0.1.2.ckan
    Astrogator/Astrogator-v0.7.8.ckan
    Kopernicus/Kopernicus-2-release-1.3.1-1.ckan
    CrowdSourcedFlags/CrowdSourcedFlags-1.55.5.ckan
    RFStockalike/RFStockalike-v2.0.4.ckan
    USITools/USITools-0.2.4.ckan
    TWR1/TWR1-1.31a.ckan
    WindowShineTR/WindowShineTR-v15.ckan
    USI-FTT/USI-FTT-0.4.3.0.ckan
    SVE-Sunflare/SVE-Sunflare-2-1.1.6.ckan
    surfacelights/surfacelights-1.6.ckan
    SolarSailNavigator/SolarSailNavigator-v1.0.9.ckan
)

for CK in "${CKANS[@]}"
do
    echo -n "$(basename $CK): "
    ckan_matching_versions "$CK"
done
