# from typing import Set
# import streamlit as st
# from backend import run_llm
# from streamlit_chat import message

# st.header("Ebay Information Helper")

# prompt = st.text_input("Prompt", placeholder="Enter queries here")

# if (
#     "user_prompt_history" not in st.session_state 
#     and "chat_answers_history" not in st.session_state
#     and "chat_history" not in st.session_state
#     ):
#     st.session_state["user_prompt_history"] = []
#     st.session_state["chat_answers_history"] = []
#     st.session_state["chat_history"] = []


# def create_sources_string(source_urls: Set[str]) -> str:
#     if not source_urls:
#         return ""
#     sources_list = list(source_urls)
#     sources_list.sort()
#     sources_string = "sources:\n"
#     for i, source in enumerate(sources_list):
#         source = source.replace("index.html", "")
#         sources_string += f"{i + 1}, {source}\n"
#     return sources_string

# if prompt:
#     with st.spinner("Generating response..."):
#         generated_response = run_llm(
#             query=prompt, chat_history = st.session_state["chat_history"]
#             )
#         sources = set(
#             [doc.metadata["source"] for doc in generated_response["source_document"]]
#             )

#         # response to user
#         formatted_response = (
#             f'{generated_response["result"]} \n\n {create_sources_string(sources)}'
#         )
#         # print("here")
#         st.session_state["user_prompt_history"].append(prompt)
#         st.session_state["chat_answers_history"].append(formatted_response)
#         st.session_state["chat_history"].append(("human", prompt))
#         st.session_state["chat_history"].append(("ai", generated_response["result"]))
        

# if st.session_state["chat_answers_history"]:
#     for generated_response, user_query in zip(st.session_state["chat_answers_history"], st.session_state["user_prompt_history"]):
#         message(user_query, is_user=True)
#         message(generated_response)


from typing import Set
import streamlit as st
from backend import run_llm
# from streamlit_chat import message

# Main title and caption
st.title("Ebay Information Helper")

# Initialize session state messages and additional session state variables
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Function to create sources string
def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        source = source.replace("index.html", "")
        sources_string += f"{i + 1}. [{source}]({source})\n"
    return sources_string

# Display chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle new user input
if prompt := st.chat_input():
    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    with st.spinner("Generating response..."):
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )
        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_document"]]
        )

        # Formatted response to user
        formatted_response = (
            f'{generated_response["result"]} \n\n {create_sources_string(sources)}'
        )
        
        # Append assistant message to session state and display it
        st.session_state.messages.append({"role": "assistant", "content": formatted_response})
        st.chat_message("assistant").write(formatted_response)

        # Update chat histories
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", generated_response["result"]))
