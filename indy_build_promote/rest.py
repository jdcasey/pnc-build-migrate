import requests
import json
from indy_build_promote.builds import mark_failed
from time import sleep

PROMOTE_TIMEOUT = 30*60 # 30 minutes, expressed in seconds
BACKOFF = 5*60

PROMOTE_THREADS = 'promotion:'
PROMOTE_LOAD = 'current-load'

def monitor_promote_readiness(config):
    while is_promotion_ready(config) is False:
        print(f"Promotion is not ready. Re-checking in {BACKOFF} seconds")
        sleep(BACKOFF)

    print("Indy is ready for more promotion requests")

def is_promotion_ready(config):
    retry=1
    while retry < 3:
        try:
            promote_load_threshold = int(config.promote_load_threshold)
            token = config.token
            base_url = config.url

            headers = {
                'Authorization': f"Bearer {token}",
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            url = f"{base_url}/healthcheck"

            print("Checking health of promote threadpool on Indy")
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"Invalid response from Indy healthcheck: {response.status_code}")

            data = response.json()
            pool = data.get(PROMOTE_THREADS)
            if pool is None:
                load = 0
            else:
                load = pool.get(PROMOTE_LOAD)

            if load is None:
                load = 0

            if load > promote_load_threshold:
                print(f"Current promotion load {load} is greater than back-off threshold: {promote_load_threshold}")
                return False

            print(f"Current promotion load {load} is within parameters.")
            return True
        except e:
            print(e)
        finally:
            retry+=1

def do_promote(build, config, fail_file):
    token = config.token
    base_url = config.url
    target_repo = config.target_repo

    req = {
        'source': f"maven:hosted:{build}",
        'target': f"maven:hosted:{target_repo}"
    }

    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    url = f"{base_url}/api/promotion/paths/promote"

    print(f"Running promotion of: {build} to: {target_repo}")
    response = requests.post(url, headers=headers, data=json.dumps(req), timeout=PROMOTE_TIMEOUT)
    status = response.status_code
    success = True
    if status != 200:
        print(f"Build {build} failed promotion with: {response.status_code}")
        success = False
    else:
        rjson = response.json()
        if rjson.get('error') is not None:
            print(f"Build {build} failed promotion with error: {rjson['error']}")
            success = False

    if success is False:
        mark_failed(build, fail_file)

    print("Promotion succeeded!")
    return status

def get_group(config):
    token = config.token
    base_url = config.url
    group = config.group

    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    url = f"{base_url}/api/admin/stores/maven/group/{group}"

    print(f"Retrieving group via URL:\n  {url}")
    response = requests.get(url, headers=headers, timeout=PROMOTE_TIMEOUT)
    status = response.status_code
    if status != 200:
        print(f"Failed to retrieve group: {group} with status: {response.status_code}")
        return None
    else:
        return response.json()

def save_group(config, out_file):
    token = config.token
    base_url = config.url
    groupname = config.group

    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    url = f"{base_url}/api/admin/stores/maven/group/{groupname}"

    response = requests.get(url, headers=headers)
    status = response.status_code
    if status != 200:
        print(f"Failed to retrieve group: {groupname} with: {status}")

    with open(out_file, 'w') as f:
        f.write(response.text)

def update_group(group, config, fail_file, build=None):
    token = config.token
    base_url = config.url
    groupname = config.group

    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    url = f"{base_url}/api/admin/stores/maven/group/{groupname}"

    response = requests.put(url, headers=headers, data=json.dumps(group), timeout=PROMOTE_TIMEOUT)
    status = response.status_code
    if status not in [200, 304]:
        if build is not None:
            print(f"Build {build} failed promotion with: {status}")
            mark_failed(build, fail_file)
        else:
            print(f"Failed to update group: {groupname} with: {status}")
        return False

    return True
