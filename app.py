import streamlit as st

from retrieval_application_comprehensive import run_rag_query_comprehensive
from retrieval_application_quick import run_rag_query_quick
from mongo_db_utils import get_collection_list
import re

def get_image_urls(coll_name, pglist_str):
    ## Generate URLs of manual page images
    pglist = re.findall(r'\d+', pglist_str)
    url = 'https://storage.googleapis.com/electric_sherpa_manual_images/' + coll_name + '_'
    strlist = [url + s.lstrip().rstrip() + '.jpg' for s in pglist]
    return strlist

def main():
    ## Initialize window
    st.title("Electric Sherpa Manual Q and A")
    st.subheader("Get answer to your EV model problems")
    st.write("Please wait for response if you see the 'running' status")

    ## Provide user input options
    available_manuals = get_collection_list()
    manual_req = st.selectbox("Select your EV model", available_manuals)

    select_options = ["Quick", "Comprehensive"]
    selection = st.segmented_control("Select retrieval type", options=select_options, selection_mode="single")
    prompt = st.chat_input("What problem are you having with your EV?")

    ## Generate results
    result = ''
    if prompt:
        if selection == "Comprehensive":
            result = run_rag_query_comprehensive(prompt, manual_req)
        else:
            result = run_rag_query_quick(prompt, manual_req)

        if ('Page references:' in result):
            split_result = result.split('Page references:')
            st.write(split_result[0])
            image_list = get_image_urls(manual_req, split_result[1])
            if(len(image_list)>0):
                with st.expander("See manual pages"):
                    st.image(image_list)
        else:
            st.write(result)



if __name__ == "__main__":
    main()
