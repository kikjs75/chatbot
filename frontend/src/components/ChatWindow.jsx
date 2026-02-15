import React, { useState, useCallback } from "react";
import ConversationList from "./ConversationList";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";
import { sendMessage, getConversation, getConversations } from "../services/api";

function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const [conversations, setConversations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = useCallback(
    async (text) => {
      const userMsg = {
        role: "user",
        content: text,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, userMsg]);
      setIsLoading(true);

      try {
        const data = await sendMessage(text, conversationId);
        setConversationId(data.conversation_id);
        setMessages((prev) => [...prev, data.bot_message]);

        // 대화 목록 갱신
        try {
          const convs = await getConversations();
          setConversations(convs);
        } catch {
          // 목록 갱신 실패는 무시
        }
      } catch (error) {
        setMessages((prev) => [
          ...prev,
          {
            role: "bot",
            content: "서버 연결에 실패했습니다. 잠시 후 다시 시도해주세요.",
            timestamp: new Date().toISOString(),
          },
        ]);
      } finally {
        setIsLoading(false);
      }
    },
    [conversationId]
  );

  const handleNewConversation = useCallback(() => {
    setMessages([]);
    setConversationId(null);
  }, []);

  const handleSelectConversation = useCallback(async (id) => {
    try {
      const conv = await getConversation(id);
      setConversationId(conv.conversation_id);
      setMessages(conv.messages || []);
    } catch {
      // 조회 실패 시 무시
    }
  }, []);

  return (
    <div className="chat-window">
      <ConversationList
        conversations={conversations}
        activeId={conversationId}
        onSelect={handleSelectConversation}
        onNew={handleNewConversation}
      />
      <div className="chat-area">
        <div className="chat-area__header">
          <h3>고객 상담 챗봇</h3>
        </div>
        <MessageList messages={messages} isLoading={isLoading} />
        <MessageInput onSend={handleSend} disabled={isLoading} />
      </div>
    </div>
  );
}

export default ChatWindow;
