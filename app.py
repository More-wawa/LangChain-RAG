import streamlit as st
from src.agent.react_agent import ReactAgent

# title
st.title("智扫通机器人智能客服")
st.divider()

if "agent" not in st.session_state:
    st.session_state.agent = ReactAgent()
if "message" not in st.session_state:
    st.session_state.message = list()

# 每次重新加载历史对话记录
for message in st.session_state.message:
    st.chat_message(message["role"]).write(message["content"])

# user input prompt
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.message.append({"role": "user", "content": prompt})

    response_cache = list()

    with st.spinner("thinking..."):
        res_stream = st.session_state["agent"].stream(prompt)


        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk


        st.chat_message("assistant").write_stream(capture(res_stream, response_cache))
        st.session_state.message.append({"role": "assistant", "content": response_cache[-1]})
