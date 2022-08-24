import os

from invoke import task

DOCKERFILE_NAME = "Dockerfile"
COMPOSEFILE_NAME = "docker-compose.yml"

BASE_DIR = os.path.join(os.path.dirname(__file__))
ACCOUNTS_DIR = os.path.join(BASE_DIR, "apps/accounts")


def run_command(c, cmd):
    print("CMD => %s" % cmd)
    c.run(cmd, pty=True)


def run_accounts(c, detach=True, rebuild=False):
    run_command(c, f"cd {ACCOUNTS_DIR}")

    cmd = f"docker-compose -f {ACCOUNTS_DIR}/{COMPOSEFILE_NAME}"

    if rebuild:
        down_cmd = cmd + " down --remove-orphans"
        run_command(c, down_cmd)

    up_cmd = cmd + " up"

    if detach:
        up_cmd += " --detach"

    run_command(c, up_cmd)


@task
def run(c, all=False, accounts=False, rebuild=False):
    if all:
        print("Running all services...")
        run_accounts(c, rebuild=rebuild)

    elif accounts:
        print("Running accounts service...")
        run_accounts(c, rebuild=rebuild, detach=False)

    else:
        print("Nothing to run!")

    print("Done!")
