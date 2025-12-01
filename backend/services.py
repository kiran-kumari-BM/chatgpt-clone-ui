from typing import List, Optional
import os

import openai  # pip install openai
from models import UploadedFileInfo  # note: no leading dot


# Read key from env: export OPENAI_API_KEY="sk-..."
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_answer(
    prompt: str,
    files: List[UploadedFileInfo],
    conversation_id: Optional[str] = None,
) -> str:
    """
    Generate an answer using OpenAI GPT model.
    You can customize the prompt to include file metadata.
    """

    if not openai.api_key:
        # Fallback if no API key is set – do NOT crash the server
        file_summary = ""
        if files:
            file_lines = [
                f"- {f.filename} ({f.content_type}, {f.size} bytes)" for f in files
            ]
            file_summary = "\n\nYou also sent these files:\n" + "\n".join(file_lines)

        return (
            f"OPENAI_API_KEY is not set.\n\n"
            f'I received your prompt:\n"{prompt}"\n'
            f"Conversation ID: {conversation_id or 'none'}"
            f"{file_summary}\n\n"
            "Set OPENAI_API_KEY in your environment to get real AI responses."
        )

    # Build extra context about uploaded files
    file_context = ""
    if files:
        file_lines = [
            f"- {f.filename} ({f.content_type}, {f.size} bytes)" for f in files
        ]
        file_context = (
            "\n\nThe user also uploaded these files (metadata only):\n"
            + "\n".join(file_lines)
        )

    user_content = prompt + file_context

    # Call OpenAI ChatCompletion
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. If file metadata is provided, use it for context.",
            },
            {"role": "user", "content": user_content},
        ],
    )

    # Extract the answer text
    return response["choices"][0]["message"]["content"]
