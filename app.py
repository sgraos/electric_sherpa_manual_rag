import streamlit as st

from retrieval_application_comprehensive import run_rag_query_comprehensive
from retrieval_application_quick import run_rag_query_quick
from mongo_db_utils import get_collection_list

def main():
## Initialize window
    st.title("Electric Sherpa Manual Q and A")
    st.subheader("Get answer to your EV model problems")
    st.write("Please wait for response if you see the 'running' status")

    available_manuals = get_collection_list()
    manual_req = st.radio("Select your EV model", available_manuals)

    select_options = ["Quick", "Comprehensive"]
    selection = st.segmented_control("Select retrieval type", options=select_options, selection_mode="single")
    prompt = st.chat_input("What problem are you having with your EV?")

    result = ''
    if prompt:
        if selection == "Comprehensive":
            result = run_rag_query_comprehensive(prompt, manual_req)
        else:
            result = run_rag_query_quick(prompt, manual_req)

        st.write(result)


if __name__ == "__main__":
    main()
