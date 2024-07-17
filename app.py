# streamlit을 사용한 gpt 채팅방

from openai import OpenAI
import streamlit as st
import time

client = OpenAI(api_key='YOUR_API_KEY')

assistant_id=''

with st.sidebar:
   thread_btn = st.button("Create Threads")

   if "thread_id" not in st.session_state:
      st.session_state.thread_id = ""

   if thread_btn: 
      thread = client.beta.threads.create()
      st.session_state.thread_id=thread.id
      st.subheader(thread.id)
      st.info('thread가 생성되었습니다')

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")
if "messages" not in st.session_state:
   st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
   st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
   if not st.session_state.thread_id:
      st.info("Please make your Thread.")
      st.stop()

   st.session_state.messages.append({"role": "user", "content": prompt})
   st.chat_message("user").write(prompt)
   response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
   msg = response.choices[0].message.content
   st.session_state.messages.append({"role": "assistant", "content": msg})

   
   message = client.beta.threads.messages.create(
      thread_id = st.session_state.thread_id,
      role="user",
      content="다음의 방정식을 풀고 싶습니다. '3x + 11 = 14'. 수학선생님 도와주실 수 있나요?"
   )

   run = client.beta.threads.runs.create(
      thread_id = st.session_state.thread_id,
      assistant_id=assistant_id,
   )

   while(True):
      run = client.beta.threads.runs.retrieve(
         thread_id = st.session_state.thread_id,
         run_id=run.id,
      )
      if(run.status == 'completed'):
         break
      else:
         time.sleep(2)

   thread_messages = client.beta.threads.messages.list(
      thread_id = st.session_state.thread_id
   )
   meg = thread_messages.data[0].content[0].text.value

   st.chat_message("assistant").write(msg)