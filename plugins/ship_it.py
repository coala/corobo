import random
import re

from errbot import BotPlugin, re_botcmd


class Ship_it(BotPlugin):
    """
    Show motivational ship it squirrel images.
    """

    # start ignoring LineLengthBear PyCodeStyleBear
    IMAGES = [
        'http://i.imgur.com/DPVM1.png',
        'http://d2f8dzk2mhcqts.cloudfront.net/0772_PEW_Roundup/09_Squirrel.jpg',
        'http://www.cybersalt.org/images/funnypictures/s/supersquirrel.jpg',
        'http://www.zmescience.com/wp-content/uploads/2010/09/squirrel.jpg',
        'https://dl.dropboxusercontent.com/u/602885/github/sniper-squirrel.jpg',
        'http://1.bp.blogspot.com/_v0neUj-VDa4/TFBEbqFQcII/AAAAAAAAFBU/E8kPNmF1h1E/s640/squirrelbacca-thumb.jpg',
        'https://dl.dropboxusercontent.com/u/602885/github/soldier-squirrel.jpg',
        'https://dl.dropboxusercontent.com/u/602885/github/squirrelmobster.jpeg',
    ]
    # stop ignoring LineLengthBear PyCodeStyleBear

    @re_botcmd(pattern=r'ship\s*it', flags=re.IGNORECASE)
    def ship_it(self, msg, match):
        """
        Show motivational ship it squirrel images.
        """
        return ':shipit: ![ship it!]({})'.format(
            self.IMAGES[random.randint(0, len(self.IMAGES) - 1)]
        )
