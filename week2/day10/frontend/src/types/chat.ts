
export interface Message {
  role: "user" | "assistant";
  content: string;
}

export interface ChatRequest {
  message: string;
  session_id: string;
}

export interface ClearChatRequest {
  session_id: string;
}

export interface ChatResponse {
  answer: string;
}
