import os

import requests
from ramlient import Client

from errbot import BotPlugin, re_botcmd

client = Client('webservices.raml')


class Coatils(BotPlugin):
    """
    Various coala related utilities, exposing the REST API, etc.
    """

    def __init__(self, bot, name=None):
        super().__init__(bot, name)

    @staticmethod
    def total_bears():
        bears = client.list.bears.get().json()
        return len(bears.keys())

    @staticmethod
    def all_langs():
        bears = client.list.bears.get().json()
        langs_list = list(map(lambda x: x['languages'], bears.values()))
        all_langs = []
        for ls in langs_list:
            for lang in ls:
                all_langs.append(lang)

        return set(all_langs)

    @re_botcmd(pattern=r'(?:(contrib|bear|lang)\s+)?stats(.+)?(?:(?:\s+)|$)')
    def contrib_stats(self, msg, match):
        """
        Allowed commands:
        - contrib stats <username>
        - bear stats
        - bear stats <language>
        - lang stats
        - stats
        """

        stat_type = match.group(1).strip() if match.group(1) else ''
        entity = match.group(2).strip() if match.group(2) else ''

        # contrib stats user
        if stat_type == 'contrib' and entity != '':
            try:
                res = list(
                        filter(
                            lambda x: x['login'].lower() == entity.lower(),
                            client.contrib.get().json()
                        ))[0]
            except IndexError:
                yield 'stats for {} not found'.format(entity)
                return

            commits = res['contributions']
            issues = res['issues']
            reviews = res['reviews']

            success = ('User {} has:\n'
                       '1. Opened {} issues\n'
                       '2. Commited {} commits\n'
                       '3. Done {} reviews'.format(entity, issues,
                                                   commits, reviews))

            yield success

        # bear stats
        elif stat_type == 'bear' and entity == '':
            yield 'There are total {} bears.'.format(Coatils.total_bears())
        # bear stats lang
        elif stat_type == 'bear' and entity != '':
            bears = client.list.bears.get().json()
            all_langs = Coatils.all_langs()
            if entity in map(lambda x: x.lower(), all_langs):
                selected_bears = filter(lambda x: entity in list(map(
                                            lambda y: y.lower(), x['languages']
                                        )),
                                        bears.values())
                yield 'There are {} bears for {} language'.format(
                    len(list(selected_bears)), entity
                )
            else:
                yield 'No bear exists for {} language'.format(entity)
        # lang stats
        elif stat_type == 'lang' and entity == '':
            yield 'coala supports {} languages'.format(
                len(Coatils.all_langs())
            )
        # stats
        elif stat_type == '' and entity == '':
            yield ('coala has {} bears across {} languages'
                   ''.format(Coatils.total_bears(),
                             len(Coatils.all_langs())))

    @re_botcmd(pattern=r'ls\s+bears\s+((?:[\w\+]+(?:\s+)?)+)')
    def ls(self, msg, match):
        """
        List bears of given languages:
        Example: `ls bears python python3`
        """
        langs = list(map(lambda x: x.lower(), match.group(1).split()))
        all_langs = Coatils.all_langs()

        bears = client.list.bears.get().json()
        bears = [{**{'name': bear}, **content}
                 for bear, content in bears.items()]

        for lang in langs:
            selected_bears = [
                ' | ' + bear['name'] for bear in filter(lambda x: lang in list(
                    map(lambda y: y.lower(), x['languages'])),
                    bears
                )
            ]

            if selected_bears:
                yield 'Bears for {} are: '.format(lang)
                yield ''.join(selected_bears) + ' |'
            else:
                yield 'No bears found for {}'.format(lang)
