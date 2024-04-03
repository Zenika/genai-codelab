from langchain_community.llms import ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.prompts import ChatPromptTemplate

from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader


OLLAMA_URL = "http://localhost:11434"

MODEL = "openhermes"

llm = ollama.Ollama(
    base_url=OLLAMA_URL,
    model=MODEL
)


