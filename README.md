# corobo

[![Travis branch](https://img.shields.io/travis/coala/corobo/master.svg)](https://travis-ci.org/coala/corobo)
[![Codecov branch](https://img.shields.io/codecov/c/github/coala/corobo/master.svg)](https://codecov.io/gh/coala/corobo)
[![Semaphore branch](https://semaphoreci.com/api/v1/coala/corobo/branches/master/badge.svg)](https://semaphoreci.com/coala/corobo)

## Setup

1. Install the dependencies
   `pip install -r requirements.txt`

2. Set environment variables `COBOT_ROOT`, `COBOT_TOKEN` to the path of corobo
   repo and gitter token for cobot.

3. Run errbot: `cd COBOT_ROOT &&  errbot`

## Environment Variables

1. `COBOT_ROOT` - absolute path of the project root.
2. `COBOT_PREFIX` - prefix to use for issuing bot commands.
3. `GH_TOKEN` - GitHub personal access token to create issues, invite people to
   org, assign and unassign issues, etc.
4. `GL_TOKEN` - GitLab personal access token to create, assign, unassign
   issues, etc.
5. `WA_TOKEN` - wolframalpha APP_ID to access wolfram API.
