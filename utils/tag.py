def parse_tags(lines: list[str]) -> list:
    """
    获取所有的版本tag
    :param lines:
    :return: 所有版本的列表
    """

    def is_version(ver):
        parts = ver.split('.')
        return all(part.isdigit() for part in parts)

    versions = set()
    for line in lines:
        if line.startswith('- '):
            vers = line.replace(',', '').split()
            for v in vers:
                if v[0].lower() == 'v':
                    v = v[1:]
                if is_version(v):
                    versions.add(v)

    versions = list(versions)
    versions.sort(reverse=True)
    return versions


def generate_tag(versions: list) -> str:
    """
    生成markdown格式的tag列表
    :param versions: 形式为x.x.x的版本集合
    :return: string
    """

    version_dict = {}
    content = ''

    for version in versions:
        major_minor_version = ".".join(version.split(".")[:2])
        if major_minor_version not in version_dict:
            version_dict[major_minor_version] = []
        version_dict[major_minor_version].append(version)

    mm_versions = list(version_dict.keys())
    mm_versions.sort(reverse=True)
    for mm_ver in mm_versions:
        full_vers = version_dict[mm_ver]
        full_vers.sort(reverse=True)
        if mm_ver == mm_versions[0]:
            content = f'- {full_vers[0]}, {mm_ver}, latest\n'
        else:
            content += f'- {full_vers[0]}, {mm_ver}\n'
        for v in full_vers[1:]:
            if not mm_ver == v:
                content += f'- {v}\n'
    return content


def get_tag_lines(file):
    """
    获取readme中tag标签所在的行的index，不包含标题
    :param file:
    :return:
    """
    start = end = -1
    with open(file, 'r', encoding='utf8') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if start == -1 and lines[i].strip() == '# Tags':
                start = i + 1
            elif start > -1 and lines[i].startswith('#'):
                end = i - 1
                break
    return start, end, lines


def generate_readme(current_ver, file='README.md'):
    print(f'Current version is {current_ver}')
    start, end, lines = get_tag_lines(file)
    if end >= start > -1:
        versions = parse_tags(lines[start:end])
        latest = '0.0.0'
        if len(versions) > 0:
            latest = versions[0]
            print(f'Latest version in {file} is {latest}')
        if current_ver not in versions:
            versions.append(current_ver)
            version_str = generate_tag(versions)
            new_file_lines = lines[:start] + version_str.splitlines(keepends=True) + lines[end:]
            with open(file, 'w', encoding='utf8') as f:
                f.writelines(new_file_lines)
        else:
            print(f'{current_ver} is already in {file}')
            return False

        return current_ver > latest
    return False


if __name__ == '__main__':
    generate_readme('1.3.3')
