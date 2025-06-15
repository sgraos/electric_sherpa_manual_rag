from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from vertexai.preview.generative_models import GenerativeModel, ChatSession
from pymongo import MongoClient

# --- 1. Embedding Generator (Gemini Embedding Model) ---
def return_embedding(text):
    MODEL_NAME = "gemini-embedding-001"
    DIMENSIONALITY = 3072
    task = "QUESTION_ANSWERING"
    model = TextEmbeddingModel.from_pretrained(MODEL_NAME)
    text_input = TextEmbeddingInput(text, task)
    embedding = model.get_embeddings([text_input], output_dimensionality=DIMENSIONALITY)
    return embedding

# --- 2. MongoDB Atlas Vector Search ---
def vector_search(user_query: str, collection: str) -> list[dict]:
    db = mongodb_client["ev_manuals"]
    collection = db[collection]

    query_embedding = return_embedding(user_query)[0].values
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "queryVector": query_embedding,
                "path": "embedding",
                "numCandidates": 150,
                "limit": 5,
            }
        },
        {
            "$project": {
                "_id": 0,
                "page_number": 1,
                "text": 1,
                "score": {"$meta": "vectorSearchScore"},
            }
        },
    ]
    results = collection.aggregate(pipeline)
    return list(results)

# --- 3. Gemini Flash Agent Call ---
def call_gemini_flash(instruction: str, user_question: str, retrieved_docs: list[dict]) -> str:
    model = GenerativeModel("gemini-2.0-flash")
    chat: ChatSession = model.start_chat()

    # Format retrieved content
    context_blocks = [
        f"[Page {doc['page_number']}]: {doc['text']}" for doc in retrieved_docs
    ]
    combined_context = "\n\n".join(context_blocks)

    # Prompt
    prompt = f"""
    You are an assistant helping users by referencing an EV car manual.

    ## Instructions:
    {instruction}

    ## Context from Manual (retrieved via vector search):
    {combined_context}

    ## User Question:
    {user_question}

    ## Your Answer:
    """
    response = chat.send_message(prompt)
    return response.text

# --- 4. Main RAG Query Function ---
def run_rag_query_quick(user_question: str, manual_collection: str):
    retrieved_chunks = vector_search(user_question, manual_collection)

    # You control formatting here:
    instruction = """
Format the answer into 3 sections:
1. 📘 Summary of the issue
2. 🔧 Suggested action steps based on manual
3. 📄 Page references (include page numbers where info is found)

Be concise and helpful.
"""

    final_answer = call_gemini_flash(instruction, user_question, retrieved_chunks)
    return final_answer

# --- 5. MongoDB Setup ---
mongo_uri = "mongodb+srv://rag_access:rdMnHQ1usHRncXYp@cluster0.pfd6gvx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongodb_client = MongoClient(mongo_uri, appname="ntuakshayrao.evmanual_rag")
mongodb_client.admin.command("ping")

# --- 6. Run Query ---
if __name__ == "__main__":
    collection_name = "Kia_EV6"
    user_query = "My car is not starting"

    answer = run_rag_query_quick(user_query, collection_name)
    print("\n🚗 Gemini Flash RAG Response:\n")
    print(answer)
