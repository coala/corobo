from collections import OrderedDict
import json
import textwrap

import requests
from ramlient import Client

from errbot import BotPlugin, re_botcmd

client = Client('webservices.raml')


class Coatils(BotPlugin):
    """
    Various coala related utilities, exposing the REST API, etc.
    """

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

    @re_botcmd(pattern=r'(?:(contrib|bear|lang)\s+)?stats(.+)?(?:(?:\s+)|$)',
               re_cmd_name_help='(contrib|bear|lang) stats [username|language]')
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

    @re_botcmd(pattern=r'ls\s+bears\s+((?:[\w\+]+(?:\s+)?)+)',
               re_cmd_name_help='ls bears [langs]+')
    def ls(self, msg, match):
        """
        List bears of given languages:
        Example: `ls bears python python3`
        """
        langs = list(map(lambda x: x.lower(), match.group(1).split()))

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

    @staticmethod
    def construct_settings(settings):
        settings = settings.strip().split()

        def is_setting(x): return '=' in x  # Ignore PycodestyleBear (E731)
        setting_dict = OrderedDict()
        for candidate in settings:
            if not is_setting(candidate):  # bear
                setting_dict[candidate.strip()] = dict()
            else:
                key, value = candidate.strip().split('=')
                setting_dict[list(setting_dict.keys())[-1]][key] = value
        return setting_dict

    @staticmethod
    def position(stl, stc, enl, enc):
        if stc is None and enc is None:
            if stl != enl:
                return 'Between lines {} and {}'.format(stl, enl)
            else:
                return 'At line {}'.format(stl)
        if stc is None and enc is not None:
            return 'Between line {} and position {}:{}'.format(stl, enl, enc)
        if stc is not None and enc is None:
            return 'Between position {}:{} and line {}'.format(stl, stc, enl)
        if stl == enl:
            if stc == enc:
                return "At {}:{}".format(stl, stc)
            else:
                return "At line {}, between col {} and {}".format(stl, stc, enc)
        else:
            return "Between positions {}:{} and {}:{}".format(stl, stc,
                                                              enl, enc)

    # Ignore PycodestyleBear, LineLengthBear
    @re_botcmd(pattern=r'^run\s+(\w+)((?:\s+\w+(?:\s+\w+=\w+)*)+)\n+```\n([\s\S]+)\n```$',
               re_cmd_name_help='run <Bear [[setting=value]+]>+\n'
                                '```\n<code>+\n```')
    def run(self, msg, match):
        """
        Run coala over the given code.

        Example: `run Bear1 setting1=something setting2=something Bear2\ncode`
        """
        lang = match.group(1)
        bear_settings = type(self).construct_settings(match.group(2))
        code = match.group(3) + ('\n' if not match.group(3).endswith('\n')
                                 else '')

        yield 'coala analysis in progress...'

        data = {
            "sections": {
                "corobo": {
                    "files": "**.gyp",
                    "bears": dict(bear_settings),
                }
            },
            "mode": "coala",
            "language": lang,
            "file_data": code,
        }

        # Ignore InvalidLinkBear, this only accepts post requests
        rq = requests.post('https://api.gitmate.io/coala_online/', json=data)
        try:
            results = rq.json()['response']['results']['corobo']
        except json.JSONDecodeError:
            went_wrong = '\n - '.join([
                'Is the bear name correct? Note that bear names are '
                'case sensitive.'
                'Are all required settings provided? If a required setting is '
                'not provided, analysis will fail.'
            ])
            yield 'Something went wrong, things to check for:\n' + went_wrong
            self.log.exception('Something went wrong, please try again')
        else:
            if not results:
                yield 'Your code is flawless :tada:'
                return
            result_message = 'Here is what I think is wrong: \n'
            for result in results:
                affected_area = []
                for afc in result['affected_code']:
                    affected_area.append((afc['start']['line'],
                                          afc['start']['column'],
                                          afc['end']['line'],
                                          afc['end']['column']))

                afm = '\n'.join([Coatils.position(stl, stc, enl, enc)
                                 for (stl, stc, enl, enc) in affected_area])

                message = result['message']
                origin = result['origin']
                diffs = []
                if result['diffs']:
                    for _, diff in result['diffs'].items():
                        diffs.append(diff)

                diff_message = ''
                if diffs:
                    diff_message += ('These patches can help solve the '
                                     'issue: \n')
                    for diff in diffs:
                        diff = ''.join(diff.splitlines(True)[2:])
                        diff_message += '```diff\n{}```\n'.format(
                            textwrap.indent(diff, '   ')
                        )

                result_message += '- {} - {} :\n{}{diff}\n'.format(
                    origin, afm, message, diff=diff_message
                )

            yield result_message
