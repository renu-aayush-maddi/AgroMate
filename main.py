# # main.py
# import os
# import json
# import asyncio
# from datetime import datetime
# from typing import Optional

# from fastapi import FastAPI, HTTPException, Depends, Request
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from dotenv import load_dotenv

# from db_mongo import get_db, close_db
# from models_mongo import USERS_COLL, PROFILES_COLL, SESSIONS_COLL, user_doc, profile_doc, session_context_doc
# from schemas import SignupRequest, LoginRequest, TokenResponse, FarmerProfileRequest, FarmerProfileResponse, QuestionRequest
# from auth import hash_password, verify_password, create_access_token, get_current_user

# # LangChain / RAG
# from langchain_google_genai import GoogleGenerativeAI
# from langchain.chains import create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_pinecone import PineconeVectorStore
# from pinecone import Pinecone
# from src.prompt import structured_system_prompt
# from src.helper import download_hugging_face_embeddings

# load_dotenv()

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # tighten in prod
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.on_event("shutdown")
# async def shutdown_event():
#     await close_db()

# # API Keys
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# # Pinecone + retriever
# embeddings_default = download_hugging_face_embeddings()
# index_name = "test"
# Pinecone(api_key=PINECONE_API_KEY)
# docsearch_default = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings_default)
# retriever_default = docsearch_default.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# # LLM setup
# llm_default = GoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4, max_tokens=500)
# prompt_default = ChatPromptTemplate.from_messages([
#     ("system", structured_system_prompt + "\n\n"
#      "Use the provided farmer profile and session context when available.\n"
#      "If critical details are missing (e.g., crop type, growth stage, soil), ask concise follow-up questions.\n"
#      "If the user is authenticated, prefer profile defaults but confirm if outdated.\n"
#      "Always state assumptions if proceeding without some details.\n"
#      "You may include a single-line JSON after 'SESSION_UPDATE:' for context persistence."),
#     ("human", "{input}\n\nFarmer Profile: {farmer_profile}\nSession Context: {session_context}\nAdditional Info: {location_info}")
# ])
# qa_chain_default = create_stuff_documents_chain(llm_default, prompt_default)
# rag_chain_default = create_retrieval_chain(retriever_default, qa_chain_default)



# # Helpers
# def serialize_profile(profile: Optional[dict]) -> str:
#     if not profile:
#         return "None"
#     cleaned = {k: v for k, v in profile.items() if k not in ("_id", "user_id")}
#     return json.dumps(cleaned, ensure_ascii=False)

# async def get_or_create_session_context(db, session_id: str):
#     sc = await db[SESSIONS_COLL].find_one({"session_id": session_id})
#     if sc is None:
#         sc = session_context_doc(session_id)
#         await db[SESSIONS_COLL].insert_one(sc)
#     return sc

# async def update_session_context(db, session_id: str, updates: dict):
#     now = datetime.utcnow()
#     await db[SESSIONS_COLL].update_one(
#         {"session_id": session_id},
#         {
#             "$set": {f"data.{k}": v for k, v in updates.items()},
#             "$setOnInsert": {"session_id": session_id},
#             "$currentDate": {"updated_at": True},
#         },
#         upsert=True
#     )

# # Auth routes
# @app.post("/signup", response_model=TokenResponse)
# async def signup(body: SignupRequest, db=Depends(get_db)):
#     existing = await db[USERS_COLL].find_one({"email": body.email})
#     if existing:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     user = user_doc(email=body.email, password_hash=hash_password(body.password), name=body.name)
#     await db[USERS_COLL].insert_one(user)
#     token = create_access_token(body.email)
#     return TokenResponse(access_token=token)

# @app.post("/login", response_model=TokenResponse)
# async def login(body: LoginRequest, db=Depends(get_db)):
#     user = await db[USERS_COLL].find_one({"email": body.email})
#     if not user or not verify_password(body.password, user["password_hash"]):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     token = create_access_token(user["email"])
#     return TokenResponse(access_token=token)

# # Profile routes
# @app.get("/me", response_model=FarmerProfileResponse)
# async def get_profile(user=Depends(get_current_user), db=Depends(get_db)):
#     prof = await db[PROFILES_COLL].find_one({"user_id": user["email"]})
#     if not prof:
#         return FarmerProfileResponse()
#     return FarmerProfileResponse(
#         crops=prof.get("crops"),
#         soil_type=prof.get("soil_type"),
#         location_pref=prof.get("location_pref"),
#         irrigation_method=prof.get("irrigation_method"),
#         acreage=prof.get("acreage"),
#         custom_notes=prof.get("custom_notes"),
#     )

