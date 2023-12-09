import os

from utils import set_output
from utils.repo import Release
from utils.tag import generate_readme


def handle_frp():
    cur_path = os.path.split(os.path.realpath(__file__))[0]
    frp = Release('fatedier/frp', r'[vV]\d+.\d+.\d+')
    # remove prefix 'v'
    updated = generate_readme(frp.version[1:], os.path.join(cur_path, 'frp', 'README.md'))
    if updated:
        print(f'frp will update to {frp.version[1:]}')
        frp.download_file(['linux_amd64'], os.path.join(cur_path, 'frp'), set_out=True)
        set_output('version', frp.version[1:])
        set_output('tag', '.'.join(frp.version[1:].split('.')[:2]))
    set_output('update', str(updated).lower())


if __name__ == '__main__':
    handle_frp()
