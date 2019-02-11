import time
from rest import (do_promote, update_group, get_group)
from build import (pop_build, get_pod)

REQUEST_TIMEOUT_BACKOFF = 10*60

def promote_build(build, group, config, pod, progress_file, fail_file):
    status = do_promote(build, config, fail_file)

    if status == 200 or status == 504:
        print(f"Updating group: {config.group} to remove {build} repository...")
        group['constituents'] = [c for c in group['constituents'] if c != build]
        success = update_group(group, config, progress_file, build)
        if success is False:
            print(f"Failed to update group: {config.group} after promotion of: {build}")
            exit(3)

        print(f"Promotion of {build} is complete.")

        if status == 504:
            print(f"Submitted promotion timed out. Waiting {REQUEST_TIMEOUT_BACKOFF} seconds for load to clear.")
            time.sleep(REQUEST_TIMEOUT_BACKOFF)
    else:
        print(f"Promotion failed for {build}")

def promote_builds(config, input_file, progress_file, fail_file):
    project = config.project
    groupname = config.group
    print(f"Retrieving Indy pod name in project: {project}")
    pod = get_pod(config)
    print(f"Project {project} Indy pod is: {pod}")

    print(f"Retrieving group definition for: {groupname}")
    group = get_group(config)
    if group is None:
        print("Promotion failed with missing group.")
        exit(2)

    target_key = f"maven:hosted:{config.target_repo}"
    if target_key not in group['constituents']:
        print(f"Group: {groupname} doesn't contain the consolidation target: {target_key}. Attempting to add it.")
        group['constituents'].insert(0, target_key)
        success = update_group(group, config, fail_file)
        if success is False:
            print(f"Failed to update group: {config.group} with target-repo: {target_key}")
            exit(3)

    build = pop_build(input_file, progress_file)
    while build is not None:
        print(f"Next build to promote is: {build}")
        promote_build(build, group, config, pod, progress_file)

        build = pop_build(input_file, progress_file)
