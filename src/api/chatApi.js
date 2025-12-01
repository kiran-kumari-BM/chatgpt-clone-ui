// src/api/chatApi.js

// URL of your FastAPI backend
const API_BASE_URL = "http://localhost:8000";

export async function sendMessageToBackend(prompt, files, conversationId) {
  const formData = new FormData();
  formData.append("prompt", prompt || "");
  if (conversationId) {
    formData.append("conversationId", conversationId);
  }

  (files || []).forEach((file) => {
    formData.append("files", file);
  });

  const res = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Backend error: ${res.status} - ${text}`);
  }

  const data = await res.json();
  // FastAPI returns: { "answer": "..." }
  return data.answer;
}
