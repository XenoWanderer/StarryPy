from base_plugin import BasePlugin
from core_plugins.player_manager import UserLevels
import packets


class AdminMessenger(BasePlugin):
    """Adds support to message moderators/admins/owner with a ## prefixed message."""
    name = "admin_messenger"
    depends = ['player_manager']
    auto_activate = True

    def on_chat_sent(self, data):
        data = packets.chat_sent().parse(data.data)
        if data.message[:2] == "##":
            self.message_admins(data)
            return False
        return True

    def message_admins(self, message):
        for protocol in self.protocol.factory.protocols.itervalues():
            if protocol.player.access_level >= UserLevels.MODERATOR:
                protocol.send_chat_message(
                    "Received an admin message from %s: %s." % (self.protocol.player.name,
                                                                message.message[2:]))
                self.logger.info("Received an admin message from %s. Message: %s", self.protocol.player.name,
                                 message.message[2:])