# @app.post("/me", response_model=FarmerProfileResponse)
# async def upsert_profile(body: FarmerProfileRequest, user=Depends(get_current_user), db=Depends(get_db)):
#     payload = {k: v for k, v in body.dict().items() if v is not None}
#     if not payload:
#         prof = await db[PROFILES_COLL].find_one({"user_id": user["email"]})
#         if not prof:
#             return FarmerProfileResponse()
#         return FarmerProfileResponse(
#             crops=prof.get("crops"),
#             soil_type=prof.get("soil_type"),
#             location_pref=prof.get("location_pref"),
#             irrigation_method=prof.get("irrigation_method"),
#             acreage=prof.get("acreage"),
#             custom_notes=prof.get("custom_notes"),
#         )
#     # upsert by user_id
#     payload["updated_at"] = datetime.utcnow()
#     await db[PROFILES_COLL].update_one(
#         {"user_id": user["email"]},
#         {"$set": payload, "$setOnInsert": {"user_id": user["email"]}},
#         upsert=True
#     )
#     prof = await db[PROFILES_COLL].find_one({"user_id": user["email"]})
#     return FarmerProfileResponse(
#         crops=prof.get("crops"),
#         soil_type=prof.get("soil_type"),
#         location_pref=prof.get("location_pref"),
#         irrigation_method=prof.get("irrigation_method"),
#         acreage=prof.get("acreage"),
#         custom_notes=prof.get("custom_notes"),
#     )

# # Q&A route
# @app.post("/answer")
# async def run_query(body: QuestionRequest, request: Request, db=Depends(get_db)):
#     # Optional auth parse
#     auth_header = request.headers.get("Authorization")
#     authed_email = None
#     if auth_header and auth_header.lower().startswith("bearer "):
#         token = auth_header.split(" ", 1)[1]
#         from auth import JWT_SECRET, JWT_ALG
#         import jwt
#         try:
#             payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
#             authed_email = payload.get("sub")
#             user = await db[USERS_COLL].find_one({"email": authed_email})
#             if not user:
#                 authed_email = None
#         except Exception:
#             authed_email = None

#     if not body.question or not body.question.strip():
#         raise HTTPException(status_code=400, detail="Question is required")

#     # Profile for authenticated user
#     farmer_profile = "None"
#     if authed_email:
#         prof = await db[PROFILES_COLL].find_one({"user_id": authed_email})
#         farmer_profile = serialize_profile(prof)

#     loc_str = ""
#     if body.location:
#         loc_str = f"User location: lat {body.location.get('lat')}, lon {body.location.get('lon')}"

#     # Session context handling
#     session_ctx_json = "{}"
#     session_id = body.session_id or request.headers.get("X-Session-Id")
#     if authed_email:
#         # Optional session even for logged-in
#         if session_id:
#             sc = await get_or_create_session_context(db, session_id)
#             session_ctx_json = json.dumps(sc.get("data") or {})
#     else:
#         if not session_id:
#             session_id = os.urandom(8).hex()
#         sc = await get_or_create_session_context(db, session_id)
#         session_ctx_json = json.dumps(sc.get("data") or {})

#     # Invoke RAG
#     response = await asyncio.to_thread(
#         rag_chain_default.invoke,
#         {
#             "input": body.question,
#             "farmer_profile": farmer_profile,
#             "session_context": session_ctx_json,
#             "location_info": loc_str
#         }
#     )

#     answer_text = response.get("answer") if isinstance(response, dict) else str(response)

#     # Parse SESSION_UPDATE JSON line to persist context
#     new_ctx = {}
#     try:
#         if isinstance(answer_text, str) and "SESSION_UPDATE:" in answer_text:
#             part = answer_text.split("SESSION_UPDATE:", 1)[1].strip()
#             block = part.split("\n", 1).strip()
#             new_ctx = json.loads(block)
#     except Exception:
#         new_ctx = {}

#     if session_id and new_ctx:
#         await update_session_context(db, session_id, new_ctx)

#     return JSONResponse(content={"answer": answer_text, "session_id": session_id})



# main.py
import os
import json
import asyncio
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from db_mongo import get_db, close_db
from models_mongo import USERS_COLL, PROFILES_COLL, SESSIONS_COLL, user_doc, profile_doc, session_context_doc
from schemas import SignupRequest, LoginRequest, TokenResponse, FarmerProfileRequest, FarmerProfileResponse, QuestionRequest
from auth import hash_password, verify_password, create_access_token, get_current_user

