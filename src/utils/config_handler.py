"""
为工程加载配置文件
"""
from .path_handler import get_abs_path
import yaml
from os.path import join


def load_config(config_path: str):
    with open(config_path, 'r', encoding="utf-8") as fr:
        return yaml.load(fr, Loader=yaml.FullLoader)


base_config_path = get_abs_path('config')

rag_conf = load_config(join(base_config_path, 'rag.yml'))
chroma_conf = load_config(join(base_config_path, 'chroma.yml'))
prompts_conf = load_config(join(base_config_path, 'prompts.yml'))
agent_conf = load_config(join(base_config_path, 'agent.yml'))
