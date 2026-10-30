from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
st.set_page_config(page_title="AI Powered Chatbot", page_icon="🤖")
st.title("🤖 AI Powered Chatbot ")
st.caption('Type EXIT to quit the conversation')
@st.cache_resource
def llm_lode():
    return ChatOllama(
        model="gemma2:2b",
        temperature=0.1)
llm=llm_lode()
parser=StrOutputParser()

#chat history
if "chat_his" not in st.session_state:
    st.session_state.chat_his=[("system","you are helpful AI tutore assistant and Be concise and precise (3–10 sentences, unless the question requires more)") ]
if "ended" not in st.session_state:
    st.session_state.ended= False

chat_his=st.session_state.chat_his

#Sidebar
with st.sidebar:
    st.header("Options")
    if st.button("🗑️ New conversation"):
        st.session_state.chat_his = [
            ("system", "you are helpful AI tutore assistant and Be concise")
        ]
        st.session_state.ended = False
        st.rerun()
# Show previous messages 
for role, content in chat_his:
    if role == "system":
        continue
    with st.chat_message("user" if role == "user" else "assistant"):
        st.markdown(content)

if st.session_state.ended:
    st.info("THANK_YOU... Conversation ended. Click 'New conversation' in the sidebar to start again.")
    st.stop()

# chat input
user_input=st.chat_input("YOU")
if user_input:
    user_input=user_input.strip()
    if user_input.lower()=="exit":
        st.session_state.ended=True
        st.rerun()
    chat_his.append(("user",user_input))
    with st.chat_message("user"):
        st.markdown(user_input)
        
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            promt=ChatPromptTemplate.from_messages(chat_his)
            chain= promt|llm|parser
            res= chain.invoke({})
        st.markdown(res)

    chat_his.append(("assistant",res))
