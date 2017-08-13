import json
import os
from urllib.parse import quote_plus, urljoin

from errbot import BotPlugin, botcmd
import requests


class Answer(BotPlugin):

    # Ignore LineLengthBear, PyCodestyleBear
    SURVEY_LINK = 'https://docs.google.com/forms/d/e/1FAIpQLSdQSWtGa6SsUb14h8fkhhZjz6rvPg6sIU31bJpbFz1RNJi4Og/viewform?usp=pp_url&entry.1041743666={question}&entry.2054411228={response}&entry.1180476220={message_link}'
    MESSAGE_LINK = 'https://gitter.im/{uri}?at={idd}'

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
            reply = requests.post(urljoin(os.environ['ANSWER_END'],
                                          'summarize'),
                                  data={'text': answers[0][0]}).json()['res']
            # Ignore InvalidLinkBear
            reply += '\n' + 'You can read more here: {}'.format(
                type(self).construct_link(answers[0][0].splitlines()[-1])
            )
            try:
                reply += ('\n\nPlease fill in [this]({}) form to rate the '
                          'answer'.format(self.SURVEY_LINK.format(
                                    question=quote_plus(arg),
                                    response=quote_plus(reply),
                                    message_link=self.MESSAGE_LINK.format(
                                        uri=msg.frm.room.uri,
                                        idd=msg.extras['id'])
                                )
                            )
                          )
            except AttributeError:  # pragma: no cover
                # Test backend doesn't have room attribute
                pass
            yield reply
        else:
            yield 'Dunno'
