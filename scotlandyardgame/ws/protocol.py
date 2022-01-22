from __future__ import annotations

from .WebSocketConsumer import WebSocketConsumer


class Protocol:
    def __init__(self, consumer: WebSocketConsumer, fmap: dict[str, function]) -> None:
        self.__handlers = fmap
        self.__consumer = consumer
        self.game_id = consumer.game_id

    async def process(self, msg: str) -> None:
        """parse incoming ws client message"""
        tokens = msg.split()
        keyword = tokens[0]

        if keyword not in self.__handlers:
            raise ValueError(f"invalid message: {msg}")

        await self.__handlers[keyword](*(tokens[1:] if len(tokens) > 1 else []))

    def send(self, msg: str):
        self.__consumer.send(msg)

    def group_send(self, msg: str):
        self.__consumer.channel_layer.group_send(
            self.__consumer.game_id, {"type": "ws.send", "text": msg})
