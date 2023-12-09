import json
import os.path
import re

import requests

from utils import set_output


class Release:
    def __init__(self, name: str, version_pattern: str):
        # repo name
        self.name = name
        # release info https://docs.github.com/en/rest/releases/releases#get-the-latest-release
        self.release = self._get_latest_release()
        self.version = self._get_version(version_pattern)
        if self.release is not None:
            self.assets = self.release.get('assets', None)
        else:
            self.assets = None

    def _get_latest_release(self):
        headers = {"Accept": "application/vnd.github+json"}
        url = f"https://api.github.com/repos/{self.name}/releases/latest"
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            result = json.loads(r.text)
            return result
        else:
            print(r)
            return None

    def _get_version(self, pattern):
        """
        获取版本号

        :param pattern: 版本号的正则形式
        :return:
        """
        version = self.release.get('tag_name', None)
        if version:
            version = re.search(pattern, version)
            return version.group()
        return None

    def _get_download_link(self) -> dict:
        links = {}
        if self.assets:
            for asset in self.assets:
                links[asset['name']] = asset['browser_download_url']
        return links

    def download_file(self, keywords: list, dst_path, set_out=False):
        """
        下载文件名中包含指定关键字的文件

        :param set_out: 是否需要设置GITHUB_OUTPUT
        :param keywords: 关键字列表
        :param dst_path: 文件下载目录
        :return: None
        """
        links = self._get_download_link()
        for keyword in keywords:
            # links包含了所有asset的下载链接
            # 遍历links找到与关键字相关的下载链接
            for asset_name in links.keys():
                if keyword in asset_name:
                    download_link = links[asset_name]
                    if set_out:
                        set_output('link', download_link)
                    file_name = download_link.split('/')[-1]
                    file_path = os.path.join(dst_path, file_name)
                    with open(file_path, 'wb') as f:
                        print(f"Downloading {file_name}...")
                        down_data = requests.get(download_link).content
                        f.write(down_data)
                        print(f"{file_name} saved.")
                    break
