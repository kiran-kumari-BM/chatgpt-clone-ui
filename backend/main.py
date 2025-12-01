from typing import List, Optional

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

# ✅ Use absolute imports (same folder)
from models import UploadedFileInfo, ChatResponse
from services import generate_answer

app = FastAPI(title="ChatGPT Clone Backend", version="1.0.0")

# Adjust these to your actual frontend origin
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(
    prompt: str = Form(...),
    conversationId: Optional[str] = Form(None),
    files: List[UploadFile] = File(default_factory=list),
):
    """
    Handles chat requests with optional file uploads.
    Frontend sends multipart/form-data with:
    - prompt (string)
    - conversationId (string | null)
    - files[] (one or more files)
    """

    uploaded_files: List[UploadedFileInfo] = []

    for file in files:
        contents = await file.read()
        uploaded_files.append(
            UploadedFileInfo(
                filename=file.filename,
                content_type=file.content_type or "application/octet-stream",
                size=len(contents),
            )
        )

    answer = generate_answer(
        prompt=prompt,
        files=uploaded_files,
        conversation_id=conversationId,
    )

    return ChatResponse(answer=answer)


# Optional: run directly with `python main.py`
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
