#!/usr/bin/jq -rMf

# List modules in order of the gap between their timestamps.
# May show misleading outliers due to recently-frozen modules
# and in-progress bot passes.

# Usage: wget -q -O - http://status.ksp-ckan.space/status/netkan.json | slow-modules.jq

(now - 3*60*60) as $cutoff
| to_entries
| map(select(.value.frozen != true)
    | {id:.key, dt:(.value.last_checked[0:19]+"Z"|fromdate)}
    | select(.dt >= $cutoff))
| sort_by(.dt)
| [range(1;length) as $i
   | .[$i-1] as $a
   | .[$i] as $b
   | {id:$a.id, dur:($b.dt - $a.dt)}]
| sort_by(-.dur)
