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
from services.agent_service import create_agent_prompt, extract_api_calls, execute_api_calls, format_api_results_for_llm,remove_internal_lines
from services.dynamic_api_tool import dynamic_api_call
from schemas import AgentQuestionRequest  # Add to your existing schema imports



# LangChain / RAG
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from src.prompt import structured_system_prompt
from src.helper import download_hugging_face_embeddings
from langchain_openai import ChatOpenAI

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
llm_default = GoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1, max_tokens=800)
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
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm_router = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4o-mini")
# llm_router = ChatOpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=OPENROUTER_API_KEY,
#     model="qwen/qwen-2.5-72b-instruct:free"
# )
qa_chain_default = create_stuff_documents_chain(llm_router, prompt_default)
rag_chain_default = create_retrieval_chain(retriever_default, qa_chain_default)


# Add this new agent-enhanced LLM setup (after your existing LLM setup)
agent_prompt_default = ChatPromptTemplate.from_messages([
    ("system", create_agent_prompt(structured_system_prompt) + "\n\n"
     "Use the provided farmer profile and session context when available.\n"
     "If you need real-time data (weather, prices, soil info), use API_CALL format.\n"
     "After getting API results, provide a comprehensive answer combining real-time data with your knowledge.\n"
     "Always state data sources and timestamps in your final response.\n"
     "Always include a normal answer; optionally include SESSION_UPDATE for context persistence."),
    ("human", "{input}\n\nFarmer Profile: {farmer_profile}\nSession Context: {session_context}\nAdditional Info: {location_info}\n{api_results}")
])

agent_qa_chain = create_stuff_documents_chain(llm_router, agent_prompt_default)
agent_rag_chain = create_retrieval_chain(retriever_default, agent_qa_chain)

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
def serialize_profile(profile: Optional[dict]) -> str:
    if not profile:
        return "None"
    cleaned = {
        k: v
        for k, v in profile.items()
        if k not in ("_id", "user_id", "updated_at", "created_at")
    }
    return json.dumps(cleaned, ensure_ascii=False)
def extract_answer(resp) -> str:
    """Extract the actual LLM response from LangChain output"""
    
    if isinstance(resp, dict):
        # LangChain retrieval chain returns answer in 'answer' key
        if 'answer' in resp:
            answer = resp['answer']
            if isinstance(answer, str) and answer.strip():
                return answer.strip()
            elif answer == "":
                return "I couldn't find a specific answer. Please provide more details about your crops and location."
        
        # Try other possible keys
        for key in ["output_text", "result", "text", "content"]:
            if key in resp and isinstance(resp[key], str) and resp[key].strip():
                return resp[key].strip()
    
    # If we get here, something is wrong
    return "I'm having trouble processing your question. Please try again."

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

# main.py - ADD THIS FUNCTION FIRST

async def classify_intent_with_llm(question: str, user_location: dict = None) -> str:
    """Use LLM to classify user intent as 'rag' or 'agent'"""
    
    location_context = ""
    if user_location and user_location.get('lat') and user_location.get('lon'):
        location_context = f"User has location: lat {user_location['lat']}, lon {user_location['lon']}"
    else:
        location_context = "No location provided"
    
    classification_prompt = f"""
Classify this agricultural question as either 'rag' or 'agent':

- 'rag': Question can be answered with general agricultural knowledge/best practices
- 'agent': Question needs real-time data (weather, market prices, current conditions)

Question: "{question}"
{location_context}

Examples:
"What are symptoms of nitrogen deficiency?" → rag
"Should I water my crops today?" → agent  
"How to prepare soil for planting?" → rag
"Will it rain tomorrow?" → agent
"Benefits of crop rotation" → rag
"Current wheat prices" → agent
"When should I harvest?" → agent
"Types of fertilizers" → rag

Respond with only: rag OR agent
"""

    try:
        response = await asyncio.to_thread(
            llm_default.invoke,
            classification_prompt
        )
        
        intent = response.strip().lower()
        if intent in ['rag', 'agent']:
            return intent
        else:
            # Fallback if LLM gives unexpected response
            print(f"⚠️ Unexpected LLM classification response: {response}")
            return 'rag'
            
    except Exception as e:
        print(f"❌ Intent classification failed: {e}")
        # Fallback to RAG mode if classification fails
        return 'rag'

# main.py - ADD THIS UNIFIED ENDPOINT


