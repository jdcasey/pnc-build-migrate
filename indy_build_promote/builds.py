import os
import subprocess

def pop_build(input_file, progress_file):
    lines = []
    current = None
    with open(input_file) as f:
        lines = [line.rstrip() for line in f.readlines()]

    if len(lines) > 0:
        current = lines[0]

    with open(progress_file, 'a') as f:
        f.write(current + "\n")

    if len(lines) > 1:
        with open(input_file, 'w') as f:
            f.write("\n".join(lines[1:]))

    # print(f"Next build is: {current}")
    return current

def peek_build(input_file, index=0):
    lines = []
    current = None
    with open(INPUT_FILE) as f:
        lines = [line.rstrip() for line in f.readlines()]

    if len(lines) > index:
        current = lines[index]

    # print(f"Next build is: {current}")
    return current

def get_pod(config):
    project = config.project

    # print("Getting Indy pod info...")
    proc = subprocess.run(['oc', '-n', project, 'get', 'pods'], stdout=subprocess.PIPE)
    lines = [line for line in proc.stdout.decode('utf-8').splitlines()]
    pod = [line.split()[0] for line in lines if 'indy' in line and 'Running' in line and 'build' not in line and 'deploy' not in line][0]
    # print(f"Using Indy pod: {pod}")
    return pod

def list_files(build, config, pod):
    project = config.project
    command = f"oc -n {project} rsh {pod} find /opt/indy/var/lib/indy/storage/maven/hosted-{build} -type f"
    # print("Executing find command:")
    # print(command)
    output = subprocess.run(command.split(), stdout=subprocess.PIPE)
    files = output.stdout.decode('utf-8').splitlines()
    return files

def mark_failed(build, progress_file):
    with open(f"{progress_file}.FAILS", 'a') as f:
        f.write(build + "\n")

def list_builds(config, input_file, progress_file, repo_defs, build_listing_dir):
    project = config.project
    pod = get_pod(config)
    print(f"Project {project} Indy pod is: {pod}")

    build = pop_build(input_file, progress_file)
    while build is not None:
        print(f"Next build is: {build}")
        files = list_files(build, config, pod)
        if len(files) < 1:
            print(f"Build: {build} has no files. Skipping")
        else:
            print(f"Build: {build} has {len(files)} files")

            if not os.path.isdir(build_listing_dir):
                os.makedirs(build_listing_dir)
            
            with open(os.path.join(build_listing_dir, build + ".lst"), 'w') as f:
                f.write("\n".join(files))

            build_json = f"{build}.json"
            os.rename(os.path.join(repo_defs, build_json), os.path.join(build_listing_dir, build_json))

        build = pop_build(input_file, progress_file)
