import contextlib
import os
import subprocess
import sys
import venv


@contextlib.contextmanager
def activate_virtualenv(env_dir):
    os.environ['VIRTUAL_ENV'] = os.path.abspath(env_dir)
    os.environ['PATH'] = '{VIRTUAL_ENV}/bin:{PATH}'.format(**os.environ)

    if not os.path.isdir(os.environ['VIRTUAL_ENV']):
        create_virtualenv(env_dir)
        install_requirements(env_dir)

    yield


def create_virtualenv(env_dir):
    return venv.create(env_dir, with_pip=True)


def install_requirements(env_dir):
    env = os.environ.copy()
    proc = subprocess.run(
        ['pip', 'install', '-r', 'requirements.txt'],
        env=env)
    if proc.returncode:
        sys.exit(proc.returncode)


def run_in_virtualenv(argv, env_dir='venv'):
    with activate_virtualenv(env_dir):
        env = os.environ.copy()
        proc = subprocess.run(argv, env=env)
        sys.exit(proc.returncode)


@contextlib.contextmanager
def virtualenv(env_dir='venv'):

    if os.environ.get('VIRTUAL_ENV') is None:
        run_in_virtualenv(sys.argv)

    else:
        yield


@contextlib.contextmanager
def environment(env_file='environment.sh'):
    if os.path.exists(env_file):
        os.environ.update(dict(env_vars_from_file(env_file)))
    yield


def env_vars_from_file(env_file):
    with open(env_file) as f:
        for line in f.readlines():
            if '=' in line:
                key, val = parse_env_var(line)
                if key and val:
                    yield key, val


def parse_env_var(line):
    key, val = line.split('=', 1)
    key = key.strip()
    if key.startswith('export '):
        key = key[7:]
    val = val.strip()
    return key, val
