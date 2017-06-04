import re

from errbot import BotPlugin, botcmd

from plugins import constants


class Searchdocs(BotPlugin):
    """
    Search API and user docs
    """

    API_DOCS = constants.API_DOCS
    USER_DOCS = constants.USER_DOCS

    @botcmd
    def search(self, msg, arg):
        """
        Gives the url of the relevant docs search page with given search string.
        Syntax: `<bot> search api|user here goes the search string.`
        """

        match = re.match(r'((?:api)|(?:user))\s+(.+)', arg, flags=re.IGNORECASE)
        if match is None:
            return ('Invalid syntax, try again. It should be of the form '
                    '`search api|user search string`.')
        doc_type = match.group(1)
        search_string = match.group(2)
        if doc_type.lower() == 'api':
            return (self.API_DOCS +
                    '/search.html?q=' +
                    '+'.join(re.split(r'\s+', search_string)))
        elif doc_type.lower() == 'user':
            return (self.USER_DOCS +
                    '/search.html?q=' +
                    '+'.join(re.split(r'\s+', search_string)))
