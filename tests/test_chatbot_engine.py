import pytest

from backend.services.chatbot_engine import get_response


class TestGreetings:
    def test_hello_korean(self):
        response = get_response("안녕하세요")
        assert "안녕하세요" in response or "반갑습니다" in response or "도움" in response

    def test_hello_english(self):
        response = get_response("hello")
        assert len(response) > 0

    def test_hi(self):
        response = get_response("hi")
        assert len(response) > 0


class TestGoodbyes:
    def test_thanks(self):
        response = get_response("감사합니다")
        assert "감사" in response or "좋은" in response

    def test_bye(self):
        response = get_response("bye")
        assert len(response) > 0


class TestFAQ:
    def test_shipping(self):
        response = get_response("배송 얼마나 걸려요?")
        assert "배송" in response
        assert "영업일" in response

    def test_return(self):
        response = get_response("반품하고 싶어요")
        assert "반품" in response
        assert "7일" in response

    def test_exchange(self):
        response = get_response("교환 가능한가요?")
        assert "교환" in response

    def test_payment(self):
        response = get_response("결제 방법이 뭐가 있나요?")
        assert "결제" in response
        assert "카드" in response or "페이" in response

    def test_membership(self):
        response = get_response("비밀번호를 잊어버렸어요")
        assert "비밀번호" in response

    def test_business_hours(self):
        response = get_response("상담시간이 어떻게 되나요?")
        assert "운영 시간" in response or "09:00" in response


class TestOrderLookup:
    def test_existing_order(self):
        response = get_response("주문번호 ORD-20240001 조회해주세요")
        assert "ORD-20240001" in response
        assert "프리미엄 무선 이어폰" in response
        assert "배송 완료" in response

    def test_existing_order_in_transit(self):
        response = get_response("ORD-20240002")
        assert "배송 중" in response

    def test_nonexistent_order(self):
        response = get_response("ORD-99999999")
        assert "찾을 수 없습니다" in response

    def test_order_pattern_in_sentence(self):
        response = get_response("제 주문번호는 ORD-20240003입니다")
        assert "노트북 파우치" in response


class TestHelp:
    def test_help_keyword(self):
        response = get_response("도움")
        assert "배송" in response
        assert "반품" in response

    def test_menu(self):
        response = get_response("메뉴")
        assert "배송" in response


class TestDefault:
    def test_unknown_input(self):
        response = get_response("asdfghjkl")
        assert "죄송합니다" in response or "상담원" in response

    def test_empty_input(self):
        response = get_response("")
        assert "입력" in response

    def test_whitespace_only(self):
        response = get_response("   ")
        assert "입력" in response
