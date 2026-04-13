"""
加载 RAG 所需的文档
"""
import hashlib

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

from .logger_handler import logger
from .path_handler import get_abs_path
from .config_handler import chroma_conf

import os


def get_file_md5_hex(file_name: str) -> str | None:
    """
    get file md5 hex string, judge whether it loaded or not
    :param: file_name: file path
    :return: file md5 hex string
    """
    # ensure file_name dose exist and is a file
    if not os.path.isfile(file_name):
        logger.error(f"{file_name} does not exist or isn't a file")
        return None

    md5_obj = hashlib.md5()
    chunk_size = 4096
    try:
        with open(file_name, 'rb') as f:
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)

            return md5_obj.hexdigest()
    except Exception as e:
        logger.error(f"calculate file {file_name} md5 hex string error:{e}")
        return None


def is_repeat_md5_hex(md5_hex: str) -> bool:
    """
    whether the file has been uploaded repeatedly
    :param md5_hex: md5 hex for the file
    :return: result of md5 hex check
    """
    try:
        md5_absolute_path = get_abs_path(chroma_conf['md5_store_path'])
    except KeyError as e:
        logger.error(f"key md5_store_path not found")
        raise e

    # if md5 store file does not exist, then make the file
    if not os.path.exists(md5_absolute_path):
        open(md5_absolute_path, 'w', encoding='utf-8').close()
        return False

    with open(md5_absolute_path, 'r', encoding='utf-8') as fr:
        for line in fr.readlines():
            line = line.strip()
            if line == md5_hex:
                return True
        return False


def save_md5_hex(md5_hex: str):
    with open(chroma_conf['md5_store_path'], 'a', encoding='utf-8') as fa:
        fa.write(md5_hex + '\n')


def list_allowed_type_in_dir(path: str, allow_type: tuple[str]) -> tuple[str, ...] | None:
    """
    list allowed type file absolute path
    :param: path: directory path
    :param: allow_type: allowed type
    :return: list of allowed type file path
    """
    # ensure the path is a directory
    if not os.path.isdir(path):
        logger.error(f"{path} does not exist or isn't a directory")
        return None

    # return list of allowed type file path
    return tuple(
        get_abs_path(os.path.join(path, file_name)) for file_name in os.listdir(path) if file_name.endswith(allow_type))


def load_documents(file_path: str, passwd=None) -> list[Document] | None:
    if file_path.endswith('txt'):
        return TextLoader(file_path=file_path, encoding='utf-8').load()
    elif file_path.endswith('pdf'):
        return PyPDFLoader(file_path=file_path, password=passwd).load()
    return None


if __name__ == '__main__':
    # print(get_file_md5_hex(".env"))
    # print(list_allowed_type_in_dir("utils", tuple(".py")))
    pass
