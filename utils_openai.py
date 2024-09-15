"""
Utilities for using OpenAI Chat API.
- Includes tools for creating conversation histories, getting chat completions, and tool calling.
"""

from dotenv import load_dotenv
from openai import OpenAI
from typing import Literal, Optional

load_dotenv()

### Chats ###

class Messages():

    def __init__(self):
        self.messages = []

    def clear(self):
        self.messages = []

    def keep_last(self, n: int):
        """Drop all but the last n messages."""
        self.messages = self.messages[-n:]

    def add_message(self, role: Literal['user', 'assistant', 'system'], message: str):
        message = {"role": role, "content": message}

        if role == 'system':
            # remove any system message(s) in the messages
            self.messages = [d for d in self.messages if 'system' not in d]
            # insert the system message at the beginning of the messages
            self.messages.insert(0, message)
        else:
            # append the message to the end of the messages
            self.messages.append(message)

class ChatBot():

    def __init__(self):
        self.conversation = Messages()
        self.model = 'gpt-4o'

    def set_system_message(self, message: str):
        self.conversation.add_message('system', message)

    def add_comment(self, comment: str):
        # Add a user message to the conversation but don't send it to the ai
        self.conversation.add_message('user', comment)

    def get_reply(self, temperature = 0.0):
        # Send the current conversation to the ai and get its reply.
        # Add it's reply to the conversation history
        completion = OpenAI().chat.completions.create(
                                                model=self.model,
                                                temperature=temperature,
                                                messages=self.conversation.messages,
                                                )
        reply = completion.choices[0].message.content
        tools = completion.choices[0].message.tool_calls

        self.conversation.add_message('assistant', reply)

        return reply

    def comment_reply(self, comment: str, temperature = 0.0):
        # Send a user comment to the ai for a reply.
        # Both the user comment and the ai reply will be recorded in the message history
        # Return the reply
        self.add_comment(comment)
        return self.get_reply(temperature)
        