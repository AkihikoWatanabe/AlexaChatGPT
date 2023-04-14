# Overview
[日本語はこちら](https://github.com/AkihikoWatanabe/AlexaChatGPT/blob/main/readme_jp.md)

This Alexa skill enables users to interact with ChatGPT via Amazon Echo or the Alexa app to accomplish the following:
1. Obtain answers to questions
  - Receive simple answers
  - Receive answers using Zero-shot Chain-of-Thought
  - Obtain answers without particularly crafted prompts
2. Perform Japanese-to-English and English-to-Japanese translations

Feel free to edit the sample utterances for the interaction model used in the Alexa skill. In my example, "El-chan" appears, which is the name of my late pet rabbit.

You may also freely edit the system_content and reprompt_text in lambda_function.py. In the current source, the character of "El-chan" is emulated by the prompts set for system_content.

The invocation name of the skill is set to "Newton," but you may edit this as well.

# Setup

*Please note that the following instructions are based on GPT-4. The original prompt is provided at the end of the Readme.

## Step 1: Obtain ChatGPT API Key
1. Access the OpenAI website (https://www.openai.com/) and create an account or log in.
2. Go to the dashboard to obtain an API key, which will be used in later steps.

## Step 2: Create and Set Up an AWS Account
1. Access AWS (https://aws.amazon.com/) and create an account or log in.
2. Navigate to the IAM (Identity and Access Management) console, create a new user, and grant appropriate permissions. You will need permissions to execute AWS Lambda.

## Step 3: Create an AWS Lambda Function
1. Go to the AWS Lambda console (https://console.aws.amazon.com/lambda/) and click "Create function."
2. Select "Author from scratch," enter a function name and runtime (Python).
3. Select the created function, and in the Function code section, click "Upload code."
4. Create a ZIP file for uploading the code, including the Python script (lambda_function.py) and any required dependencies (such as the openai library). Upload the ZIP file.
5. Add OPENAI_API_KEY to the environment variables and set the obtained ChatGPT API key.

## Step 4: Install Required Dependencies
1. Install the dependencies with the following command:
```
pip install -r requirements.txt -t .
```
2. Create a ZIP file and upload it to the Lambda function.

## Step 5: Create an Alexa Skill
1. Access the Amazon Developer Console (https://developer.amazon.com/) and create an account or log in.
2. Go to the "Alexa Console" and click "Create Skill."
3. Enter a skill name, select the "Custom" model, and choose "Self-hosted" for the hosting service. Also, select the skill language and click "Create Skill."
4. In the left menu of "Interaction Model," select "JSON Editor" and paste the following intent schema. This creates an intent for users to ask questions.
=======
```
{
    "interactionModel": {
        "languageModel": {
            "invocationName": "Newton",
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
                        "Ask Intelligent El-chan {Prompt} with Newton",
                        "Intelligent El-chan {Prompt}",
                        "How about {Prompt}",
                        "Tell me about {Prompt}",
                        "Explain {Prompt}"
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
                        "Translate {Prompt} to English",
                        "Translate {Prompt} into English",
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
                        "Translate {Prompt} to Japanese",
                        "Translate {Prompt} into Japanese"
                    ]
                },
                {
                    "name": "ContinueIntent",
                    "slots": [],
                    "samples": [
                        "Please continue",
                        "Please proceed",
                        "Continue"
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
                        "Ask Simple El-chan {Prompt} with Newton",
                        "Simple El-chan {Prompt}"
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
                        "Ask Normal El-chan {Prompt} with Newton",
                        "Normal El-chan {Prompt}"
                    ]
                }
            ],
            "types": []
        }
    }
}
```
4. Click the "Build" tab to build the interaction model.

## Step 7: Configuring the Endpoint
1. In your Alexa skill, select "Endpoint" and input the AWS Lambda ARN (Amazon Resource Name). This is the ARN of the Lambda function you created in Step 3.
2. Copy the Skill ID and add it to the Lambda function's triggers. This will enable the Lambda function to be invoked from your Alexa skill.

## Step 8: Testing the Skill
1. Select the "Test" tab in the Alexa Developer Console and enable the skill.
2. In the test page's left menu, select "Device Display" and enter a test request. 
3. Confirm that the correct response is displayed.
4. With this, the setup to use ChatGPT in Alexa is complete. Users can now ask questions to ChatGPT through the skill and receive responses.

## Step 9: Using the Skill on Amazon Echo
1. I am currently using the skill as a beta tester on my home Amazon Echo and Alexa app.
2. As beta testing is only valid for 3 months, if there are better alternatives, I would appreciate any suggestions.

## Step 10: Setting Usage Limitations for Each Service (if necessary)
1. I have set up usage limitations for OpenAI's API and configured AWS Budgets to operate within my budget constraints.

## Prompt used to create the setup instructions
```
I want to use ChatGPT on Alexa. I plan to use the following services:
- ChatGPT API
- Alexa Skill
- AWS Lambda

Please explain step-by-step how to achieve this.
```

# How to Use
- Launch the skill and ask a question
  1. Alexa, launch Newton 
  2. {Intelligent, Simple, Normal} El-chan, tell me about delicious beer brands or Translate hogehoge to English/Japanese
- Directly launch the intent and ask a question
  1. Alexa, ask {Intelligent, Simple, Normal} El-chan in Newton about "delicious beer brands"
- If the answer is cut off halfway
  - If you say "Continue," the response will continue.

# Limitations
- Alexa's speech recognition time
  - Alexa only recognizes user speech for 8 seconds, so if your question is too long, the recognition may end prematurely.
  - If you know any good solutions to improve this, I would be grateful for your advice.
- If the answer ends abruptly
  - ~~Saying "Continue" will prompt a continuation of the response, but it may not seamlessly continue or may start with an apology.~~
  - ~~The iPhone's Alexa app perfectly continues the response, but for some reason, it doesn't work well on Android or Amazon Echo.~~
  - ~~If you have any helpful tips, I would appreciate your advice.~~
  - Adding context explicitly in the prompt and directly inject system_content into user_content improved it.

# Example
## Simple El-chan
![image](https://user-images.githubusercontent.com/12249301/231931147-c20f352d-4ff1-40cf-afdd-a7375ff4bc2e.png)
## Intelligent El-chan
![image](https://user-images.githubusercontent.com/12249301/231930862-05d00abd-34b2-465f-86d4-107a6cdb6923.png)

Enjoy your ChatGPT life!
