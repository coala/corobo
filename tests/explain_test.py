import errbot.rendering

from tests.isolated_testcase import IsolatedTestCase
from plugins.explain import Explain


text = errbot.rendering.text()


class ExplainTest(IsolatedTestCase):

    def test_explain(self):
        self.assertCommand('!explain REView', 'For a good review,')
        self.assertCommand('!explain gOOgle', 'use google')
        self.assertCommand('!explain not_found',
                           text.convert(Explain.ERROR_MSG))
        self.assertCommand('!explain review to @meet',
                           '@meet')
        self.assertCommand('!please explain review',
                           'Command \"please\" / \"please explain\" not found.')
