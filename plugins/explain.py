import re

from errbot import BotPlugin, re_botcmd


class Explain(BotPlugin):
    """
    Explain various terms
    """

    MSGS = {
        'review': 'After creating your `Pull Request`, it is under the review '
                  'process. This can be deduced from the `process/pending '
                  'review` label. Now you have to wait for the reviewers to '
                  'review your PR. You should *not* ask for reviews on our '
                  'Gitter channel - we review those PRs continuously.\n\n'
                  'We\'re usually swamped with reviews, while you are waiting '
                  '**please review other people\'s PRs** at [coala.io/review]'
                  '(https://coala.io/review): that helps you and will make '
                  'your review happen faster as well. As a rule of thumb, '
                  '*for every review you receive, give at least one review '
                  'to someone else!*\n\nFor a good review, look at every '
                  'commit on its own and place `ack <sha>`(commit is ready) or '
                  '`unack <sha>(commit needs work) needs work` comments on the '
                  'pull request, be sure to remove other spacing like tabs. If '
                  'you\'re done with a pull request, you can use '
                  '`{bot_prefix} mark wip <pull URL>` to mark it *work in '
                  'progress* finally.',
        'closes': 'We use bug prediction in coala which relies on the `Fixes` '
                  'keyword in commit messages. To get good results from that '
                  'we need to use `Closes` for normal issues instead of `Fixes`'
                  ' which should only be used for real bugs. (See also [the '
                  'commit message docs](https://coala.io/commit).) To change '
                  'your message you just use `git commit --amend` and then '
                  '`git push --force` the new commit to replace the old one.',
        'fixes': 'We use bug prediction in coala which relies on the `Fixes` '
                 'keyword in commit messages. To get good results from that '
                 'we need to use `Fixes` for bugfix issues instead of '
                 '`Closes`. (See also [the commit message docs]'
                 '(https://coala.io/commit).) To change your message you '
                 'just use `git commit --amend` and then `git push --force` '
                 'the new commit to replace the old one.',
        'commit message': 'To change your message you just use `git commit '
                          '--amend` and then `git push --force` the new '
                          'commit to replace the old one.\n\nIf you\'re just '
                          'looking to fix an issue very quickly and not '
                          'interested in contributing to coala long term, we '
                          'can fix up the message for you - just tell us :).',
        'rebase': 'It looks like your PR is out of date and needs a rebase.'
                  '\n\n[This page](https://coala.io/rebase) may help you to get'
                  ' started on this. We also have [a quick video tutorial on '
                  'how to rebase](https://asciinema.org/a/78683). That should '
                  'help you understand the basics of how it works and what you'
                  'should be doing.\n\nIf you\'re just looking to fix an issue '
                  'very quickly and not interested in contributing to coala '
                  'long term, we can fix it up for you - just tell us :).',
        'cep': 'At coala we\'re using [cEP\'s (coala Enhancement Proposals)]'
               '(http://coala.io/cep) to define major design decisions - '
               'they\'re a bit like PEP\'s but not quite as extensive and '
               'obviously written with a lower case c.',
        'gitlab': 'We are currently evaluating on if we want to use GitLab for'
                  'code hosting. That\'s why some repositories are already on '
                  'GitLab, if you want to participate in the migration '
                  'discussion, please add information [at our GitLab wiki page]'
                  '(https://github.com/coala/coala/wiki/GitLab).',
        'google': 'Hey. This message was triggered because someone was too '
                  'lazy to type this *again*. Don\'t take it personally. '
                  'Please.\n\nWe all got to learn this: *use google*. Or '
                  'duckduckgo. Anything. The search engine that earned your '
                  'trust. You got a build error? Search for the first red '
                  'thing and google it. You got an exception? *Read the '
                  'message.* Search it. *Think.*\n\nKeep this in mind: *You*'
                  'are sitting in front of the problem, not us. You will have '
                  'a much easier time solving it. That\'s why you should try '
                  'doing it first.',
        'promotion': 'To become part of the coala developers team, there '
                     'are a few steps you need to complete. The newcomer '
                     'process is as follows:\nYou will start as a newcomer, '
                     'which is kind of a trial. If you complete the following '
                     'tasks, you will become a developer at coala:\n\n- run '
                     'coala on a project of yours\n- merge a difficulty/'
                     'newcomer Pull Request\n- review at least a difficulty/'
                     'newcomer Pull Request\n- merge a difficulty/low Pull '
                     'Request\n- review at least a difficulty/low or higher '
                     'Pull Request'
    }

    ERROR_MSG = (
        'Sorry, I only know about these things:\n- ' +
        '\n- '.join(MSGS.keys())
    )

    @re_botcmd(pattern=r'explain\s+(\w+)(?:\s+to\s+@?([\w-]+))?',
               re_cmd_name_help='explain <term>',
               flags=re.IGNORECASE)
    def explain(self, msg, match):
        """Explain various terms."""  # Ignore QuotesBear
        return ('{}'.format('@{}: \n'.format(match.group(2))
                            if match.group(2) else '') +
                self.MSGS.get(
                    match.group(1).lower(),
                    self.ERROR_MSG
                ).format(bot_prefix=self.bot_config.BOT_PREFIX))
