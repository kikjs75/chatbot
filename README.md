# 고객 상담 챗봇 (Customer Service Chatbot)

AWS Lambda 기반 서버리스 고객 상담 챗봇 프로젝트.
규칙 기반 상담 엔진으로 배송, 반품, 교환, 결제 등의 고객 문의를 자동 처리하며, DynamoDB에 대화 이력을 저장한다.

## 아키텍처

```
[React SPA] → [API Gateway (REST)] → [Lambda Functions] → [DynamoDB]
     ↑
  S3 + CloudFront (정적 호스팅)
```

- **백엔드**: Python 3.11 + AWS Lambda + Serverless Framework
- **프론트엔드**: React 18
- **데이터베이스**: DynamoDB (PAY_PER_REQUEST)
- **API**: REST API Gateway (CORS 지원)

## 프로젝트 구조

```
chatbot/
├── serverless.yml                  # Serverless Framework 설정
├── requirements.txt                # Python 의존성
├── backend/
│   ├── handlers/
│   │   ├── chat.py                 # POST /chat - 메시지 처리
│   │   ├── conversations.py        # GET /conversations - 대화 이력 조회
│   │   └── health.py               # GET /health - 헬스체크
│   ├── services/
│   │   ├── chatbot_engine.py       # 규칙 기반 상담 로직
│   │   └── conversation_store.py   # DynamoDB CRUD
│   └── utils/
│       └── response.py             # API Gateway 응답 헬퍼
├── frontend/
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.jsx                 # 루트 컴포넌트
│       ├── App.css                 # 전체 스타일
│       ├── index.jsx               # 엔트리포인트
│       ├── components/
│       │   ├── ChatWindow.jsx      # 메인 채팅 컨테이너
│       │   ├── MessageList.jsx     # 메시지 목록 (버블 UI)
│       │   ├── MessageInput.jsx    # 입력창 + 전송 버튼
│       │   └── ConversationList.jsx# 대화 이력 사이드바
│       └── services/
│           └── api.js              # axios 기반 API 클라이언트
└── tests/
    ├── test_chat.py                # Lambda 핸들러 단위 테스트
    └── test_chatbot_engine.py      # 챗봇 엔진 테스트
```

## API 엔드포인트

| Method | Path                | Description                 |
| ------ | ------------------- | --------------------------- |
| POST   | /chat               | 메시지 전송 및 봇 응답 수신 |
| GET    | /conversations      | 대화 목록 조회              |
| GET    | /conversations/{id} | 특정 대화 이력 조회         |
| GET    | /health             | 서비스 상태 확인            |

### POST /chat 요청/응답 예시

**요청:**

```json
{
  "message": "배송 얼마나 걸려요?",
  "conversation_id": "optional-uuid"
}
```

**응답:**

```json
{
  "conversation_id": "uuid",
  "user_message": {
    "role": "user",
    "content": "배송 얼마나 걸려요?",
    "timestamp": "2024-01-20T12:00:00+00:00"
  },
  "bot_message": {
    "role": "bot",
    "content": "배송 관련 안내드립니다.\n- 일반 배송: 결제 완료 후 2~3 영업일 소요\n...",
    "timestamp": "2024-01-20T12:00:00+00:00"
  }
}
```

## 챗봇 엔진 기능

| 기능      | 키워드 예시                | 설명                                  |
| --------- | -------------------------- | ------------------------------------- |
| 인사      | 안녕하세요, hello, hi      | 랜덤 인사말 응답                      |
| 작별      | 감사합니다, bye            | 작별 인사 응답                        |
| 배송 안내 | 배송, 택배, 도착           | 일반/특급 배송 소요일 안내            |
| 반품/환불 | 반품, 환불, 취소           | 반품 절차 및 배송비 안내              |
| 교환      | 교환, 사이즈               | 교환 절차 안내                        |
| 결제      | 결제, 카드, 페이           | 결제 수단 안내                        |
| 회원      | 회원가입, 비밀번호, 로그인 | 회원 관련 안내                        |
| 영업시간  | 영업시간, 몇시             | 고객센터 운영시간 안내                |
| 주문 조회 | ORD-20240001               | 주문번호 패턴 인식 → 상태 조회 (Mock) |
| 도움말    | 도움, 메뉴, help           | 전체 기능 목록 안내                   |

## DynamoDB 테이블 설계

**테이블명:** `customer-chatbot-conversations-{stage}`

| 속성                 | 타입              | 설명                         |
| -------------------- | ----------------- | ---------------------------- |
| conversation_id (PK) | String (UUID)     | 대화 고유 식별자             |
| created_at           | String (ISO 8601) | 대화 생성 시각               |
| updated_at           | String (ISO 8601) | 마지막 업데이트 시각         |
| messages             | List of Map       | `{role, content, timestamp}` |

## 실행 방법

### 테스트 실행

```bash
cd chatbot
python3 -m pytest tests/ -v
```

### 프론트엔드 로컬 실행

```bash
cd chatbot/frontend
npm install
npm start
```

`frontend/.env` 파일에 `REACT_APP_API_URL`을 설정해 백엔드 API URL을 지정한다.

