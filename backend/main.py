from dotenv import load_dotenv
load_dotenv() # MUST BE AT THE VERY TOP

import os
os.makedirs("uploads", exist_ok=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.upload import router as upload_router
from api.process import router as process_router
from api.extract import router as extract_router
from api.decision import router as decision_router
from api.copilot import router as copilot_router
from api.approvals import router as approvals_router # <-- ADDED

app = FastAPI(title="AI Manufacturing Decision Copilot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(process_router)
app.include_router(extract_router)
app.include_router(decision_router)
app.include_router(copilot_router)
app.include_router(approvals_router) # <-- ADDED

@app.get("/health")
def health_check():
    return {"status": "healthy"}