import re

from errbot import BotPlugin, cmdfilter


class Filters(BotPlugin):
    """
    Filter and manipulate incoming commands
    """

    @cmdfilter
    def filters(self, msg, cmd, args, dry_run):
        # Blacklisting commands from specified rooms
        CMDS_TO_BLACKLIST = {
            'coala/coala': ['echo'],
            'coala/coala-bears': ['echo'],
            'coala/corobo': ['echo']
        }

        for room, commands in CMDS_TO_BLACKLIST.items():
            if cmd in commands and msg.frm.room.uri == room:
                return None, None, None
        return msg, cmd, args

    @cmdfilter
    def filter_ignored_users(self, msg, cmd, args, dry_run):
        if msg.frm.nick in self.bot_config.IGNORE_USERNAMES:
            return None, None, None
        return msg, cmd, args
