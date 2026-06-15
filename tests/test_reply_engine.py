from app.reply_engine import build_reply


def test_price_reply() -> None:
    reply = build_reply("料金を教えてください")
    assert "料金" in reply


def test_default_reply() -> None:
    reply = build_reply("こんにちは")
    assert "メッセージありがとうございます" in reply
