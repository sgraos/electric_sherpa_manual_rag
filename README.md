# Retrieval function for EV manual Q&A using MongoDB

## Introduction
This is a user-facing application to select EV manuals from list of manuals available and ask questions

## Components
The manual is extracted, chunked, the embeddings are extracted and stored in MongoDB using the "Admin panel" script found here: 

Screenshots of each page of the manual are extracted and stored in Google Cloud Storage.

The user app is developed in Python using a Streamlit frontend and hosted as a container on Google Cloud Run.

## How to use
There are 2 different methods for getting answers:
1. RAG quick uses Gemini-2.0-Flash to get a quick response from the EV manual selected (quick, but accuracy is not checked)
2. RAG comprehensive uses Gemini-2.0-Flash to get the initial response and validate with Gemini-2.0-Flash-Lite (slower, but more accurate). It uses a larger vector search limit to obtain more candidates

Screenshots of pages from the manual referenced in the answer are also provided to the user

Application can be viewed at: https://manual-rag-app-251571508738.us-east4.run.app/