# LangChain / RAG
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
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()

# API Keys
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY or ""

# Pinecone + retriever
embeddings_default = download_hugging_face_embeddings()
index_name = "test"
if PINECONE_API_KEY:
    Pinecone(api_key=PINECONE_API_KEY)
docsearch_default = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings_default)
retriever_default = docsearch_default.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# LLM setup
llm_default = GoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4, max_tokens=500)
prompt_default = ChatPromptTemplate.from_messages([
    ("system", structured_system_prompt + "\n\n"
     "Use the provided farmer profile and session context when available.\n"
     "If critical details are missing (e.g., crop type, growth stage, soil), ask concise follow-up questions.\n"
     "If the user is authenticated, prefer profile defaults but confirm if outdated.\n"
     "Always state assumptions if proceeding without some details.\n"
     "If the user message provides missing details (e.g., 'tomato, 1 month, black soil'), acknowledge and continue.\n"
     "Always include a normal answer; optionally include a single-line JSON after 'SESSION_UPDATE:' to persist context."),
    ("human", "{input}\n\nFarmer Profile: {farmer_profile}\nSession Context: {session_context}\nAdditional Info: {location_info}")
])
qa_chain_default = create_stuff_documents_chain(llm_default, prompt_default)
rag_chain_default = create_retrieval_chain(retriever_default, qa_chain_default)

# Helpers
def serialize_profile(profile: Optional[dict]) -> str:
    if not profile:
        return "None"
    cleaned = {k: v for k, v in profile.items() if k not in ("_id", "user_id")}
    return json.dumps(cleaned, ensure_ascii=False)

async def get_or_create_session_context(db, session_id: str):
    sc = await db[SESSIONS_COLL].find_one({"session_id": session_id})
    if sc is None:
        sc = session_context_doc(session_id)
        await db[SESSIONS_COLL].insert_one(sc)
    return sc

async def update_session_context(db, session_id: str, updates: dict):
    await db[SESSIONS_COLL].update_one(
        {"session_id": session_id},
        {
            "$set": {f"data.{k}": v for k, v in updates.items()},
            "$setOnInsert": {"session_id": session_id},
            "$currentDate": {"updated_at": True},
        },
        upsert=True
    )

def extract_answer(resp) -> str:
    # Try common keys first
    if isinstance(resp, dict):
        for key in ["answer", "output_text", "result", "output"]:
            val = resp.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
        # Sometimes LC returns {"answer": "", "context": ...} but has 'generations' or 'text'
        for key in ["text", "message", "content"]:
            val = resp.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
    # Fallback to string conversion
    try:
        text = str(resp)
        if text and text.strip():
            return text.strip()
    except Exception:
        pass
    return ""

def safe_parse_session_update(answer_text: str) -> dict:
    """
    Extract a one-line JSON object following 'SESSION_UPDATE:' from the answer.
    Example in model output:
    ...normal text...
    SESSION_UPDATE: {"crop":"tomato","growth_stage":"flowering"}
    """
    if not isinstance(answer_text, str):
        return {}
    marker = "SESSION_UPDATE:"
    idx = answer_text.find(marker)
    if idx == -1:
        return {}
    after = answer_text[idx + len(marker):].lstrip()
    # Take until the first newline or end
    first_line = after.split("\n", 1)[0].strip()
    try:
        return json.loads(first_line)
    except Exception:
        return {}

# Auth routes
@app.post("/signup", response_model=TokenResponse)
async def signup(body: SignupRequest, db=Depends(get_db)):
    existing = await db[USERS_COLL].find_one({"email": body.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = user_doc(email=body.email, password_hash=hash_password(body.password), name=body.name)
    await db[USERS_COLL].insert_one(user)
    token = create_access_token(body.email)
    return TokenResponse(access_token=token)

@app.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db=Depends(get_db)):
    user = await db[USERS_COLL].find_one({"email": body.email})
    if not user or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user["email"])
    return TokenResponse(access_token=token)

# Profile routes
@app.get("/me", response_model=FarmerProfileResponse)
async def get_profile(user=Depends(get_current_user), db=Depends(get_db)):
    prof = await db[PROFILES_COLL].find_one({"user_id": user["email"]})
    if not prof:
        return FarmerProfileResponse()
    return FarmerProfileResponse(
        crops=prof.get("crops"),
        soil_type=prof.get("soil_type"),
        location_pref=prof.get("location_pref"),
        irrigation_method=prof.get("irrigation_method"),
        acreage=prof.get("acreage"),
        custom_notes=prof.get("custom_notes"),
    )

