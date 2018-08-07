import github3
import IGitt
import plugins.labhub

from unittest.mock import create_autospec, PropertyMock
from tests.corobo_test_case import CoroboTestCase


class LabHubTestCase(CoroboTestCase):

    def setUp(self, klasses=None):
        plugins.labhub.github3 = create_autospec(github3)

        self.mock_org = create_autospec(github3.orgs.Organization)
        self.mock_gh = create_autospec(github3.GitHub)
        self.mock_team = create_autospec(github3.orgs.Team)
        self.mock_team.name = PropertyMock()
        self.mock_team.name = 'mocked team'
        self.teams = {
            'coala newcomers': self.mock_team,
            'coala developers': self.mock_team,
            'coala maintainers': self.mock_team,
        }

        self.mock_repo = create_autospec(IGitt.GitHub.GitHub.GitHubRepository)

        plugins.labhub.github3.login.return_value = self.mock_gh
        self.mock_gh.organization.return_value = self.mock_org
        self.mock_org.teams.return_value = [self.mock_team]
        plugins.labhub.github3.organization.return_value = self.mock_org

        # patching
        plugins.labhub.GitHub = create_autospec(IGitt.GitHub.GitHub.GitHub)
        plugins.labhub.GitLab = create_autospec(IGitt.GitLab.GitLab.GitLab)
        plugins.labhub.GitHubToken = create_autospec(IGitt.GitHub.GitHubToken)
        plugins.labhub.GitLabPrivateToken = create_autospec(
            IGitt.GitLab.GitLabPrivateToken)

        if klasses:
            super().setUp(klasses)
