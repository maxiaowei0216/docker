import argparse
import os

from utils.repo import Release


def set_env(k, v):
    cmd = f'echo "{k}={v}" >> $GITHUB_ENV'
    print(f'Will run cmd: {cmd}')
    os.system(cmd)


def handle_frp():
    frp = Release('fatedier/frp', r'[vV]\d+.\d+.\d+')
    time = os.environ.get('time', '')
    time = int(time) if len(time) > 0 else 24
    if frp.is_need_update(time):
        frp.download_file(['linux_amd64'], os.path.join(os.getcwd(), 'frp'))
        set_env('frp_version', frp.version[1:])
        set_env('update', 'true')
    else:
        set_env('update', 'false')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repo', choices=['frp'], help='Choose which project to build')
    args = parser.parse_args()

    if args.repo == 'frp':
        handle_frp()
