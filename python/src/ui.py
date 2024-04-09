import streamlit as st
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_community.llms import ollama
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain.prompts import FewShotChatMessagePromptTemplate

OLLAMA_URL = "http://localhost:11434"

MODEL = "openhermes"

llm = ollama.Ollama(base_url=OLLAMA_URL, model=MODEL)

st.title("GenAi Codelab by Zenika")
st.write("")

st.image("./image/schema.png")

tab_simple, tab_template, tab_few_shot, tab_summarize, tab_memory = st.tabs(
    [
        'Simple prompt',
        'Templated prompt',
        'Few shot learning',
        'Document summarize',
        'Memory'
    ]
)

with tab_simple:
    prompt = st.chat_input("What would you like to know ?")
    response_callback = StreamlitCallbackHandler(st.container())
    if prompt:
        llm.invoke(prompt, {"callbacks": [response_callback]})

with tab_template:
    st.write("Explique moi cette expression régulière (^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$) ")

    prompt = PromptTemplate.from_template(
        "Explain me what is the purpose of this regexp {regexp}"
    )
    chain = prompt | llm

    regexp = st.chat_input("RegExp: ")
    story_callback = StreamlitCallbackHandler(st.container())

    if regexp:
        chain.invoke({"regexp": regexp}, {"callbacks": [story_callback]})

with tab_few_shot:
    st.write("Quel son fait un animal : ")

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

    animal = st.chat_input("Animal")

    few_shot_example_chain = final_prompt | llm
    few_shot_callback = StreamlitCallbackHandler(st.container())

    if animal:
        few_shot_example_chain.invoke(
            {"input": animal}, {"callbacks": [few_shot_callback]}
        )

with tab_summarize:
    st.write("Résume moi le contenu d'un lien (https://fr.wikipedia.org/wiki/Niort)")
    link = st.chat_input("Résume moi ce lien")
    summarize_callback = StreamlitCallbackHandler(st.container())
    if link:
        chain = load_summarize_chain(llm, chain_type="refine")
        loader = WebBaseLoader(link)
        pages = loader.load()
        chain.invoke(pages, {"callbacks": [summarize_callback]})

with tab_memory:
    st.write("Reprenons notre conversation la ou nous l'avions laissé:")
    st.write("Human: Can you translate I love programming in French")
    st.write("AI: J'adore la programmation")

    messages = ChatMessageHistory()
    messages.add_user_message('Can you translate I love programming in French')
    messages.add_ai_message("J'adore la programmation")

    memory = ConversationBufferMemory(chat_memory=messages)
    conversation_chain = ConversationChain(llm=llm, memory=memory)

    follow_up = st.chat_input("What did I just ask you ?")
    memory_callback = StreamlitCallbackHandler(st.container())
    if follow_up:
        conversation_chain.predict(input=follow_up, callbacks=[memory_callback])
