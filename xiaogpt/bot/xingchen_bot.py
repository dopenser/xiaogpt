from __future__ import annotations

from typing import Any

from xiaogpt.bot.base_bot import BaseBot, ChatHistoryMixin
from xingchen import Configuration, ApiClient, ChatApiSub, ChatReqParams, ChatContext, CharacterKey, Message, UserProfile, ModelParameters


class xingchenBot(ChatHistoryMixin, BaseBot):
    name = "xingchen"

    def __init__(self, xingchen_key: str) -> None:
        self.history = []
        self.configuration = Configuration(host="https://nlp.aliyuncs.com")
        self.configuration.access_token = xingchen_key
        self.api = self.init_client()

    @classmethod
    def from_config(cls, config):
        return cls(xingchen_key=config.xingchen_key)

    def init_client(self):
        with ApiClient(self.configuration) as api_client:
            return ChatApiSub(api_client)

    async def ask(self, query, **options):
        chat_param = self.build_chat_param(query)
        response = self.api.chat(chat_param)
        if response.success and response.data.choices:
            # 获取第一个选择的第一个消息的content字段
            content = response.data.choices[0].messages[0].content
            self.history.append(content)
            print(content)
            return content
        else:
            return "没有返回"

    async def ask_stream(self, query: str, **options: Any):
        chat_param = self.build_chat_param(query)
        chat_param.streaming = True
        responses = self.api.chat(chat_param)
        full_content = ""
        for res in responses:
            if res.success and res.data.choices:
                content = res.data.choices[0].messages[0].content
                full_content += content
                yield content
                print(content)
            else:
                break
        self.history.append(full_content)

    def build_chat_param(self, query: str):
        return ChatReqParams(
            bot_profile=CharacterKey(character_id="9cd8f5e344704beaa8e079e316f9aef7"),
            model_parameters=ModelParameters(seed=1683806810, incrementalOutput=False),
            messages=[
                Message(name='11', role='user', content=query),
            ],
            context=ChatContext(use_chat_history=True),
            user_profile=UserProfile(user_id='1256', user_name='测户')
        )