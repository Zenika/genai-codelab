import { ChatOllama } from '@langchain/community/chat_models/ollama';
import {
  MessagesPlaceholder,
  PromptTemplate,
  ChatPromptTemplate,
  FewShotChatMessagePromptTemplate,
} from '@langchain/core/prompts';
import { ChatMessageHistory } from 'langchain/stores/message/in_memory';
import { RunnableWithMessageHistory } from '@langchain/core/runnables';
import { loadSummarizationChain } from 'langchain/chains';
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';
import { readFile } from 'node:fs/promises';

const OLLAMA_URL = 'http://localhost:11434';
const MODEL = 'openhermes';
const llm = new ChatOllama({
  baseUrl: OLLAMA_URL,
  model: MODEL,
  temperature: 0.1,
});
