const { ChatOllama }  = require("@langchain/community/chat_models/ollama");
const { MessagesPlaceholder, PromptTemplate, ChatPromptTemplate, FewShotChatMessagePromptTemplate } = require("@langchain/core/prompts");
const { ChatMessageHistory } = require("langchain/stores/message/in_memory");
const { RunnableWithMessageHistory } = require("@langchain/core/runnables");
const { loadSummarizationChain } = require("langchain/chains");
const { RecursiveCharacterTextSplitter } = require("langchain/text_splitter");
const fs = require("fs");

const OLLAMA_URL = 'http://localhost:11434'
const MODEL = 'openhermes'
const main = async () => {

  const llm = new ChatOllama({
    baseUrl: OLLAMA_URL,
    model: MODEL,
    temperature: 0.1
  });

  // YOUR CODE GOES HERE

};

main();