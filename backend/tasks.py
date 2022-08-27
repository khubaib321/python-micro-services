import os

from invoke import task
from invoke.context import Context

DOCKERFILE_NAME = "Dockerfile"
COMPOSEFILE_NAME = "docker-compose.yml"

BACKEND_DIR = os.path.join(os.path.dirname(__file__))
ACCOUNTS_DIR = os.path.join(BACKEND_DIR, "apps", "accounts")


def run_commands(c: Context, cmds):
    if cmds and not type(cmds) in [list]:
        cmds = [cmds]

    for cmd in cmds:
        print("CMD => %s" % cmd)
        c.run(cmd, pty=True)


def create_venv(c: Context, build):
    if build:
        run_commands(c, "rm -rf .venv")
        run_commands(c, "python3 -m venv .venv")

    run_commands(c, "source .venv/bin/activate")

    reqs_path = os.path.join(ACCOUNTS_DIR, "requirements.txt")
    install_cmd = f"pip3 install -r {reqs_path}"

    run_commands(c, install_cmd)


def get_run_commands(base_cmd, detach, build):
    commands = []

    down_cmd = base_cmd + " down --remove-orphans"
    commands.append(down_cmd)

    if build:
        build_cmd = base_cmd + " build"
        commands.append(build_cmd)

    up_cmd = base_cmd + " up"

    if detach:
        up_cmd += " --detach"

    commands.append(up_cmd)

    return commands


def run_accounts(c: Context, detach, build):
    run_commands(c, f"cd {ACCOUNTS_DIR}")

    compose_file_path = os.path.join(ACCOUNTS_DIR, COMPOSEFILE_NAME)

    cmd = f"docker-compose -f {compose_file_path}"

    cmds = get_run_commands(cmd, detach, build)

    run_commands(c, cmds)


@task
def run(c: Context, accounts=False, build=False):
    create_venv(c, build)

    if accounts:
        print("Running accounts service...")
        run_accounts(c, detach=False, build=build)

    else:
        print("Running all services...")
        run_accounts(c, detach=True, build=build)

    print("Done!")
