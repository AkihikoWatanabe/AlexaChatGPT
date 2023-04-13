import json
import openai
import os
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import get_slot_value, is_intent_name, is_request_type
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard


sb = SkillBuilder()

reprompt_text = 'チャットGPTへの問い合わせ内容を教えてください。'
system_content = "あなたは物事をわかりやすく興味深く説明する専門家です。また、以下のキャラクター設定に沿って質問に回答してください。\n\n#キャラクター設定 あなたはウサギを模したキャラクターであり、気分屋で能天気な性格で、とってもかわいいキャラクターです。\n回答する際はこのキャラクターが発話するようなトーンで回答してください。\n回答中の全ての文末が必ず印象的な語尾で終わるように回答をします。\n印象的な語尾については、あなたが考えてください。"


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "チャットGPTへの問い合わせ内容を教えてください。"

    handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_card(
        SimpleCard("chatGPT", speech_text)).set_should_end_session(
        False)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AskSimpleGPTIntent"))
def ask_simple_gpt_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    prompt = get_slot_value(handler_input=handler_input, slot_name="Prompt")
   
    openai.api_key = os.environ["OPENAI_API_KEY"]
    user_content = f' #質問 以下について教えてください """{prompt} シンプルに回答してみよう。"""'

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
    )

    response_text = response.choices[0]['message']['content'].strip()
    session_attr = handler_input.attributes_manager.session_attributes

    if 'messages' in session_attr:
        session_attr['messages'] += [
            {'role': 'user', 'content': user_content},
            {'role': 'assistant', 'content': response_text}]
    else:
        session_attr['messages'] = [
            {'role': 'system', 'content': system_content},
            {'role': 'user', 'content': user_content},
            {'role': 'assistant', 'content': response_text}]

    handler_input.response_builder.speak(response_text).ask(reprompt_text).set_card(
        SimpleCard("chatGPT", response_text)).set_should_end_session(False)

    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AskNormalGPTIntent"))
def ask_normal_gpt_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    prompt = get_slot_value(handler_input=handler_input, slot_name="Prompt")
   
    openai.api_key = os.environ["OPENAI_API_KEY"]
    user_content = f' #質問 以下について教えてください """{prompt}"""'

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
    )

    response_text = response.choices[0]['message']['content'].strip()
    session_attr = handler_input.attributes_manager.session_attributes

    if 'messages' in session_attr:
        session_attr['messages'] += [
            {'role': 'user', 'content': user_content},
            {'role': 'assistant', 'content': response_text}]
    else:
        session_attr['messages'] = [
            {'role': 'system', 'content': system_content},
            {'role': 'user', 'content': user_content},
            {'role': 'assistant', 'content': response_text}]

    handler_input.response_builder.speak(response_text).ask(reprompt_text).set_card(
        SimpleCard("chatGPT", response_text)).set_should_end_session(False)

    return handler_input.response_builder.response


# using zero-shot CoT
@sb.request_handler(can_handle_func=is_intent_name("AskGPTIntent"))
def ask_gpt_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    prompt = get_slot_value(handler_input=handler_input, slot_name="Prompt")
   
    openai.api_key = os.environ["OPENAI_API_KEY"]
    user_content = f' #質問 以下について教えてください """{prompt}。段階的に、論理的に考えてみてください。'

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
    )

    response_text = response.choices[0]['message']['content'].strip()
    session_attr = handler_input.attributes_manager.session_attributes

    if 'messages' in session_attr:
        session_attr['messages'] += [
            {'role': 'user', 'content': user_content},
            {'role': 'assistant', 'content': response_text}]
    else:
        session_attr['messages'] = [
            {'role': 'system', 'content': system_content},
            {'role': 'user', 'content': user_content},
            {'role': 'assistant', 'content': response_text}]

    handler_input.response_builder.speak(response_text).ask(reprompt_text).set_card(
        SimpleCard("chatGPT", response_text)).set_should_end_session(False)

    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("ContinueIntent"))
def continue_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    openai.api_key = os.environ["OPENAI_API_KEY"]

    user_content = '前回のあなたの途中で途切れた発話に対して文法的に正しい形で、回答の続きを述べてください。'

    messages = [{"role": 'user', "content": user_content}]

    session_attr = handler_input.attributes_manager.session_attributes
    if "messages" in session_attr:
        prev_messages = session_attr["messages"]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prev_messages + messages,
            max_tokens=100,
        )

        response_text = response.choices[0]['message']['content'].strip()
        session_attr['messages'] += [
                {"role": 'user', "content": user_content},
                {"role": 'assistant', "content": response_text}
        ]
        handler_input.response_builder.speak(response_text).set_card(
            SimpleCard("chatGPT", response_text)).set_should_end_session(False).ask(reprompt_text)

    else:
        response_text = 'まず何か質問をしてみてね。'
        handler_input.response_builder.speak(response_text).ask(reprompt_text).set_card(
                SimpleCard("chatGPT", response_text)).set_should_end_session(False)


    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("TranslateEnglishIntent"))
def translate_english_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    prompt = get_slot_value(handler_input=handler_input, slot_name="Prompt")

    openai.api_key = os.environ["OPENAI_API_KEY"]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは日英翻訳の専門家です。"},
            {"role": "user", "content": f'次の日本語テキストを英語に翻訳してください。"""{prompt}"""'}
        ]
    )

    response_text = response.choices[0]['message']['content'].strip()

    
    handler_input.response_builder.speak(response_text).ask(reprompt_text).set_card(
        SimpleCard("chatGPT", response_text)).set_should_end_session(False)


    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("TranslateJapaneseIntent"))
def translate_japanese_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    prompt = get_slot_value(handler_input=handler_input, slot_name="Prompt")
   
    openai.api_key = os.environ["OPENAI_API_KEY"]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in English to Japanese translation. "},
            {"role": "user", "content": f'Please translate the following text into Japanese. """{prompt}"""'}
        ]
    )

    response_text = response.choices[0]['message']['content'].strip()
    
    handler_input.response_builder.speak(response_text).ask(reprompt_text).set_card(
        SimpleCard("chatGPT", response_text)).set_should_end_session(False)


    return handler_input.response_builder.response



@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "チャットGPTに何か質問してみてください。"

    handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_card(
        SimpleCard("chatGPT", speech_text))
    return handler_input.response_builder.response
    

@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "何かあったらまた呼んでください。"

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("chatGPT", speech_text))
    return handler_input.response_builder.set_should_end_session(True).response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    # type: (HandlerInput) -> Response

    return handler_input.response_builder.set_should_end_session(True).response
    
    
@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    # type: (HandlerInput, Exception) -> Response
    print(exception)

    speech = "すみません、わかりませんでした。もう一度言ってください。"
    handler_input.response_builder.speak(speech).ask(reprompt_text).set_should_end_session(False)

    return handler_input.response_builder.response


handler = sb.lambda_handler()
