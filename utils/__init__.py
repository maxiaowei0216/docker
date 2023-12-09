def set_env(k, v):
    cmd = f'echo "{k}={v}" >> $GITHUB_ENV'
    print(f'Will run cmd: {cmd}')
    import os
    os.system(cmd)


def set_output(k, v):
    cmd = f'echo "{k}={v}" >> $GITHUB_OUTPUT'
    print(f'Will run cmd: {cmd}')
    import os
    os.system(cmd)
