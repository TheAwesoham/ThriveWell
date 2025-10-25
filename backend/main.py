from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend import journal  

app = FastAPI(title="Mental Health App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(journal.router, prefix="/journal", tags=["Journal"])

@app.get("/")
def root():
    return {"message": "Mental Health App Backend is running 🚀"}