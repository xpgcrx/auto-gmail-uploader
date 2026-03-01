# Googleドライブの特定フォルダに特定の条件を満たすGmailを定期的にアップロードするワークフロー

## やりたいこと

- Gmailのメールマガジンが届いたらMarkdownに変換し、Googleドライブの特定のディレクトリにアップロードする

### HAPA英会話

- 平日毎日日本時間の6:07や6:08あたりに配信される
- GoogleドライブのフォルダID = [REDACTED_FOLDER_ID] にアップロード

### ニックのひとこと英会話

- 平日毎日日本時間の8:04や8:06あたりに配信される
- GoogleドライブのフォルダID = [REDACTED_FOLDER_ID] にアップロード

### 週刊Life is beautiful

- 火曜日の日本時間の7:20や7:25あたりに配信される
- GoogleドライブのフォルダID = [REDACTED_FOLDER_ID] にアップロード

## 技術要件

このディレクトリにはまだ何も無いが以下のように作ることとする

- Pythonを使用（最新版で良いが後述のuvを使ってバージョン固定する）
- パッケージマネージャーにはuvを使用する
- 適切にGEMINI.mdをプロジェクトルートに生成する
- 動作したらdiscordに通知する。webhookで通知出来る
  - webhook URLはどのメルマガも同じで以下で良い
    - https://discord.com/api/webhooks/[REDACTED_WEBHOOK_ID]/[REDACTED_TOKEN]
- 認証情報やdiscordの通知のwebhook URLやGoogleドライブのフォルダIDはgit管理化に置かないようにする
- Google Cloud上で稼働させたい。定期的に実行だけすれば良いものなら、Compute EngineなどよりCloud Functionsなどで良いと思う
  - インフラはterraformで定義しデプロイ出来るようにする。必要であればterragruntも使う。デプロイ手順は手順書を書く

## アーキテクチャ案

以下に案を書くが、もっと良いものがあれば提案してほしい

- メールマガジンは一種類につき1つのyamlなどで定義
- Pythonスクリプトは共通で使用し、そのyamlをパラメータとして読み込んで使用
- その場合、それぞれの更新タイミングは違うがそれに関してはどう吸収する？
  - 例えば火曜日にだけ配信されるものなら、チェックタイミングは火曜日に動くだけで良い
