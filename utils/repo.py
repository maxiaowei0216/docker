import json
import os.path
import re
from datetime import datetime, timedelta

import requests


class Release:
    def __init__(self, name: str, version_pattern: str):
        # repo name
        self.name = name
        # release info https://docs.github.com/en/rest/releases/releases#get-the-latest-release
        self.release = self._get_latest_release()
        self.assets = self.release.get('assets', None)
        self.version = self._get_version(version_pattern)

    def _get_latest_release(self):
        headers = {"Accept": "application/vnd.github+json"}
        url = f"https://api.github.com/repos/{self.name}/releases/latest"
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            result = json.loads(r.text)
            return result
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

    def is_need_update(self, dh: int = 24) -> bool:
        """
        检查是否需要更新，即最新的release的发布时间是否在指定范围内

        :param dh: 时间差，单位为小时。
        :return: true / false
        """
        if dh < 0:
            return True
        publish_time = self.release.get('published_at', None)
        if publish_time:
            # UTC
            publish_time = datetime.strptime(publish_time, '%Y-%m-%dT%H:%M:%SZ')
            now = datetime.utcnow()
            delta_time = timedelta(hours=dh)
            if (now - publish_time) <= delta_time:
                return True
        return False

    def download_file(self, keywords: list, dst_path):
        """
        下载文件名中包含指定关键字的文件

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
                    file_name = download_link.split('/')[-1]
                    file_path = os.path.join(dst_path, file_name)
                    with open(file_path, 'wb') as f:
                        print(f"Downloading {file_name}...")
                        down_data = requests.get(download_link).content
                        f.write(down_data)
                        print(f"{file_name} saved.")
                    break
