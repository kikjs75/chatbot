import React from "react";

function formatDate(dateStr) {
  if (!dateStr) return "";
  const date = new Date(dateStr);
  return date.toLocaleDateString("ko-KR", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function ConversationList({ conversations, activeId, onSelect, onNew }) {
  return (
    <div className="conversation-list">
      <div className="conversation-list__header">
        <h2>대화 목록</h2>
        <button className="conversation-list__new-btn" onClick={onNew}>
          + 새 대화
        </button>
      </div>
      <div className="conversation-list__items">
        {conversations.length === 0 ? (
          <div className="conversation-list__empty">
            대화 이력이 없습니다.
            <br />
            새 대화를 시작해보세요!
          </div>
        ) : (
          conversations.map((conv) => (
            <div
              key={conv.conversation_id}
              className={`conversation-list__item ${
                conv.conversation_id === activeId
                  ? "conversation-list__item--active"
                  : ""
              }`}
              onClick={() => onSelect(conv.conversation_id)}
            >
              <div className="conversation-list__item-title">
                대화 #{conv.conversation_id.slice(0, 8)}
              </div>
              <div className="conversation-list__item-date">
                {formatDate(conv.updated_at)}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default ConversationList;
