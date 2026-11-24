
import { useState, useRef, useEffect } from "react";
import type { Message, ChatRequest, ClearChatRequest } from "./types/chat";
import "./App.css";

const API_URL = "http://localhost:8000";

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hi! I'm CareerTwin. Ask me anything about Jaydeep's professional background, skills, projects or experience.",
    },
  ]);

  const [input, setInput] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Maintain session ID across browser refreshes
  const [sessionId] = useState<string>(() => {
    let id = localStorage.getItem("careertwin_session");

    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem("careertwin_session", id);
    }

    return id;
  });

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  const sendMessage = async (): Promise<void> => {
    const userMessage = input.trim();

    if (!userMessage || loading) return;

    setInput("");

    setMessages((prev) => [
      ...prev,
      { role: "user", content: userMessage },
      { role: "assistant", content: "" },
    ]);

    setLoading(true);

    try {
      const payload: ChatRequest = {
        message: userMessage,
        session_id: sessionId,
      };

      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Failed to communicate with CareerTwin.");
      }

      if (!response.body) {
        throw new Error("Streaming response is unavailable.");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let fullResponse = "";

      while (true) {
        const { done, value } = await reader.read();

        if (done) break;

        const chunk = decoder.decode(value, {
          stream: true,
        });

        fullResponse += chunk;

        setMessages((prev) => {
          const updated = [...prev];

          updated[updated.length - 1] = {
            role: "assistant",
            content: fullResponse,
          };

          return updated;
        });
      }

      // Flush any remaining decoder data
      fullResponse += decoder.decode();

      setMessages((prev) => {
        const updated = [...prev];

        updated[updated.length - 1] = {
          role: "assistant",
          content: fullResponse,
        };

        return updated;
      });
    } catch (error: unknown) {
      console.error("Chat error:", error);

      setMessages((prev) => {
        const updated = [...prev];

        updated[updated.length - 1] = {
          role: "assistant",
          content: "Sorry, something went wrong. Please try again.",
        };

        return updated;
      });
    } finally {
      setLoading(false);
    }
  };

  // Clear current conversation
  const clearChat = async (): Promise<void> => {
    if (loading) return;

    try {
      const payload: ClearChatRequest = {
        session_id: sessionId,
      };

      const response = await fetch(`${API_URL}/chat/clear`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Unable to clear server history.");
      }

      setMessages([
        {
          role: "assistant",
          content:
            "New conversation started! What would you like to know about Jaydeep?",
        },
      ]);
    } catch (error: unknown) {
      console.error("Clear chat error:", error);
    }
  };

  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLTextAreaElement>
  ): void => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      void sendMessage();
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">C</div>
          <span>CareerTwin</span>
        </div>

        <button className="new-chat-btn" onClick={() => void clearChat()}>
          + New Chat
        </button>

        <div className="sidebar-bottom">
          <span>AI Professional Assistant</span>
          <span className="version">Version 1.0</span>
        </div>
      </aside>

      {/* Main Chat */}
      <main className="chat-container">
        <header className="chat-header">
          <div>
            <h2>CareerTwin</h2>
            <p>Ask about Jaydeep's professional profile</p>
          </div>

          <div className="online-status">
            <span className="status-dot" />
            Online
          </div>
        </header>

        {/* Messages */}
        <section className="messages-container">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message-row ${message.role}`}
            >
              {message.role === "assistant" && (
                <div className="avatar">C</div>
              )}

              <div className="message-content">
                <div className="message-name">
                  {message.role === "user" ? "You" : "CareerTwin"}
                </div>

                <div className="message-bubble">
                  {message.content ||
                    (loading && index === messages.length - 1
                      ? "Thinking..."
                      : "")}
                </div>
              </div>

              {message.role === "user" && (
                <div className="user-avatar">Y</div>
              )}
            </div>
          ))}

          <div ref={messagesEndRef} />
        </section>

        {/* Input */}
        <footer className="input-section">
          <div className="input-wrapper">
            <textarea
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask me anything about Jaydeep..."
              rows={1}
              disabled={loading}
            />

            <button
              className="send-btn"
              onClick={() => void sendMessage()}
              disabled={!input.trim() || loading}
            >
              ↑
            </button>
          </div>

          <p className="input-note">
            CareerTwin can make mistakes. Verify important information.
          </p>
        </footer>
      </main>
    </div>
  );
}

export default App;