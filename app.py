#!/usr/bin/env python

import indy_build_promote.rest as rest

from indy_build_promote.config import load_config_map
import os

DIR='/opt/data'
CFG = '/opt/config'

IN='repo.lst.IN'
OUT='repo.lst.OUT'
ERR='repo.lst.ERR'

# import time
# while True:
#     time.sleep(10)





if not os.path.exists(CFG):
    print(f"Cannot load configuration from: {CFG}")
    exit(-1)

cfg = load_config_map(CFG)

subs = sorted([d for d in os.listdir(DIR) if os.path.isdir(os.path.join(DIR, d)) and d.isdigit()])

next_dirname='1'
pending = []
if subs is None or len(subs) < 1:
    print(f"Cannot find previous pass at promotion. Downloading group definition for: {cfg.group} to get a list of members to start consolidating.")
    group = rest.get_group(cfg)
    for m in group['constituents']:
        if 'hosted' in m and 'build' in m:
            pending.append(m.split(':')[2])

else:
    last_dir = os.path.join(DIR, subs[-1])
    next_dirname = str(int(last_dir)+1)

    print(f"Merging pending and failed repos from last pass ({last_dir}) to generate the next list to start promoting")

    files = [os.path.join(last_dir, IN), os.path.join(last_dir, ERR)]
    for filename in files:
        with open(filename) as f:
            pending += [line.rstrip() for line in f.readlines() if len(line.rstrip()) > 0]

    if len(pending) < 1:
        print(f"Cannot find any repositories pending promotion in data directory: {last_dir}")
        exit(-2)


print(f"Got pending members:\n\n{pending}")
# curr_dir = os.path.join(DIR, next_dirname)
# os.makedirs(curr_dir)

# current_in = os.path.join(curr_dir, IN)
# print(f"Writing pending list to: {current_in}")
# with open(current_in 'w') as f:
#     o.write("\n".join(members))

