Readme in English

# 概要
Amazon EchoやAlexaアプリを通じて、ChatGPTに対して以下のことが実施できるAlexaスキルです。
1. 質問に対する回答を得ること
  - シンプルに回答を得る
  - Zero-shot Chain-of-Thoughtを利用した回答を得る
  - 特にPromptに工夫なく回答を得る
2. 日英/英日翻訳を実施すること

Alexaスキルで利用するインタラクションモデルのサンプル発話はご自由にご編集ください。 
私の例では「エルちゃん」が出てきますが、これは亡くなった私のペットのウサギの名前です。  

lambda_function.pyのsystem_contentおよびreprompt_textもご自由にご編集ください。 
現在のソースでは、system_contentでは「エルちゃん」のキャラクター性が模倣されるようなPromptを考え設定しています。  

スキルのinvocationNameはニュートンとしていますが、こちらもご自由にご編集ください。 

# 導入方法

※以下はGPT-4に基づいて記述しています。Readmeの最後に元となったpromptを記載します。

## Step 1: ChatGPT APIキーの取得
1. OpenAIのWebサイト(https://www.openai.com/)にアクセスし、アカウントを作成またはログインします。
2. APIキーを取得するために、ダッシュボードに移動します。キーは後の手順で使用します。

## Step 2: AWSアカウントの作成と設定
1. AWSにアクセスし（https://aws.amazon.com/)、アカウントを作成またはログインします。
2. IAM（Identity and Access Management）コンソールに移動し、新しいユーザーを作成して適切な権限を付与します。AWS Lambdaを実行するための権限が必要です。

## Step 3: AWS Lambda関数の作成
1. AWS Lambdaコンソール（https://console.aws.amazon.com/lambda/)に移動し、「関数の作成」をクリックします。
2. 「一から作成」を選択し、関数名とランタイム（Python）を入力します。
3. 作成した関数を選択し、関数コードセクションで「コードのアップロード」をクリックします。
4. コードをアップロードするためのZIPファイルを作成します。ZIPファイルには、Pythonスクリプト（lambda_function.py）と、必要な依存関係（openaiライブラリなど）を含めます。ZIPファイルをアップロードします。
5. 環境変数にOPENAI_API_KEYを追加し、取得したChatGPT APIキーを設定します。

## Step 4: 必要な依存関係のインストール
1. 下記コマンドで依存関係をインストールします
```
pip install -r requirements.txt -t .
```
2. ZIPファイルを作成しLambda関数にアップロードします。

## Step 5: Alexaスキルの作成
1. Amazon Developer Console（https://developer.amazon.com/)にアクセスし、アカウントを作成またはログインします。
2. 「Alexaコンソール」に移動し、「スキルの作成」をクリックします。
3. スキル名を入力し、「カスタム」モデルを選択します。 ホスティングサービスは「独自のプロビジョニング」とします。スキルの言語も選択し、「スキルの作成」をクリックします。
4. 「インタラクションモデル」の左側のメニューで、「JSONエディタ」を選択し、以下のインテントスキーマを貼り付けます。これにより、ユーザーが質問をするためのインテントが作成されます。
```
{
    "interactionModel": {
        "languageModel": {
            "invocationName": "ニュートン",
            "intents": [
                {
                    "name": "AMAZON.CancelIntent",
                    "samples": []
                },
                {
                    "name": "AMAZON.HelpIntent",
                    "samples": []
                },
                {
                    "name": "AMAZON.StopIntent",
                    "samples": []
                },
                {
                    "name": "AMAZON.NavigateHomeIntent",
                    "samples": []
                },
                {
                    "name": "AskGPTIntent",
                    "slots": [
                        {
                            "name": "Prompt",
                            "type": "AMAZON.SearchQuery"
                        }
                    ],
                    "samples": [
                        "ニュートンでインテリエルちゃんに {Prompt} とお願いして",
                        "インテリエルちゃん {Prompt}",
                        "{Prompt} ないんですか",
                        "{Prompt} どうですか",
                        "{Prompt} ですか",
                        "{Prompt} 教えて",
                        "{Prompt} について教えて"
                    ]
                },
                {
                    "name": "TranslateEnglishIntent",
                    "slots": [
                        {
                            "name": "Prompt",
                            "type": "AMAZON.SearchQuery"
                        }
                    ],
                    "samples": [
                        "{Prompt} を英訳して",
                        "{Prompt} を英語に訳して",
                        "{Prompt} を英語に翻訳して"
                    ]
                },
                {
                    "name": "TranslateJapaneseIntent",
                    "slots": [
                        {
                            "name": "Prompt",
                            "type": "AMAZON.SearchQuery"
                        }
                    ],
                    "samples": [
                        "{Prompt} を訳して",
                        "{Prompt} を翻訳して",
                        "{Prompt} を日本語に翻訳して"
                    ]
                },
                {
                    "name": "ContinueIntent",
                    "slots": [],
                    "samples": [
                        "続きをお願い",
                        "続きをお願いします",
                        "続きを"
                    ]
                },
                {
                    "name": "AskSimpleGPTIntent",
                    "slots": [
                        {
                            "name": "Prompt",
                            "type": "AMAZON.SearchQuery"
                        }
                    ],
                    "samples": [
                        "ニュートンでシンプルエルちゃんに {Prompt} とお願いして",
                        "シンプルエルちゃん {Prompt}"
                    ]
                },
                {
                    "name": "AskNormalGPTIntent",
                    "slots": [
                        {
                            "name": "Prompt",
                            "type": "AMAZON.SearchQuery"
                        }
                    ],
                    "samples": [
                        "ニュートンでノーマルエルちゃんに {Prompt} とお願いして",
                        "ノーマルエルちゃん {Prompt}"
                    ]
                }
            ],
            "types": []
        }
    }
}
```
4. 「ビルド」タブをクリックして、インタラクションモデルをビルドします。

## Step 7: エンドポイントの設定
1. Alexaスキルで「エンドポイント」を選択し、AWS Lambda ARN（Amazon Resource Name）を入力します。これは、Step 3で作成したLambda関数のARNです。
2. スキルIDをコピーし、Lambda関数のトリガーに追加します。これにより、Lambda関数がAlexaスキルから呼び出されるようになります。

## Step 8: スキルのテスト
1. Alexa Developer Consoleの「テスト」タブを選択し、スキルを有効化します。
2. テストページの左側のメニューで、「デバイスディスプレイ」を選択し、テストリクエストを入力します。例: "ニュートンでインテリエルちゃんにおいしいビールの銘柄について教えてとお願いして"
3. 正しい応答が表示されることを確認します。
4. これで、AlexaでChatGPTを使用する設定が完了しました。ユーザーは、スキルを使ってChatGPTに質問を投げかけ、応答を受け取ることができます。

## Step 9: スキルのAmazon Echoでの利用
1. 現在私はベータテスターとして自宅のAmazon EchoやAlexaアプリにスキルをインストールし利用しています。
2. ベータテストは3ヶ月間しか有効でないため、もし他に良い方法があれば、教えて欲しいです。

## Step 10: 各サービスに対する利用料の上限値の設定（必要であれば）
1. OpenAIのAPIの利用上限値の設定やAWSのBudgetsの設定等を行い、自分の予算感にあった金額で運用できるようにしています。

## 導入方法の作成に利用したprompt
```
AlexaでChatGPTを使用できるようにしたいと考えています。以下のサービスを使用する前提です。
- ChatGPT API
- Alexaスキル
- AWS Lambda
これを実現するための方法をstep-by-stepで説明してください。
```

# 利用方法
- スキルを起動してから質問を投げる
  1. アレクサ、ニュートンを起動して
  2. {インテリ, シンプル, ノーマル}エルちゃん、おいしいビールの銘柄について教えて / hogehogeを英訳して
- インテントを直接起動して質問を投げる
  1. アレクサ、ニュートンで{インテリ, シンプル, ノーマル}エルちゃんに「おいしいビールの銘柄について教えて」とお願いして
- 回答が途中で途切れた場合
  - 「続きを」というと、回答の続きを答えてくれます。

# Limitation
- Alexaの発話の受付時間
  - Alexaのユーザの発話の受付時間が8秒しかないため、あまり長い質問をすると、途中で受付が終わってしまいます。
  - 何かよい改善方法を知っていましたら、教えてもらえると嬉しいです。
- 回答が途中で終わってしまった場合
  - 「続きを」と発話することで続きの回答を教えてくれますが、冒頭に謝罪などが入ったり、きちんと続きを話してくれないことがあります。
  - iPhoneのAlexaアプリだと完璧に続きを話してくれますが、Android, Amazon Echoだとなぜかうまくいきません。
  - もし何か良い知恵がありましたら、教えてもらえると嬉しいです。

# Example
## シンプルエルちゃん
![image](https://user-images.githubusercontent.com/12249301/231931147-c20f352d-4ff1-40cf-afdd-a7375ff4bc2e.png)
## インテリエルちゃん
![image](https://user-images.githubusercontent.com/12249301/231930862-05d00abd-34b2-465f-86d4-107a6cdb6923.png)

良いChatGPTライフを！
