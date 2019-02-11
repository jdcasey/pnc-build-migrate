#!/usr/bin/env python

import indy_build_promote.rest as rest
from indy_build_promote.config import load_config_map
from indy_build_promote.promote import promote_builds
import os
import time
import traceback

DIR='/opt/data'
CFG = '/opt/config'

IN='repo.lst.IN'
OUT='repo.lst.OUT'
ERR='repo.lst.ERR'

try:
    while True:
        if not os.path.exists(CFG):
            print(f"Cannot load configuration from: {CFG}")
            exit(-1)

        cfg = load_config_map(CFG)

        subs = sorted([d for d in os.listdir(DIR) if os.path.isdir(os.path.join(DIR, d)) and d.isdigit()])

        next_dirname='0001'
        pending = []
        if subs is None or len(subs) < 1:
            print(f"Cannot find previous pass at promotion. Downloading group definition for: {cfg.group} to get a list of members to start consolidating.")
        else:
            last_dirname = subs[-1]
            last_dir = os.path.join(DIR, last_dirname)
            next_dirname = str(int(last_dirname)+1).zfill(4)

            print(f"Merging pending and failed repos from last pass ({last_dir}) to generate the next list to start promoting")

            files = [os.path.join(last_dir, IN), os.path.join(last_dir, ERR)]
            for filename in files:
                if os.path.exists(filename):
                    print(f"Reading pending promotions from: {filename}")
                    with open(filename) as f:
                        pending += [line.rstrip() for line in f.readlines() if len(line.rstrip()) > 0]

        if len(pending) < 1:
            print(f"Cannot find any repositories pending promotion...pulling group definition to look")

            group = rest.get_group(cfg)
            for m in group['constituents']:
                if 'hosted' in m and 'build' in m:
                    pending.append(m.split(':')[2])

        if len(pending) < 1:
            print("Still cannot find any repositories to promote. Sleeping 4 hours...")
            time.sleep(60*60*4)
        else:
            # print(f"Got pending members:\n\n{pending}")
            curr_dir = os.path.join(DIR, next_dirname)
            os.makedirs(curr_dir)

            current_in = os.path.join(curr_dir, IN)
            print(f"Writing pending list to: {current_in}")
            with open(current_in, 'w') as f:
                f.write("\n".join(members))

            promote_builds(cfg, IN, OUT, ERR)

except Exception:
    print(traceback.format_exc())
    while True:
        time.sleep(5)
