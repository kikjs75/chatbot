import re
import random


GREETINGS = ["안녕하세요", "안녕", "하이", "hello", "hi", "반갑습니다"]
GOODBYES = ["감사합니다", "고마워요", "바이", "bye", "종료", "끝"]

FAQ = {
    "배송": {
        "keywords": ["배송", "택배", "배달", "도착", "며칠"],
        "answer": (
            "배송 관련 안내드립니다.\n"
            "- 일반 배송: 결제 완료 후 2~3 영업일 소요\n"
            "- 특급 배송: 결제 완료 후 1 영업일 이내 도착\n"
            "- 배송 조회는 주문번호를 입력해주시면 확인 가능합니다."
        ),
    },
    "반품": {
        "keywords": ["반품", "환불", "돌려", "취소"],
        "answer": (
            "반품/환불 안내드립니다.\n"
            "- 수령 후 7일 이내 반품 신청 가능합니다.\n"
            "- 단순 변심: 반품 배송비 고객 부담 (3,000원)\n"
            "- 상품 불량: 반품 배송비 무료\n"
            "- 반품 신청은 마이페이지 > 주문내역에서 가능합니다."
        ),
    },
    "교환": {
        "keywords": ["교환", "바꿔", "사이즈", "색상 변경"],
        "answer": (
            "교환 안내드립니다.\n"
            "- 수령 후 7일 이내 교환 신청 가능합니다.\n"
            "- 동일 상품 내 사이즈/색상 교환만 가능합니다.\n"
            "- 교환 배송비: 단순 변심 시 6,000원 (왕복)\n"
            "- 마이페이지 > 주문내역에서 신청해주세요."
        ),
    },
    "결제": {
        "keywords": ["결제", "카드", "계좌", "페이", "할부", "무통장"],
        "answer": (
            "결제 수단 안내드립니다.\n"
            "- 신용/체크카드 (2~6개월 무이자 할부 가능)\n"
            "- 카카오페이, 네이버페이, 토스페이\n"
            "- 무통장 입금 (입금 확인 후 발송)\n"
            "- 결제 오류 시 다른 브라우저나 결제 수단을 이용해보세요."
        ),
    },
    "회원": {
        "keywords": ["회원가입", "탈퇴", "비밀번호", "로그인", "아이디"],
        "answer": (
            "회원 관련 안내드립니다.\n"
            "- 회원가입: 이메일 또는 소셜 로그인으로 간편 가입 가능\n"
            "- 비밀번호 분실: 로그인 페이지 > '비밀번호 찾기' 이용\n"
            "- 회원 탈퇴: 마이페이지 > 설정 > 회원 탈퇴\n"
            "- 탈퇴 후 동일 이메일로 재가입 가능합니다."
        ),
    },
    "영업시간": {
        "keywords": ["영업시간", "운영시간", "몇시", "상담시간", "언제"],
        "answer": (
            "고객센터 운영 시간 안내드립니다.\n"
            "- 평일: 09:00 ~ 18:00\n"
            "- 점심시간: 12:00 ~ 13:00\n"
            "- 주말 및 공휴일 휴무\n"
            "- 챗봇은 24시간 이용 가능합니다."
        ),
    },
}

MOCK_ORDERS = {
    "ORD-20240001": {"status": "배송 완료", "item": "프리미엄 무선 이어폰", "date": "2024-01-15"},
    "ORD-20240002": {"status": "배송 중", "item": "스마트워치 Pro", "date": "2024-01-18"},
    "ORD-20240003": {"status": "결제 완료 (배송 준비 중)", "item": "노트북 파우치", "date": "2024-01-20"},
}

ORDER_PATTERN = re.compile(r"ORD-\d{8}", re.IGNORECASE)


def get_response(message):
    text = message.strip()
    if not text:
        return "메시지를 입력해주세요."

    lower = text.lower()

    # 인사
    if any(g in lower for g in GREETINGS):
        greetings = [
            "안녕하세요! 고객 상담 챗봇입니다. 무엇을 도와드릴까요?",
            "반갑습니다! 배송, 반품, 교환, 결제 등 궁금한 점을 물어보세요.",
            "안녕하세요! 어떤 도움이 필요하신가요?",
        ]
        return random.choice(greetings)

    # 작별
    if any(g in lower for g in GOODBYES):
        farewells = [
            "감사합니다! 좋은 하루 보내세요. 😊",
            "이용해 주셔서 감사합니다. 또 궁금한 점이 있으시면 언제든 문의해주세요!",
            "감사합니다! 다른 문의사항이 있으시면 다시 찾아주세요.",
        ]
        return random.choice(farewells)

    # 주문 조회
    order_match = ORDER_PATTERN.search(text)
    if order_match:
        order_id = order_match.group(0).upper()
        return _lookup_order(order_id)

    # FAQ 매칭
    for category, data in FAQ.items():
        if any(kw in lower for kw in data["keywords"]):
            return data["answer"]

    # 도움말 / 메뉴
    if any(kw in lower for kw in ["도움", "help", "메뉴", "뭐", "기능"]):
        return (
            "다음과 같은 문의를 도와드릴 수 있습니다:\n"
            "1. 📦 배송 조회 및 안내\n"
            "2. 🔄 반품/환불 안내\n"
            "3. 🔃 교환 안내\n"
            "4. 💳 결제 수단 안내\n"
            "5. 👤 회원 관련 안내\n"
            "6. 🔍 주문 조회 (주문번호 입력)\n\n"
            "궁금한 항목을 선택하거나 질문을 입력해주세요!"
        )

    # 기본 응답
    return (
        "죄송합니다. 해당 문의에 대한 답변을 찾지 못했습니다.\n"
        "아래 항목 중 선택하시거나, '도움'을 입력하여 안내를 받아보세요.\n"
        "- 배송, 반품, 교환, 결제, 회원, 주문조회\n\n"
        "상담원 연결이 필요하시면 고객센터(1588-0000)로 전화해주세요."
    )


def _lookup_order(order_id):
    order = MOCK_ORDERS.get(order_id)
    if order:
        return (
            f"주문번호 {order_id} 조회 결과입니다.\n"
            f"- 상품: {order['item']}\n"
            f"- 주문일: {order['date']}\n"
            f"- 상태: {order['status']}"
        )
    return (
        f"주문번호 {order_id}에 해당하는 주문을 찾을 수 없습니다.\n"
        "주문번호를 다시 확인해주세요. (예: ORD-20240001)"
    )
