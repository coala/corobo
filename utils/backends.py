"""
Handle backend specific implementations.
"""

def message_link(bot, msg):
    """
    :param bot: Plugin instance.
    :param msg: Message object.
    :returns:   Message link.
    """
    backend = bot.bot_config.BACKEND.lower()
    if backend == 'gitter':
        return 'https://gitter.im/{uri}?at={idd}'.format(uri=msg.frm.room.uri,
                                                         idd=msg.extras['id'])
    elif backend == 'slack':
        return msg.extras['url']
    elif backend == 'telegram':
        return ''
    elif backend == 'text':
        return ''
    else:
        raise NotImplementedError
