# CI status

`.github/workflows/ci.yml` をGitHub API経由で作成しようとしましたが、2回とも次のエラーで拒否されました。

```text
GitHub API 404: Not Found
```

アプリ本体、テスト、README、devcontainer、設計資料は作成済みです。CIの内容は `docs/github-actions-ci.yml` に保存しています。

この失敗は、リポジトリ作成や通常ファイル更新は成功している一方で、`.github/workflows/*` だけ拒否されているため、GitHub Actions workflowファイルを更新する権限が現在のGitHub連携トークンにない状態と考えられます。

## 有効化方法

workflow更新権限を持つGitHub連携に直した後、`docs/github-actions-ci.yml` と同じ内容を `.github/workflows/ci.yml` に配置してください。

## 予定されていたCI内容

- checkout
- Python 3.11 / 3.12 setup
- dependency install
- `ruff check .`
- `pytest -q --junitxml=reports/pytest.xml`
- test report artifact upload
