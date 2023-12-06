import streamlit as st

from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun


with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Damodar12345678/chatbot_on_streamlit?quickstart=1)"
    # "[st.write["Try It Out With This API Ket :- "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""]]"
   " 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"

st.title("🔎 Sarvagya - Ask Whatever You Want")

"""

This application is `capable of answering all your questions` based
on the input given by your files, chats and your prompts.  Its name
is Sarvagya. You can use it by entering the API key of your Open AI. 🤝  
[github.com/langchain-ai/streamlit-agent](https://github.com/Damodar12345678/chatbot_on_streamlit).
"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Who won the election in MP?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)
    search = DuckDuckGoSearchRun(name="Search")
    search_agent = initialize_agent([search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True)
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)

