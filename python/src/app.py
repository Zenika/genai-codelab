from langchain_community.llms import ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import FewShotChatMessagePromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain.memory import ChatMessageHistory
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

OLLAMA_URL = "http://localhost:11434"


MODEL = "openhermes"

llm = ollama.Ollama(
    base_url=OLLAMA_URL,
    model=MODEL,
    temperature=0.5
)

# Step 1
prompt = 'Who are you ?'
response = llm.invoke(prompt)
print(response)

# PromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ('system', 'You are a professional regexp instructor'),
    ('user', 'explain the following regexp {regexp} ')
])

chain = prompt | llm
print(chain.invoke({'regexp': '^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$'}))

# Few shot learning
examples = [
    {'animal': 'cow', 'sound': 'moo'},
    {'animal': 'cat', 'sound': 'meow'},
    {'animal': 'dog', 'sound': 'woof'}
]

example_prompt = ChatPromptTemplate.from_messages([
    ('human', '{animal}'),
    ('ai', '{sound}')
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
)

final_prompt = ChatPromptTemplate.from_messages([
    ('system',
     'You are an animal sound expert, able to give the sound an animal does based on the name of the animal'),
    few_shot_prompt,
    ('human', '{input}')
])

chain = final_prompt | llm

print(chain.invoke({'input': 'lion'}))

# Summary
chain = load_summarize_chain(llm, chain_type="refine")
loader = WebBaseLoader('https://fr.wikipedia.org/wiki/Grand_mod%C3%A8le_de_langage')
docs = loader.load()
print(chain.invoke(docs))


# Memory
chat_messages = ChatMessageHistory()
chat_messages.add_user_message('Can you translate I love programming in French?')
chat_messages.add_ai_message("J'adore la programmation")

memory = ConversationBufferMemory(chat_memory=chat_messages)
conversation_chain = ConversationChain(llm=llm, memory=memory)
print(conversation_chain.predict(input="what was my previous question ?"))
