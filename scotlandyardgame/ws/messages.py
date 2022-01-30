class Messages:
    """Generic messages"""
    @staticmethod
    def LOS(player_id: str):
        """report LOS"""
        return f"LOS {player_id}"

    @staticmethod
    def abort():
        """abort game"""
        return f"ABORT"

    @staticmethod
    def remove(player_id: str):
        """remove player from lobby"""
        return f"DISCONNECT {player_id}"

    @staticmethod
    def setHost(player_id: str) -> dict:
        """set player to lobby host"""
        return f"SET_HOST {player_id}"

    @staticmethod
    def setMrX(player_id: str) -> dict:
        """set player to Mr. X for the lobby"""
        return f"SET_MRX {player_id}"