@app.post("/me", response_model=FarmerProfileResponse)
async def upsert_profile(body: FarmerProfileRequest, user=Depends(get_current_user), db=Depends(get_db)):
    payload = {k: v for k, v in body.dict().items() if v is not None}
    if not payload:
        prof = await db[PROFILES_COLL].find_one({"user_id": user["email"]})
        if not prof:
            return FarmerProfileResponse()
        return FarmerProfileResponse(
            crops=prof.get("crops"),
            soil_type=prof.get("soil_type"),
            location_pref=prof.get("location_pref"),
            irrigation_method=prof.get("irrigation_method"),
            acreage=prof.get("acreage"),
            custom_notes=prof.get("custom_notes"),
        )
    payload["updated_at"] = datetime.utcnow()
    await db[PROFILES_COLL].update_one(
        {"user_id": user["email"]},
        {"$set": payload, "$setOnInsert": {"user_id": user["email"]}},
        upsert=True
    )
    prof = await db[PROFILES_COLL].find_one({"user_id": user["email"]})
    return FarmerProfileResponse(
        crops=prof.get("crops"),
        soil_type=prof.get("soil_type"),
        location_pref=prof.get("location_pref"),
        irrigation_method=prof.get("irrigation_method"),
        acreage=prof.get("acreage"),
        custom_notes=prof.get("custom_notes"),
    )

# Q&A route
@app.post("/answer")
async def run_query(body: QuestionRequest, request: Request, db=Depends(get_db)):
    # Optional auth parse
    auth_header = request.headers.get("Authorization")
    authed_email = None
    if auth_header and auth_header.lower().startswith("bearer "):
        token = auth_header.split(" ", 1)[1]
        from auth import JWT_SECRET, JWT_ALG
        import jwt
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
            authed_email = payload.get("sub")
            user = await db[USERS_COLL].find_one({"email": authed_email})
            if not user:
                authed_email = None
        except Exception:
            authed_email = None

    if not body.question or not body.question.strip():
        raise HTTPException(status_code=400, detail="Question is required")

    # Profile for authenticated user
    farmer_profile = "None"
    if authed_email:
        prof = await db[PROFILES_COLL].find_one({"user_id": authed_email})
        farmer_profile = serialize_profile(prof)

    loc_str = ""
    if body.location:
        lat = body.location.get("lat")
        lon = body.location.get("lon")
        loc_str = f"User location: lat {lat}, lon {lon}"

    # Session context handling
    session_ctx_json = "{}"
    session_id = body.session_id or request.headers.get("X-Session-Id")
    if authed_email:
        if session_id:
            sc = await get_or_create_session_context(db, session_id)
            session_ctx_json = json.dumps(sc.get("data") or {})
    else:
        if not session_id:
            session_id = os.urandom(8).hex()
        sc = await get_or_create_session_context(db, session_id)
        session_ctx_json = json.dumps(sc.get("data") or {})

    # Invoke RAG with robust error handling and logging
    try:
        response = await asyncio.to_thread(
            rag_chain_default.invoke,
            {
                "input": body.question,
                "farmer_profile": farmer_profile,
                "session_context": session_ctx_json,
                "location_info": loc_str
            }
        )
        # Optional: uncomment for debugging
        # print("RAG raw response:", repr(response))
    except Exception as e:
        # Optional: log the error
        # print("RAG invoke error:", e)
        raise HTTPException(status_code=500, detail="LLM processing failed")

    answer_text = extract_answer(response)

    # Fallback if empty
    if not answer_text.strip():
        # If model may have emitted only SESSION_UPDATE, still return an acknowledgment
        session_data_candidate = safe_parse_session_update(str(response))
        if session_data_candidate:
            answer_text = "Noted. I’ve saved these details. How else can I help?"
        else:
            answer_text = (
                "I could not find specific references right now. "
                "I can still help with best-practice guidance. "
                "Please share crop, growth stage, soil type, and irrigation method if available."
            )

    # Parse SESSION_UPDATE JSON line to persist context
    new_ctx = safe_parse_session_update(answer_text)
    if not new_ctx:
        # Also try parsing from the raw response string in case answer_text was pruned
        new_ctx = safe_parse_session_update(str(response))

    if session_id and new_ctx:
        await update_session_context(db, session_id, new_ctx)

    return JSONResponse(content={"answer": answer_text, "session_id": session_id})
