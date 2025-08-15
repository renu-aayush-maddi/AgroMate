import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

from src.prompt import structured_system_prompt
from src.helper import download_hugging_face_embeddings

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# API Keys
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# Pinecone + retriever
embeddings_default = download_hugging_face_embeddings()
index_name = "test"
Pinecone(api_key=PINECONE_API_KEY)
docsearch_default = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings_default)
retriever_default = docsearch_default.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# LLM setup
llm_default = GoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4, max_tokens=500)
prompt_default = ChatPromptTemplate.from_messages([
    ("system", structured_system_prompt),
    ("human", "{input}\n\nAdditional Info (if any): {location_info}")
])
qa_chain_default = create_stuff_documents_chain(llm_default, prompt_default)
rag_chain_default = create_retrieval_chain(retriever_default, qa_chain_default)

class QuestionRequest(BaseModel):
    question: str
    location: dict | None = None

# @app.post("/answer")
# async def run_query(body: QuestionRequest):
#     if not body.question.strip():
#         raise HTTPException(status_code=400, detail="Question is required")
#     response = await asyncio.to_thread(rag_chain_default.invoke, {"input": body.question})
#     return {"answer": response["answer"]}

@app.post("/answer")
async def run_query(body: QuestionRequest):
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question is required")
    
    loc_str = ""
    if body.location:
        loc_str = f"User location: lat {body.location.get('lat')}, lon {body.location.get('lon')}"
        print(loc_str)

    response = await asyncio.to_thread(
        rag_chain_default.invoke,
        {
            "input": body.question,
            "location_info": loc_str
        }
    )
    return {"answer": response["answer"]}


