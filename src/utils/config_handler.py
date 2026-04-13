"""
为工程加载配置文件
"""
from .path_handler import get_abs_path
import yaml
from os.path import join

config_path = get_abs_path('config')


def load_rag_config(config_path: str = join(config_path, 'rag.yml')):
    with open(config_path, 'r', encoding="utf-8") as fr:
        return yaml.load(fr, Loader=yaml.FullLoader)


def load_chroma_config(config_path: str = join(config_path, 'chroma.yml')):
    with open(config_path, 'r', encoding="utf-8") as fr:
        return yaml.load(fr, Loader=yaml.FullLoader)


def load_prompts_config(config_path: str = join(config_path, 'prompts.yml')):
    with open(config_path, 'r', encoding="utf-8") as fr:
        return yaml.load(fr, Loader=yaml.FullLoader)


def load_agent_config(config_path: str = join(config_path, 'agent.yml')):
    with open(config_path, 'r', encoding="utf-8") as fr:
        return yaml.load(fr, Loader=yaml.FullLoader)


rag_conf = load_rag_config()
chroma_conf = load_chroma_config()
prompts_conf = load_prompts_config()
agent_conf = load_agent_config()
