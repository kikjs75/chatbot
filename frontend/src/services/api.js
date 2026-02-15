import axios from "axios";

const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:3000/dev";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

export async function sendMessage(message, conversationId = null) {
  const payload = { message };
  if (conversationId) {
    payload.conversation_id = conversationId;
  }
  const response = await api.post("/chat", payload);
  return response.data;
}

export async function getConversations() {
  const response = await api.get("/conversations");
  return response.data.conversations;
}

export async function getConversation(id) {
  const response = await api.get(`/conversations/${id}`);
  return response.data.conversation;
}

export async function checkHealth() {
  const response = await api.get("/health");
  return response.data;
}
