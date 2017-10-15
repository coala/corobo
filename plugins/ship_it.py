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
    ]
    # stop ignoring LineLengthBear PyCodeStyleBear

    @re_botcmd(pattern=r'ship\s*it',
               re_cmd_name_help='ship it',
               flags=re.IGNORECASE)
    def ship_it(self, msg, match):
        """
        Show motivational ship it squirrel images.
        """
        return '![ship it!]({})'.format(
            self.IMAGES[random.randint(0, len(self.IMAGES) - 1)]
        )
