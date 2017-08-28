#!/usr/bin/env python3

"""
Check if the docker image for answers package/microservice has to be built.
"""

import logging
import os

import git

repo = git.Repo()
answers_module_files = list(map(lambda x: os.path.join('answers', x),
                                os.listdir('answers')))

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

repo.remote('origin').fetch('master')
# New commits
commits_diff = repo.git.log('origin/master..{}'.format(repo.active_branch.name),
                            pretty='%H').splitlines()
logging.info('Commits diff: {}'.format(commits_diff))

for sha in commits_diff:
    logging.info('Files changed: {}'.format(repo.commit(sha).stats.files.keys()))
    if any(map(lambda x: x in answers_module_files,
               repo.commit(sha).stats.files.keys())):
        logging.info('answer package files changed in {}'.format(sha))
        exit(1)
    else:
        logging.info('answer package files not changed in {}'.format(sha))
exit(0)
