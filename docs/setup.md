# Setup Guide

## 1. Meta Developer Appを作る

1. Meta for Developers にログインします。
2. 新しいアプリを作成します。
3. ユースケースでMessenger / Business Messagingを選びます。
4. Facebookページを接続します。

## 2. Page Access Tokenを発行する

1. Messenger API設定画面を開きます。
2. 対象Facebookページを選びます。
3. `pages_messaging` 権限を付けて Page Access Token を生成します。
4. 生成したトークンを本番環境のSecret `PAGE_ACCESS_TOKEN` に保存します。

## 3. このアプリをHTTPS公開する

Cloud Run、Render、Fly.io、Railway、AWS App Runnerなど任意の環境にデプロイします。

最低限必要な環境変数:

```bash
VERIFY_TOKEN=任意の長い文字列
PAGE_ACCESS_TOKEN=Metaで発行したPage Access Token
PAGE_ID=FacebookページID
GRAPH_API_VERSION=v25.0
SEND_REAL_MESSAGES=true
AUTO_REPLY_ENABLED=true
```

推奨:

```bash
APP_SECRET=Meta App Secret
DATABASE_URL=sqlite:///./messenger_events.db
```

## 4. Webhookを登録する

Meta Developer ConsoleでWebhook設定を開きます。

- Callback URL: `https://YOUR-DOMAIN/webhook`
- Verify Token: `VERIFY_TOKEN` と同じ値
- Subscription fields: 最低限 `messages`

検証時、Metaは次のようなGETを送ります。

```text
GET /webhook?hub.mode=subscribe&hub.verify_token=...&hub.challenge=...
```

アプリはVerify Tokenが一致した場合、`hub.challenge` をそのまま返します。

## 5. テスト

最初は `SEND_REAL_MESSAGES=false` のdry-runで動作確認してください。

```bash
python scripts/simulate_webhook.py --url https://YOUR-DOMAIN/webhook --text '予約したいです'
```

返信文がJSONで返り、DBに保存されればアプリ側は動いています。

実際のMessenger返信をテストするには:

1. Facebookページにテストユーザーからメッセージを送る。
2. Webhookログで `sender.id`、つまりPage-scoped user IDを確認する。
3. `SEND_REAL_MESSAGES=true` にしてページへ再度メッセージを送る。

手動送信テスト:

```bash
python scripts/send_test_message.py --recipient-id PAGE_SCOPED_USER_ID --text 'テスト返信です'
```

## 6. App Review

開発者・管理者・テストユーザー以外に公開する場合、必要な権限はMetaの審査対象になることがあります。審査では、ページ宛メッセージを受け取って返信する実際の画面、利用目的、データ保存方針、ユーザーへの説明を用意してください。

## 7. 運用チェックリスト

- Page Access Tokenをリポジトリにコミットしない。
- `APP_SECRET` を設定してWebhook署名を検証する。
- 返信できる範囲はMetaのメッセージポリシーに従う。
- ユーザーの個人情報をログに保存する場合、保存期間と削除方法を決める。
- 自動返信だけで解決できない会話は人間へ引き継ぐ。