@app.post("/ask")
async def unified_agricultural_assistant(body: QuestionRequest, request: Request, db=Depends(get_db)):
    """Unified endpoint that uses LLM to classify intent and route appropriately"""
    print(f"🧠 UNIFIED ASK ENDPOINT CALLED")
    print(f"📝 Question: {body.question}")
    
    # Auth logic (same as both your routes)
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

    # Profile logic (same as both routes)
    farmer_profile = "None"
    if authed_email:
        prof = await db[PROFILES_COLL].find_one({"user_id": authed_email})
        farmer_profile = serialize_profile(prof)
        print("Farmer profile for user:", authed_email, "->", farmer_profile)

    # Location processing (combined from both routes)
    loc_str = ""
    user_location = {}
    if body.location:
        lat = body.location.get("lat")
        lon = body.location.get("lon")
        if lat and lon:
            loc_str = f"User location: lat {lat}, lon {lon}"
            user_location = {"lat": lat, "lon": lon}
            print(f"📍 Location found: {user_location}")
        else:
            loc_str = f"User location: {json.dumps(body.location)}"
            print(f"📍 Location (partial): {loc_str}")
    else:
        print("📍 No location provided")

    # Session context handling (same as both routes)
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

    print(f"🎯 Session ID: {session_id}")

    # LLM-BASED INTENT CLASSIFICATION
    print("🤖 Classifying intent with LLM...")
    intent = await classify_intent_with_llm(body.question, user_location)
    print(f"🎯 LLM CLASSIFIED INTENT: {intent.upper()}")
    
    try:
        if intent == 'agent':
            print(f"🤖 EXECUTING: Agent mode (real-time data needed)")
            
            # AGENT MODE LOGIC (from your agent route)
            print("🔄 Step 1: Getting initial LLM response...")
            initial_response = await asyncio.to_thread(
                agent_rag_chain.invoke,
                {
                    "input": body.question,
                    "farmer_profile": farmer_profile,
                    "session_context": session_ctx_json,
                    "location_info": loc_str,
                    "api_results": ""
                }
            )

            initial_answer = extract_answer(initial_response)
            print(f"🔍 Initial LLM response: {initial_answer[:200]}...")

            # Step 2: Extract API calls
            api_calls = extract_api_calls(initial_answer)
            print(f"📞 API calls requested: {len(api_calls)}")
            for i, call in enumerate(api_calls):
                print(f"  API {i+1}: {call.get('description', 'No description')}")
                print(f"  URL: {call.get('url', 'No URL')[:100]}...")

            if api_calls:
                print("🔧 Processing and validating API calls...")
                from services.agent_service import validate_and_fix_api_calls
                valid_calls = validate_and_fix_api_calls(api_calls, user_location)

                if valid_calls:
                    print(f"🚀 Executing {len(valid_calls)} valid API calls...")
                    api_results = execute_api_calls(valid_calls)
                    print(f"✅ API calls executed. Sources: {api_results.get('sources', [])}")

                    # Step 3: Get final response with API data
                    print("🔄 Step 3: Getting final LLM response with API data...")
                    final_response = await asyncio.to_thread(
                        agent_rag_chain.invoke,
                        {
                            "input": body.question,
                            "farmer_profile": farmer_profile,
                            "session_context": session_ctx_json,
                            "location_info": loc_str,
                            "api_results": format_api_results_for_llm(api_results)
                        }
                    )
                    answer_text = extract_answer(final_response)
                    sources = api_results.get("sources", [])
                    print(f"🎯 Final answer with API data: {answer_text[:200]}...")
                else:
                    print("❌ No valid API calls could be generated or fixed")
                    answer_text = initial_answer
                    sources = []
            else:
                print("⚠️ No API calls were made by the LLM")
                answer_text = initial_answer
                sources = []
            
            # Prepare agent response
            response_data = {
                "answer": answer_text,
                "session_id": session_id,
                "intent": "agent",
                "reasoning": "LLM determined real-time data needed"
            }
            if sources:
                response_data["sources"] = sources
                response_data["agent_mode"] = True

        else:  # intent == 'rag'
            print(f"📚 EXECUTING: RAG mode (knowledge base sufficient)")
            
            # RAG MODE LOGIC (from your answer route)
            response = await asyncio.to_thread(
                rag_chain_default.invoke,
                {
                    "input": body.question,
                    "farmer_profile": farmer_profile,
                    "session_context": session_ctx_json,
                    "location_info": loc_str
                }
            )

            answer_text = extract_answer(response)
            
            # Prepare RAG response
            response_data = {
                "answer": answer_text,
                "session_id": session_id,
                "intent": "rag",
                "reasoning": "LLM determined knowledge base sufficient"
            }

    except Exception as e:
        print(f"❌ LLM processing error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"LLM processing failed: {str(e)}")

    # Fallback logic (same as both routes)
    if not response_data["answer"].strip():
        print("⚠️ Empty answer, using fallback")
        response_data["answer"] = (
            "I could not find specific references right now. "
            "I can still help with best-practice guidance. "
            "Please share crop, growth stage, soil type, and irrigation method if available."
        )

    # Session update logic (same as both routes)
    new_ctx = safe_parse_session_update(response_data["answer"])
    if not new_ctx and 'response' in locals():
        new_ctx = safe_parse_session_update(str(response))

    if session_id and new_ctx:
        await update_session_context(db, session_id, new_ctx)

    print(f"✅ UNIFIED RESPONSE ({intent.upper()}): {json.dumps(response_data, indent=2)}")
    return JSONResponse(content=response_data)


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
        print("Farmer profile for user:", authed_email, "->", farmer_profile)

    loc_str = ""
    if body.location:
        lat = body.location.get("lat")
        lon = body.location.get("lon")
        loc_str = f"User location: lat {lat}, lon {lon}"
        print("User location string:", loc_str)

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



@app.post("/agent")
async def run_agent_query(body: AgentQuestionRequest, request: Request, db=Depends(get_db)):
    print(f"🚀 AGENT ENDPOINT CALLED")
    print(f"📝 Request body: {body}")
    
    # (User authentication, profile, location processing as in your original code)
    # ...
    session_ctx_json = "{}"
    session_id = body.session_id or request.headers.get("X-Session-Id")
    authed_email = None
    # ... (auth code omitted for brevity)
    farmer_profile = "None"
    # ... (profile retrieval code omitted)
    loc_str = ""
    user_location = {}
    if body.location:
        lat = body.location.get("lat")
        lon = body.location.get("lon")
        if lat and lon:
            loc_str = f"User location: lat {lat}, lon {lon}"
            user_location = {"lat": lat, "lon": lon}
            print(f"📍 Location found: {user_location}")
        elif body.location:
            loc_str = f"User location: {json.dumps(body.location)}"
            print(f"📍 Location (no lat/lon): {loc_str}")
    else:
        print("📍 No location provided")

    print(f"🎯 Session ID: {session_id}")

    try:
        if body.enable_agent:
            print(f"🤖 AGENT MODE: Processing question: {body.question}")
            print(f"📍 Location: {user_location}")

            # Step 1: Get initial response with potential API calls
            print("🔄 Step 1: Getting initial LLM response...")
            initial_response = await asyncio.to_thread(
                agent_rag_chain.invoke,
                {
                    "input": body.question,
                    "farmer_profile": farmer_profile,
                    "session_context": session_ctx_json,
                    "location_info": loc_str,
                    "api_results": ""
                }
            )

            initial_answer = extract_answer(initial_response)
            print(f"🔍 Initial LLM response: {initial_answer[:200]}...")

            # Step 2: Extract API calls
            api_calls = extract_api_calls(initial_answer)
            print(f"📞 API calls requested: {len(api_calls)}")
            for i, call in enumerate(api_calls):
                print(f"  API {i+1}: {call.get('description', 'No description')}")
                print(f"  URL: {call.get('url', 'No URL')[:100]}...")

            if api_calls:
                print("🔧 Processing and validating API calls...")
                from services.agent_service import validate_and_fix_api_calls
                valid_calls = validate_and_fix_api_calls(api_calls, user_location)

                if valid_calls:
                    print(f"🚀 Executing {len(valid_calls)} valid API calls...")
                    api_results = execute_api_calls(valid_calls)
                    print(f"✅ API calls executed. Sources: {api_results.get('sources', [])}")

                    # Step 3: Get final response with API data
                    print("🔄 Step 3: Getting final LLM response with API data...")
                    final_response = await asyncio.to_thread(
                        agent_rag_chain.invoke,
                        {
                            "input": body.question,
                            "farmer_profile": farmer_profile,
                            "session_context": session_ctx_json,
                            "location_info": loc_str,
                            "api_results": format_api_results_for_llm(api_results)
                        }
                    )
                    answer_text = extract_answer(final_response)
                    answer_text = remove_internal_lines(answer_text)
                    sources = api_results.get("sources", [])
                    print(f"🎯 Final answer with API data: {answer_text[:200]}...")
                else:
                    print("❌ No valid API calls could be generated or fixed")
                    answer_text = initial_answer
                    sources = []
            else:
                print("⚠️ No API calls were made by the LLM")
                answer_text = initial_answer
                sources = []
        else:
            # Regular RAG mode
            print("📚 REGULAR RAG MODE")
            response = await asyncio.to_thread(
                rag_chain_default.invoke,
                {
                    "input": body.question,
                    "farmer_profile": farmer_profile,
                    "session_context": session_ctx_json,
                    "location_info": loc_str
                }
            )
            answer_text = extract_answer(response)
            sources = []

    except Exception as e:
        print(f"❌ LLM processing error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"LLM processing failed: {str(e)}")

    # Fallback logic (unchanged)
    if not answer_text.strip():
        print("⚠️ Empty answer, using fallback")
        answer_text = (
            "I could not find specific references right now. "
            "I can still help with best-practice guidance."
            "Please share crop, growth stage, soil type, and irrigation method if available."
        )

    # Session update logic (unchanged)
    new_ctx = safe_parse_session_update(answer_text)
    if session_id and new_ctx:
        await update_session_context(db, session_id, new_ctx)

    # Prepare agent response
    response_data = {
        "answer": answer_text,
        "session_id": session_id
    }
    if body.enable_agent and sources:
        response_data["sources"] = sources
        response_data["agent_mode"] = True

    print(f"✅ AGENT RESPONSE: {json.dumps(response_data, indent=2)}")
    return JSONResponse(content=response_data)





# # Add new agent endpoint
# @app.post("/agent")
# async def run_agent_query(body: AgentQuestionRequest, request: Request, db=Depends(get_db)):
#     # Reuse your existing auth logic
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

#     # Reuse your existing profile logic
#     farmer_profile = "None"
#     if authed_email:
#         prof = await db[PROFILES_COLL].find_one({"user_id": authed_email})
#         farmer_profile = serialize_profile(prof)

#     # Enhanced location string with lat/lon for APIs
#     loc_str = ""
#     user_location = {}
#     if body.location:
#         lat = body.location.get("lat")
#         lon = body.location.get("lon")
#         if lat and lon:
#             loc_str = f"User location: lat {lat}, lon {lon}"
#             user_location = {"lat": lat, "lon": lon}
#         elif body.location:
#             loc_str = f"User location: {json.dumps(body.location)}"

#     # Reuse your existing session context logic
#     session_ctx_json = "{}"
#     session_id = body.session_id or request.headers.get("X-Session-Id")
#     if authed_email:
#         if session_id:
#             sc = await get_or_create_session_context(db, session_id)
#             session_ctx_json = json.dumps(sc.get("data") or {})
#     else:
#         if not session_id:
#             session_id = os.urandom(8).hex()
#         sc = await get_or_create_session_context(db, session_id)
#         session_ctx_json = json.dumps(sc.get("data") or {})

#     try:
#         if body.enable_agent:
#             # AGENT MODE: Two-step process
            
#             # Step 1: Get initial response with potential API calls
#             initial_response = await asyncio.to_thread(
#                 agent_rag_chain.invoke,
#                 {
#                     "input": body.question,
#                     "farmer_profile": farmer_profile,
#                     "session_context": session_ctx_json,
#                     "location_info": loc_str,
#                     "api_results": ""
#                 }
#             )
            
#             initial_answer = extract_answer(initial_response)
            
#             # Step 2: Check if LLM wants to make API calls
#             api_calls = extract_api_calls(initial_answer)
            
#             if api_calls:
#                 # Fill in location data for API calls that need it
#                 for call in api_calls:
#                     url = call.get('url', '')
#                     if '{lat}' in url and '{lon}' in url and user_location:
#                         call['url'] = url.format(lat=user_location['lat'], lon=user_location['lon'])
#                     elif '{lat}' in url or '{lon}' in url:
#                         # Skip API calls that need location but don't have it
#                         call['url'] = ''
                
#                 # Execute API calls
#                 api_results = execute_api_calls([c for c in api_calls if c.get('url')])
                
#                 # Step 3: Get final response with API data
#                 final_response = await asyncio.to_thread(
#                     agent_rag_chain.invoke,
#                     {
#                         "input": body.question,
#                         "farmer_profile": farmer_profile,
#                         "session_context": session_ctx_json,
#                         "location_info": loc_str,
#                         "api_results": format_api_results_for_llm(api_results)
#                     }
#                 )
                
#                 answer_text = extract_answer(final_response)
#                 sources = api_results.get("sources", [])
                
#             else:
#                 # No API calls needed, use initial response
#                 answer_text = initial_answer
#                 sources = []
            
#         else:
#             # REGULAR RAG MODE (your existing logic)
#             response = await asyncio.to_thread(
#                 rag_chain_default.invoke,
#                 {
#                     "input": body.question,
#                     "farmer_profile": farmer_profile,
#                     "session_context": session_ctx_json,
#                     "location_info": loc_str
#                 }
#             )
#             answer_text = extract_answer(response)
#             sources = []

#     except Exception as e:
#         raise HTTPException(status_code=500, detail="LLM processing failed")

#     # Reuse your existing fallback and session update logic
#     if not answer_text.strip():
#         session_data_candidate = safe_parse_session_update(str(response))
#         if session_data_candidate:
#             answer_text = "Noted. I've saved these details. How else can I help?"
#         else:
#             answer_text = (
#                 "I could not find specific references right now. "
#                 "I can still help with best-practice guidance. "
#                 "Please share crop, growth stage, soil type, and irrigation method if available."
#             )

#     # Parse SESSION_UPDATE for context persistence
#     new_ctx = safe_parse_session_update(answer_text)
#     if not new_ctx and 'response' in locals():
#         new_ctx = safe_parse_session_update(str(response))

#     if session_id and new_ctx:
#         await update_session_context(db, session_id, new_ctx)

#     response_data = {
#         "answer": answer_text, 
#         "session_id": session_id
#     }
    
#     if body.enable_agent and sources:
#         response_data["sources"] = sources
#         response_data["agent_mode"] = True

#     return JSONResponse(content=response_data)
# main.py - Enhanced with full debug logging
# @app.post("/agent")
# async def run_agent_query(body: AgentQuestionRequest, request: Request, db=Depends(get_db)):
#     print(f"🚀 AGENT ENDPOINT CALLED")
#     print(f"📝 Request body: {body}")
    
#     # Existing auth logic
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
#         except Exception as e:
#             print(f"🔐 Auth error: {e}")
#             authed_email = None

#     if not body.question or not body.question.strip():
#         print("❌ ERROR: Empty question")
#         raise HTTPException(status_code=400, detail="Question is required")

#     # Profile logic
#     farmer_profile = "None"
#     if authed_email:
#         prof = await db[PROFILES_COLL].find_one({"user_id": authed_email})
#         farmer_profile = serialize_profile(prof)
#         print(f"👤 User profile: {farmer_profile}")

#     # Location processing
#     loc_str = ""
#     user_location = {}
#     if body.location:
#         lat = body.location.get("lat")
#         lon = body.location.get("lon")
#         if lat and lon:
#             loc_str = f"User location: lat {lat}, lon {lon}"
#             user_location = {"lat": lat, "lon": lon}
#             print(f"📍 Location found: {user_location}")
#         elif body.location:
#             loc_str = f"User location: {json.dumps(body.location)}"
#             print(f"📍 Location (no lat/lon): {loc_str}")
#     else:
#         print("📍 No location provided")

#     # Session context logic
#     session_ctx_json = "{}"
#     session_id = body.session_id or request.headers.get("X-Session-Id")
#     if authed_email:
#         if session_id:
#             sc = await get_or_create_session_context(db, session_id)
#             session_ctx_json = json.dumps(sc.get("data") or {})
#     else:
#         if not session_id:
#             session_id = os.urandom(8).hex()
#         sc = await get_or_create_session_context(db, session_id)
#         session_ctx_json = json.dumps(sc.get("data") or {})

#     print(f"🎯 Session ID: {session_id}")

#     try:
#         if body.enable_agent:
#             print(f"🤖 AGENT MODE: Processing question: {body.question}")
#             print(f"📍 Location: {user_location}")
            
#             # Step 1: Get initial response with potential API calls
#             print("🔄 Step 1: Getting initial LLM response...")
#             initial_response = await asyncio.to_thread(
#                 agent_rag_chain.invoke,
#                 {
#                     "input": body.question,
#                     "farmer_profile": farmer_profile,
#                     "session_context": session_ctx_json,
#                     "location_info": loc_str,
#                     "api_results": ""
#                 }
#             )
            
#             initial_answer = extract_answer(initial_response)
#             print(f"🔍 Initial LLM response: {initial_answer[:200]}...")
            
#             # Step 2: Check if LLM wants to make API calls
#             api_calls = extract_api_calls(initial_answer)
#             print(f"📞 API calls requested: {len(api_calls)}")
#             for i, call in enumerate(api_calls):
#                 print(f"  API {i+1}: {call.get('description', 'No description')}")
#                 print(f"  URL: {call.get('url', 'No URL')[:100]}...")
            
#             if api_calls:
#                 print("🔧 Processing API calls...")
#                 # Fill in location data for API calls that need it
#                 for call in api_calls:
#                     url = call.get('url', '')
#                     if '{lat}' in url and '{lon}' in url and user_location:
#                         call['url'] = url.format(lat=user_location['lat'], lon=user_location['lon'])
#                         print(f"✅ Filled location in URL: {call['url'][:100]}...")
#                     elif '{lat}' in url or '{lon}' in url:
#                         print(f"⚠️ Skipping API call - needs location but none provided")
#                         call['url'] = ''
                
#                 # Execute API calls
#                 valid_calls = [c for c in api_calls if c.get('url')]
#                 print(f"🚀 Executing {len(valid_calls)} valid API calls...")
#                 api_results = execute_api_calls(valid_calls)
#                 print(f"✅ API calls executed. Sources: {api_results.get('sources', [])}")
                
#                 # Step 3: Get final response with API data
#                 print("🔄 Step 3: Getting final LLM response with API data...")
#                 final_response = await asyncio.to_thread(
#                     agent_rag_chain.invoke,
#                     {
#                         "input": body.question,
#                         "farmer_profile": farmer_profile,
#                         "session_context": session_ctx_json,
#                         "location_info": loc_str,
#                         "api_results": format_api_results_for_llm(api_results)
#                     }
#                 )
                
#                 answer_text = extract_answer(final_response)
#                 sources = api_results.get("sources", [])
#                 print(f"🎯 Final answer with API data: {answer_text[:200]}...")
                
#             else:
#                 print("⚠️ No API calls were made by the LLM")
#                 answer_text = initial_answer
#                 sources = []
            
#         else:
#             print("📚 REGULAR RAG MODE")
#             # Regular RAG mode
#             response = await asyncio.to_thread(
#                 rag_chain_default.invoke,
#                 {
#                     "input": body.question,
#                     "farmer_profile": farmer_profile,
#                     "session_context": session_ctx_json,
#                     "location_info": loc_str
#                 }
#             )
#             answer_text = extract_answer(response)
#             sources = []

#     except Exception as e:
#         print(f"❌ LLM processing error: {str(e)}")
#         print(f"❌ Error type: {type(e).__name__}")
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=f"LLM processing failed: {str(e)}")

#     # Fallback logic
#     if not answer_text.strip():
#         print("⚠️ Empty answer, using fallback")
#         if 'response' in locals():
#             session_data_candidate = safe_parse_session_update(str(response))
#         else:
#             session_data_candidate = {}
            
#         if session_data_candidate:
#             answer_text = "Noted. I've saved these details. How else can I help?"
#         else:
#             answer_text = (
#                 "I could not find specific references right now. "
#                 "I can still help with best-practice guidance. "
#                 "Please share crop, growth stage, soil type, and irrigation method if available."
#             )

#     # Session update logic
#     new_ctx = safe_parse_session_update(answer_text)
#     if not new_ctx and 'response' in locals():
#         new_ctx = safe_parse_session_update(str(response))

#     if session_id and new_ctx:
#         await update_session_context(db, session_id, new_ctx)

#     # Prepare response
#     response_data = {
#         "answer": answer_text, 
#         "session_id": session_id
#     }
    
#     if body.enable_agent and 'sources' in locals() and sources:
#         response_data["sources"] = sources
#         response_data["agent_mode"] = True

#     print(f"✅ AGENT RESPONSE: {json.dumps(response_data, indent=2)}")
#     return JSONResponse(content=response_data)



