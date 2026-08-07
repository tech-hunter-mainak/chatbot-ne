from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS to allow the Svelte frontend (usually running on localhost:5173 or similar) to fetch data
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development purposes
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Define the expected request body structure
class ChatRequest(BaseModel):
    query: str
    userlang: str
    destlang: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Simple chat endpoint taking query, userlang, and destlang.
    Returns a mocked translated/assistant response.
    """
    query_lower = request.query.lower()
    
    # Mocking context-aware responses based on the query and languages
    if 'assamese' in query_lower or 'hello' in query_lower:
        reply = f"নমস্কাৰ! (Namaskar!) Backend received your query. Request context: {request.userlang} -> {request.destlang}. আপোনাক কেনেকৈ সহায় কৰিব পাৰো? (How can I help you?)"
    elif 'manipuri' in query_lower:
        reply = f"ꯈꯨꯔꯨꯝꯖꯔꯤ! (Khurumjari!) Backend context: {request.userlang} -> {request.destlang}. What would you like to know?"
    elif 'mizo' in query_lower:
        reply = f"Chibai! How can I assist you with the Mizo language today? (Context: {request.userlang} -> {request.destlang})"
    else:
        reply = f"Backend Response: You asked '{request.query}'. I am ready to help translate or explain from {request.userlang} to {request.destlang}!"

    return {"reply": reply}

# To run this server, use the command:
# uvicorn main:app --reload