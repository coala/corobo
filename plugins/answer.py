import json
import os
from urllib.parse import quote, urljoin

from errbot import BotPlugin, botcmd
import requests


class Answer(BotPlugin):

    @staticmethod
    def construct_link(text):
        if 'coala/docs/' in text:
            text = text.split('coala/docs/')[-1]
            return 'https://api.coala.io/en/latest/' + text
        elif 'documentation/' in text:
            text = text.split('documentation/')[-1]
            return 'https://docs.coala.io/en/latest/' + text

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
            yield requests.post(urljoin(os.environ['ANSWER_END'],  'summarize'),
                                json={'text': answers[0][0]}).json()['res']
            # Ignore InvalidLinkBear
            yield 'You can read more here: {}'.format(
                type(self).construct_link(answers[0][0].splitlines()[-1])
            )
        else:
            yield 'Dunno'
