from __future__ import annotations


def build_reply(text: str) -> str:
    """Generate a conservative auto-reply.

    This default engine is intentionally rule-based. Replace this function with
    your CRM, FAQ database, or approved LLM workflow after reviewing privacy and
    data retention requirements.
    """
    normalized = text.strip().lower()

    if any(word in normalized for word in ["料金", "価格", "値段", "price", "cost", "fee"]):
        return "お問い合わせありがとうございます。料金について確認します。ご希望のプランや数量があれば教えてください。"

    if any(word in normalized for word in ["営業時間", "何時", "open", "hours", "business hour"]):
        return "お問い合わせありがとうございます。営業時間は店舗・サービスにより異なります。ご希望の窓口名を教えてください。"

    if any(word in normalized for word in ["予約", "日程", "booking", "reserve", "appointment"]):
        return "ご予約についてありがとうございます。希望日時、人数、お名前を送っていただければ確認します。"

    if any(word in normalized for word in ["住所", "場所", "アクセス", "address", "location"]):
        return "アクセスについてのお問い合わせありがとうございます。ご利用予定の店舗または地域を教えてください。"

    if any(word in normalized for word in ["ありがとう", "thanks", "thank you"]):
        return "こちらこそありがとうございます。ほかに必要なことがあればメッセージしてください。"

    return "メッセージありがとうございます。内容を確認しました。担当者または自動応答が順次ご案内します。"
