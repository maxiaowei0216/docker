import argparse
import json
import os

import requests


def login(user: str, pwd: str):
    url = 'https://hub.docker.com/v2/users/login'
    headers = {"Content-Type": "application/json"}
    data = {
        "username": user,
        "password": pwd
    }
    res = requests.post(url, headers=headers, data=json.dumps(data))
    if res.status_code == 200:
        return json.loads(res.text).get('token', None)
    return None


def sync_readme(repo: str, path: str, token: str):
    with open(path, 'r') as f:
        readme = f.read()
        if readme:
            url = f'https://hub.docker.com/v2/repositories/{repo}/'
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            data = {"full_description": readme}
            res = requests.patch(url, headers=headers, data=json.dumps(data))
            if res.status_code == 200:
                print("Sync readme file succeed")
            else:
                print("Sync readme file failed with return code: %d" % res.status_code)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repo')
    parser.add_argument('-p', '--path')
    args = parser.parse_args()

    username = os.environ.get('HUB_USERNAME', None)
    password = os.environ.get('HUB_PASSWORD', None)
    if username and password:
        token = login(username, password)
        sync_readme(args.repo, args.path, token)
    else:
        print("Can't get username and password from environment variables.")
        exit(-1)

if __name__ == '__main__':
    main()
