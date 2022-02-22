from __future__ import annotations

from typing import Callable

from .WebSocketConsumer import WebSocketConsumer


class Protocol:
    """
    The protocol classes are used to parse incoming messages from the client, and then process them with the appropriate handler.
    """

    def __init__(self, consumer: WebSocketConsumer, fmap: dict[str, Callable]) -> None:
        self.handlers = fmap
        self.consumer = consumer

    async def process(self, msg: str) -> None:
        """parse incoming ws client message"""
        msg = msg.strip()
        tokens = msg.split()

        if len(tokens) < 1:
            return

        keyword = tokens[0].upper()

        if keyword not in self.handlers:
            await self.send(f"ERROR - invalid message: {keyword}")
            return

        try:
            await self.handlers[keyword](*(tokens[1:] if len(tokens) > 1 else []))
        except Exception as e:
            await self.send(f"ERROR - {e}")

    def send(self, msg: str):
        return self.consumer.send(msg)

    def group_send(self, msg: str):
        return self.consumer.channel_layer.group_send(
            self.consumer.type + "_" + self.consumer.game_id,
            {"type": "ws.send", "text": msg},
        )