```bash
# 실제 AWS 배포 환경
REACT_APP_API_URL=https://irsd7zj2e2.execute-api.ap-northeast-2.amazonaws.com/dev

# 로컬 테스트 환경 (sls invoke local 사용 시)
REACT_APP_API_URL=http://localhost:3000/dev
```

#### 환경변수 우선순위 (높을수록 우선)

| 순위 | 방법 | 설명 |
| ---- | ---- | ---- |
| 1 | 셸 환경변수 | `REACT_APP_API_URL=https://... npm start` |
| 2 | `.env.local` | 로컬 전용, git 무시 |
| 3 | `.env.development` / `.env.production` | 환경별 파일 |
| 4 | `.env` | 기본값 |

로컬 테스트 시 셸에서 일시적으로 덮어쓰거나, `.env.local`에 로컬 URL을 설정하면 `.env`를 수정하지 않고 전환할 수 있다.

```bash
# 셸에서 일시적으로 덮어쓰기
REACT_APP_API_URL=http://localhost:3000/dev npm start
```

### 로컬 Lambda 테스트

```bash
sls invoke local -f chat --data '{"body":"{\"message\":\"안녕하세요\"}"}'
sls invoke local -f health
```

### AWS 배포

```bash
cd chatbot
npm install -g serverless
sls deploy --stage dev
```

배포 후 출력되는 API Gateway URL을 프론트엔드의 `REACT_APP_API_URL`에 설정한다.

### 배포 결과 (dev 스테이지)

```
✔ Service deployed to stack customer-chatbot-dev (179s)

endpoints:
  POST - https://irsd7zj2e2.execute-api.ap-northeast-2.amazonaws.com/dev/chat
  GET  - https://irsd7zj2e2.execute-api.ap-northeast-2.amazonaws.com/dev/conversations
  GET  - https://irsd7zj2e2.execute-api.ap-northeast-2.amazonaws.com/dev/conversations/{id}
  GET  - https://irsd7zj2e2.execute-api.ap-northeast-2.amazonaws.com/dev/health

functions:
  chat:             customer-chatbot-dev-chat (29 kB)
  getConversations: customer-chatbot-dev-getConversations (29 kB)
  getConversation:  customer-chatbot-dev-getConversation (29 kB)
  health:           customer-chatbot-dev-health (29 kB)
```

## 설계 결정 사항

1. **REST API**: WebSocket 대신 REST를 선택. 포트폴리오 목적으로 이해와 디버깅이 용이함.
2. **규칙 기반 엔진**: 외부 AI API 의존 없이 동작하여 비용 0원, 즉시 시연 가능. 추후 LLM 연동 확장점 제공.
3. **DynamoDB**: Serverless에 최적화되고 Free Tier 범위 내 운영 가능.
4. **단일 serverless.yml**: 백엔드 Lambda + DynamoDB를 하나의 CloudFormation 스택으로 관리.

## 테스트 현황

총 28개 테스트 전부 통과:

- `test_chatbot_engine.py` (20개): 인사, 작별, FAQ 6종, 주문조회, 도움말, 기본응답
- `test_chat.py` (8개): Lambda 핸들러 (신규 대화, 기존 대화, 입력 검증, CORS, 메시지 저장)

  체크리스트:

  ┌────────┬────────────────────────────────────────────────────┬──────┐
  │ 단계 │ 항목 │ 상태 │
  ├────────┼────────────────────────────────────────────────────┼──────┤
  │ Step 1 │ 프로젝트 구조 + serverless.yml + requirements.txt │ 완료 │
  ├────────┼────────────────────────────────────────────────────┼──────┤
  │ Step 2 │ 챗봇 엔진 (인사, FAQ 6종, 주문조회, 기본응답) │ 완료 │
  ├────────┼────────────────────────────────────────────────────┼──────┤
  │ Step 3 │ DynamoDB 대화 저장소 (CRUD) │ 완료 │
  ├────────┼────────────────────────────────────────────────────┼──────┤
  │ Step 4 │ Lambda 핸들러 4개 (chat, conversations x2, health) │ 완료 │
  ├────────┼────────────────────────────────────────────────────┼──────┤
  │ Step 5 │ React 프론트엔드 (4개 컴포넌트 + API 모듈 + CSS) │ 완료 │
  ├────────┼────────────────────────────────────────────────────┼──────┤
  │ Step 6 │ 테스트 코드 (28개 전부 통과) │ 완료 │
  └────────┴────────────────────────────────────────────────────┴──────┘

  │ Step 7 │ Git 초기화 + GitHub 저장소 업로드                    │ 완료 │
  └────────┴────────────────────────────────────────────────────┴──────┘

## GitHub 저장소

- **URL**: https://github.com/kikjs75/chatbot
- **브랜치**: master

  다음 단계로 할 수 있는 것들:
  - cd frontend && npm install && npm start - 프론트엔드 로컬 실행
  - sls deploy - AWS에 백엔드 배포
  - sls invoke local -f chat --data '{"body":"{\"message\":\"안녕하세요\"}"}' - 로컬 Lambda 테스트
