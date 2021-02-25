#!/usr/bin/python3

import os, sys, git, datetime, json, tempfile, subprocess, time
from typing import Dict, List, Tuple, Any

counts_file = "download_counts.json"
ckan_meta   = os.environ['HOME'] + "/Downloads/KSP/CKAN-meta"
plotter     = os.environ['HOME'] + "/Documents/src/ksp_tools/plot_counts.gnuplot"
repo        = git.Repo(ckan_meta)

def parse_line(line: str) -> Tuple[str, datetime.datetime]:
    fields = line.split(" ")
    return (fields[0], datetime.datetime.fromisoformat(fields[1]))

def git_hashes_and_timestamps(filename: str) -> List[Tuple[str, datetime.datetime]]:
    lines = repo.git.log('--', filename, format="%H %aI").split("\n")
    return list(map(parse_line, lines))[::-1]

def json_from_git(hash: str) -> Dict[str, Any]:
    return json.loads(repo.git.show("%s:%s" % (hash, counts_file)))

# Counts before 9/1/2018 don't include parent forks
first_day   = datetime.date(2018, 9, 1)
# SpaceDock was down this day or something
missing_day = datetime.date(2019, 5, 11)

identifiers = sys.argv[1:]
with tempfile.NamedTemporaryFile(mode='w') as tmpf:
    print("DateTime", *identifiers, file=tmpf)
    for vals in git_hashes_and_timestamps(counts_file):
        if vals[1].date() == missing_day or vals[1].date() < first_day:
            continue
        parsed = json_from_git(vals[0])
        if any(ident in parsed for ident in identifiers):
            print(vals[1].isoformat(), end=' ', file=tmpf)
            for identifier in identifiers:
                count = parsed.get(identifier, 0)
                print(count, end=' ', file=tmpf)
            print(file=tmpf)
    tmpf.flush()
    subprocess.run([plotter, tmpf.name])
