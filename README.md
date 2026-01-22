# 報告書自動セットツール

このツールは過去の報告書ページからデータを取得し、  
現在の報告書欄にをまとめて保存できる Python スクリプトです。  

## 環境準備

1. Python 3.10 以上をインストール
2. 仮想環境を作成（推奨）  ```python -m venv venv```
3. 仮想環境を有効化
    - Windows : ```venv\Scripts\activate```
    - Mac / Linux : ```source venv/bin/activate```
4. 必要パッケージをインストール  ```pip install -r requirements.txt```
5. リポジトリのクローン  
      ```git clone https://github.com/kondo-akihiro-git/project-Python-PortalScraper.git```

## 設定情報

以下情報をご自身の環境に合わせて.envファイルを作成してください。

```
BASE_URL=読み取り対象のURL
BASIC_AUTH_ID=BASIC認証ID
BASIC_AUTH_PASS=BASIC認証パスワード
LOGIN_ID=ログインID
LOGIN_PASS=ログインパスワード
MEMBER_NO=社員ナンバー
```

## 実行手順

1. 報告書ページにデータが未入力であることを確認してください。
2. main.py を実行します。
    ```python app/main.py```
3. 1週間前の報告書データが自動で保存されますので、  
    現在の報告書ページにデータが入っていることを確認してください。
