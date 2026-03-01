# タスクリスト

## 🚨 タスク完全完了の原則

**このファイルの全タスクが完了するまで作業を継続すること**

### 必須ルール
- **全てのタスクを`[x]`にすること**
- 仕掛中のタスクは `[-]` にすること
- タスクを完了として `[x]` にする際は必ずユーザの承認が必要
- 「時間の都合により別タスクとして実施予定」は禁止
- 「実装が複雑すぎるため後回し」は禁止
- 未完了タスク（`[ ]`）を残したまま作業を終了しない

---

## フェーズ0: Google Cloud 手動準備

- [x] Google Cloud プロジェクトの作成
    - [x] 新規プロジェクト作成と請求先アカウントの紐付け
- [x] API の有効化 (手動または一部 Terraform)
    - [x] Gmail API, Google Drive API, Secret Manager API, Cloud Functions API 等の有効化
- [x] OAuth 同意画面の設定
    - [x] 内部/外部テスト用の同意画面構成とテストユーザー(自身のメルマガ受信アドレス)の追加
- [x] OAuth 2.0 認証情報の作成
    - [x] デスクトップアプリ用クライアントID/シークレットの生成
- [x] 初回トークン取得スクリプトの実行
    - [x] ローカルで認証を通し、`refresh_token` を取得する

## フェーズ1: 開発環境構築

- [x] プロジェクトの初期化
    - [x] `uv init` による Python 環境の構築
    - [x] `pyproject.toml` への依存ライブラリ追加 (`google-api-python-client`, `markdownify`, `pyyaml` 等)
- [x] `GEMINI.md` の作成
    - [x] プロジェクト固有のルールを定義

## フェーズ2: コアロジックの実装

- [x] 設定管理 (`config.py`)
    - [x] `configs/newsletters.yaml` のパース処理実装
- [x] Markdown 変換エンジン (`converter.py`)
    - [x] HTML から Markdown への変換ロジック実装
    - [x] ユニットテストの作成とパス
- [x] Gmail API 連携 (`gmail_client.py`)
    - [x] クエリによるメール検索機能
    - [x] メールの取得と本文抽出
- [x] Google Drive API 連携 (`drive_client.py`)
    - [x] 指定フォルダへのファイルアップロード機能
- [x] Discord 通知 (`notifier.py`)
    - [x] Webhook を利用した通知機能

## フェーズ3: 統合とローカル検証

- [x] メインフローの実装 (`main.py`)
    - [x] 全コンポーネントの統合
- [x] ローカルでのエンドツーエンドテスト
    - [x] テスト用アカウントを使用した動作確認
    - [x] 処理済みメールの重複ガードの確認

## フェーズ4: インフラ構築 (Terraform)

- [x] Terraform 基本構成
    - [x] Provider 設定、GCP プロジェクト設定
- [x] シークレット管理
    - [x] Secret Manager への認証情報登録スクリプトの作成・実行
- [x] リソース定義
    - [x] Cloud Functions の定義
    - [x] Cloud Scheduler の定義
    - [x] IAM ロールの設定
- [x] デプロイ検証
    - [x] `terraform apply` による環境構築

## フェーズ5: 品質チェックと修正

- [x] すべての自動テストが通ることを確認
- [x] 本番用メルマガターゲットでの動作確認

## フェーズ6: ドキュメント更新

- [x] README.md の更新
- [x] 実装後の振り返り（このファイルの下部に記録）

---

## 実装後の振り返り

### 実装完了日
2026-03-01

### 計画と実績の差分

**計画と異なった点**:
- 処理対象を「全未処理メール」から「最新の1件のみ」に変更し、負荷と重複を抑制。
- ファイル命名規則を `yyyymmdd_{件名}.md` に改善。
- Cloud Functions 2nd gen 特有の権限（Storage Viewer, Artifact Registry）への対応が必要だった。

**新たに必要になったタスク**:
- `scripts/update_secrets.py`: シークレット登録の自動化。
- `main.py` (ルート): Cloud Functions のエントリポイント解決用のブリッジ。

**技術的理由でスキップしたタスク**:
- なし。

### 学んだこと

**技術的な学び**:
- Cloud Functions 2nd gen の内部構造（Cloud Runベース）と、それに伴う IAM 設定の重要性。
- `uv` と Cloud Build の相性（requirements.txt の有用性）。
- BeautifulSoup を用いた HTML メールの Markdown 化における事前整形テクニック。

**プロセス上の改善点**:
- API 有効化の反映待ち時間をあらかじめ考慮したスケジュール。

### 次回への改善提案
- シークレット登録の Terraform 完全自動化。
- メルマガごとの HTML 抽出セレクタのカスタマイズ機能。
