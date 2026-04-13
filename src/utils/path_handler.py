"""
为整个工程提供统一绝对路径
"""

import os


def get_project_root_path() -> str:
    """
    get project root path
    :return: project root path
    """
    cur_file = os.path.abspath(__file__)
    cur_dir = os.path.dirname(os.path.dirname(cur_file))
    return os.path.dirname(cur_dir)


def get_abs_path(path: str) -> str:
    """
    get absolute path
    :param: path: the path will be maked
    :return: the absolute path
    """
    project_root_path = get_project_root_path()
    return os.path.join(project_root_path, path)


if __name__ == '__main__':
    # print(get_project_root_path())
    pass