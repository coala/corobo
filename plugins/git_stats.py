import datetime
import re
from shutil import rmtree

from errbot import re_botcmd

from plugins.labhub import LabHub


class GitStats(LabHub):
    """GitHub and GitLab statistics"""  # Ignore QuotesBear

    PR_LABELS = ('process/approved',
                 'process/pending review',
                 'process/pending-review'
                 )

    def __init__(self, bot, name=None):
        super().__init__(bot, name)

    @re_botcmd(pattern=r'mergable\s+([^/]+)',  # Ignore PyCodeStyleBear
               re_cmd_name_help='pr list <repo>',
               flags=re.IGNORECASE)
    def pr_list(self, msg, match):
        """List PRs ready to be merged."""  # Ignore QuotesBear
        repo_name = match.groups(1)[0]

        try:
            merge_requests = self.REPOS[repo_name].merge_requests()
        except KeyError:
            return "Repository doesn't exist."

        checks = []

        def check_mr(func):
            checks.append(func)
            return func

        @check_mr
        def check_labels(merge_request):
            labels = set(merge_request.labels)
            if labels.intersection(self.PR_LABELS):
                return True
            return False

        @check_mr
        def check_state(merge_request):
            if merge_request.state == 'open':
                return True
            return False

        @check_mr
        def check_rebased(merge_request):
            repo, tempdir = merge_request.repository.get_clone()
            head_sha = repo.head.commit.hexsha
            rmtree(tempdir)
            if merge_request.base.sha == head_sha:
                return True
            return False

        def merge_ready(merge_request):
            for chk in checks:
                if not chk(merge_request):
                    return False
            return True

        ready_to_merge = []
        for mr in merge_requests:
            if merge_ready(mr):
                ready_to_merge.append(mr)
        if len(ready_to_merge) == 0:
            return "No merge-ready PRs!"
        else:
            now = datetime.datetime.now()
            response = "PRs ready to be merged:\n\n"
            for mr in sorted(ready_to_merge, key=lambda x: now - x.created):
                response += '{}\n'.format(mr.url)
            return response
