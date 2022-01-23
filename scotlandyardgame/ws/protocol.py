from __future__ import annotations
from typing import Callable

from .WebSocketConsumer import WebSocketConsumer


class Protocol:
    def __init__(self, consumer: WebSocketConsumer, fmap: dict[str, Callable]) -> None:
        self.__handlers = fmap
        self.__consumer = consumer

    async def process(self, msg: str) -> None:
        """parse incoming ws client message"""
        tokens = msg.split()
        keyword = tokens[0]

        if keyword not in self.__handlers:
            raise ValueError(f"invalid message: {msg}")

        await self.__handlers[keyword](*(tokens[1:] if len(tokens) > 1 else []))

    def send(self, msg: str):
        return self.__consumer.send(msg)

    def group_send(self, msg: str):
        return self.__consumer.channel_layer.group_send(
            self.__consumer.game_id, {"type": "ws.send", "text": msg})
