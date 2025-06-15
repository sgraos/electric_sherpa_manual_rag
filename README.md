# Retrieval function for EV manual Q&A using MongoDB

EV manual data is embedded in MongoDB collection using the "Admin panel" app

This is a user-facing application to select EV manuals from list of manuals available and ask questions

There are 2 different methods for getting answers:
1. RAG quick uses Gemini-2.0-Flash to get a quick response from the EV manual selected (quick, but accuracy is not checked)
2. RAG comprehensive uses Gemini-2.0-Flash to get the initial response and validate with Gemini-2.0-Flash-Lite (slower, but more accurate)
