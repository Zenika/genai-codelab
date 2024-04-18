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

  // First Step
  const prompt = 'Who are you ?'
  const result = await llm.invoke(prompt);
  console.log(result.content);

  // Prompt Template
  const template = PromptTemplate.fromTemplate('explain me this Regular expression{regexp}')
  const chain = template.pipe(llm)
  const regexpExplanation = await chain.invoke({regexp: '^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$'});
  console.log(regexpExplanation.content)

  // Few Short learning
  const examples = [
      {animal: 'cow', sound: 'moo'},
      {animal: 'cat', sound: 'meow'},
      {animal: 'dog', sound: 'woof'}
  ]
  const examplePrompt = ChatPromptTemplate.fromTemplate(`Human: {animal} 
  AI: {sound}`)

  const fewShotPrompt = new FewShotChatMessagePromptTemplate({
    prefix: "You are an animal expert able to guess the sound an animal does based on a name.",
    suffix: "Human: {input}",
    examplePrompt,
    examples,
    inputVariables: ["input"],
  });

  const formattedPrompt = await fewShotPrompt.format({input: 'lion'})
  const response = await llm.invoke(formattedPrompt)
  console.log(response.content)

  // Memory
  const runnableWithMessageHistoryPrompt = ChatPromptTemplate.fromMessages([
    [
      "system",
      "You are a helpful assistant. Answer all questions to the best of your ability.",
    ],
    new MessagesPlaceholder("chat_history"),
    ["human", "{input}"],
  ]);
    
  const chain2 = runnableWithMessageHistoryPrompt.pipe(llm);
  const chatHistory = new ChatMessageHistory();

  const chainWithMessageHistory = new RunnableWithMessageHistory({
    runnable: chain2,
    getMessageHistory: (_sessionId) => chatHistory,
    inputMessagesKey: "input",
    historyMessagesKey: "chat_history",})


  const r = await chainWithMessageHistory.invoke(
    {
      input:
        "Translate this sentence from English to French: I love programming.",
    },
    { configurable: { sessionId: "unused" } }
  )

  console.log(r.content)
    const secondR = await chainWithMessageHistory.invoke(
    {
      input:
        "What Did I just ask you ?",
    },
    { configurable: { sessionId: "unused" } }
  );

  // Summarize
  const summarizationChain = loadSummarizationChain(llm, { type: "map_reduce" });
  const text = fs.readFileSync("java_introduction.txt", "utf8");
  
  const textSplitter = new RecursiveCharacterTextSplitter({ chunkSize: 1000 });
  const docs = await textSplitter.createDocuments([text]);
  const summary = await summarizationChain.invoke({input_documents: docs});

  console.log(summary.text)
};

main();