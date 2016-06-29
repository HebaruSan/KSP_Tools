HebaruSan's KSP Tools
=====================
Command line utilities for automating common tasks related to [Kerbal Space Program](http://kerbalspaceprogram.com/).

The contents of this repository are released into the public domain.

ksp_save_dv
-----------
Parses a Kerbal Space Program save file and prints the delta V of each active craft. See code comments for known limitations.

ksp_engine_isps
---------------
Given the location of a Kerbal Space Program installation, parses the parts files and prints a table of the specific impulses of all stock engines in Perl format. Intended for updating `ksp_save_dv`.

ckan_abstract
-------------
Given a mod name, extracts the long form description of it from the [CKAN](http://forum.kerbalspaceprogram.com/index.php?/topic/90246-the-comprehensive-kerbal-archive-network-ckan-package-manager-v1180-19-june-2016/) `registry.json` file.

ckan_updates
------------
A simplistic text UI for CKAN based on the `dialog` utility. Only handles updates and installs.

deltav
------
Prints the delta V of a craft by applying the [Tsiolkovsky rocket equation](https://en.wikipedia.org/wiki/Tsiolkovsky_rocket_equation), given command line parameters:

1. Current mass in kilograms
2. Oxidizer in in-game units
3. LiquidFuel in in-game units
4. Specific impulse in seconds

dv-lvn-1.0
----------
Same as `deltav` above but ignores oxidizer. Parameters:

1. Current mass in kilograms
2. LiquidFuel in in-game units
3. Specific impulse in seconds
