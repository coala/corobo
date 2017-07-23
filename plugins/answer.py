import json
import os
from urllib.parse import quote, urljoin

from errbot import BotPlugin, botcmd
import requests


class Answer(BotPlugin):

    @botcmd
    def answer(self, msg, arg):
        try:
            answers = requests.get(urljoin(os.environ['ANSWER_END'], 'answer'),
                                   params={'question': arg}).json()
        except json.JSONDecodeError:  # pragma: no cover # for logging
            self.log.exception('something went wrong while fetching answer for'
                               'question: {}'.format(arg))
            yield 'Something went wrong, please check logs'.format()
        if answers:
            yield requests.get(urljoin(os.environ['ANSWER_END'],  'summarize'),
                               params={'text': answers[0][0]}).json()['res']
            # Ignore InvalidLinkBear
            doc_link = 'https://api.coala.io/en/latest/Developers/' + \
                answers[0][0].splitlines()[-1]
            yield 'You can read more here: {}'.format(doc_link)
        else:
            yield 'Dunno'
