import subprocess
import fcntl

from config import SATIS_DIR

def build(repo):
    result = subprocess.run(f"""composer satis:build --repository-url={repo}""", cwd=SATIS_DIR, shell=True, text=True, capture_output=True)

    if result.returncode != 0:
        raise Exception(result.stderr)

def add_repo(repo):
    try:
        subprocess.run(f"""composer satis:add {repo}""", cwd=SATIS_DIR, shell=True, text=True, capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        output = (e.stdout or "") + (e.stderr or "")

        if "Repository url already added to the file" in output:
            return False

        raise RuntimeError(f"""composer satis:add failed{output}""")

def dispatch(repo):
    lockfile = "/tmp/satis.lock"

    with open(lockfile, "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)

        add_repo(repo)

        build(repo)

    return True
