import streamlit as st
import datetime
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion import ChatCompletion, Choice

st.title("🔎 LangChain - Chat with search")
html_temp = """
    <div style="background-color:yellow ;padding:10px; border-radius:50px;">
    <h2 style="color:white;text-align:center;">Iris Classification</h2>
    </div>
    <div style="background-color:yellow; padding-top:10px; margin:10px;
     border-radius:50px;">
    <h6 style="color:black;text-align:center;">Project By:-Damodar Tiwari</h6>
    </div>
    """
# See https://github.com/openai/openai-python/issues/715#issuecomment-1809203346

def create_chat_completion(response: str, role: str = "assistant") -> ChatCompletion:
    return ChatCompletion(
        id="foo",
        model="gpt-3.5-turbo",
        object="chat.completion",
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                message=ChatCompletionMessage(
                    content=response,
                    role=role,
                ),
            )
        ],
        created=int(datetime.datetime.now().timestamp()),
    )


@patch("openai.resources.chat.Completions.create")
def test_Chatbot(openai_create):
    at = AppTest.from_file("Chatbot.py").run()
    assert not at.exception
    at.chat_input[0].set_value("Do you know any jokes?").run()
    assert at.info[0].value == "Please add your OpenAI API key to continue."

    JOKE = "Why did the chicken cross the road? To get to the other side."
    openai_create.return_value = create_chat_completion(JOKE)
    at.text_input(key="chatbot_api_key").set_value("sk-...")
    at.chat_input[0].set_value("Do you know any jokes?").run()
    print(at)
    assert at.chat_message[1].markdown[0].value == "Do you know any jokes?"
    assert at.chat_message[2].markdown[0].value == JOKE
    assert at.chat_message[2].avatar == "assistant"
    assert not at.exception


@patch("langchain.llms.OpenAI.__call__")
def test_Langchain_Quickstart(langchain_llm):
    at = AppTest.from_file("pages/3_Langchain_Quickstart.py").run()
    assert at.info[0].value == "Please add your OpenAI API key to continue."

    RESPONSE = "1. The best way to learn how to code is by practicing..."
    langchain_llm.return_value = RESPONSE
    at.sidebar.text_input[0].set_value("sk-...")
    at.button[0].set_value(True).run()
    print(at)
    assert at.info[0].value == RESPONSE
st.markdown('Damodar Tiwari')
def main():
    st.title("Flowers Classifier")
    html_temp = """
    <div style="background-color:teal ;padding:10px; border-radius:50px;">
    <h2 style="color:white;text-align:center;">Iris Classification</h2>
    </div>
    <div style="background-color:yellow; padding-top:10px; margin:10px;
     border-radius:50px;">
    <h6 style="color:black;text-align:center;">Project By:-Damodar Tiwari</h6>
    </div>
    """
if __name__=='__main__':
    main()
