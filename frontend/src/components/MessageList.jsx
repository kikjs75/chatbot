import React, { useEffect, useRef } from "react";

function formatTime(timestamp) {
  if (!timestamp) return "";
  const date = new Date(timestamp);
  return date.toLocaleTimeString("ko-KR", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

function MessageList({ messages, isLoading }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="message-list">
        <div className="message-list__welcome">
          안녕하세요! 고객 상담 챗봇입니다.
          <br />
          배송, 반품, 교환, 결제 등 궁금한 점을 물어보세요.
        </div>
      </div>
    );
  }

  return (
    <div className="message-list">
      {messages.map((msg, idx) => (
        <div key={idx} className={`message message--${msg.role}`}>
          <div className="message__bubble">{msg.content}</div>
          <span className="message__time">{formatTime(msg.timestamp)}</span>
        </div>
      ))}
      {isLoading && (
        <div className="message message--bot">
          <div className="message__bubble message__typing">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  );
}

export default MessageList;
