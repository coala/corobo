from tests.isolated_testcase import IsolatedTestCase


class SearchDocsTest(IsolatedTestCase):

    def test_search_cmd(self):
        self.assertCommand(
            '!search api search string',
            'http://api.coala.io/en/latest/search.html?q=search+string')
        self.assertCommand(
            '!search user search string',
            'http://docs.coala.io/en/latest/search.html?q=search+string')
        self.assertCommand('!search not matching',
                           'Invalid syntax')
