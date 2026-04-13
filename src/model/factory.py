"""
模型工厂
"""
from abc import ABC, abstractmethod
from typing import Optional

from dotenv import load_dotenv
import os

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from src.utils.config_handler import rag_conf

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_BASE_URL'] = os.getenv("OPENAI_BASE_URL")
os.environ['DASHSCOPE_API_KEY'] = os.getenv("DASHSCOPE_API_KEY")


class BaseModelFactory(ABC):
    @abstractmethod
    def generate(self) -> Optional[Embeddings | BaseChatModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generate(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatOpenAI(model=rag_conf['chat_model_name'])


class EmbeddingsModelFactory(BaseModelFactory):
    def generate(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(model=rag_conf['embedding_model_name'])


chat_model = ChatModelFactory().generate()
embedding_model = EmbeddingsModelFactory().generate()
