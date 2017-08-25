# corobo

[![Travis branch](https://img.shields.io/travis/coala/corobo/master.svg)](https://travis-ci.org/coala/corobo)
[![Codecov branch](https://img.shields.io/codecov/c/github/coala/corobo/master.svg)](https://codecov.io/gh/coala/corobo)
[![Semaphore branch](https://semaphoreci.com/api/v1/coala/corobo/branches/master/badge.svg)](https://semaphoreci.com/coala/corobo)
[![Gitter Room](https://img.shields.io/badge/gitter-join%20chat%20%E2%86%92-brightgreen.svg)](https://gitter.im/coala/corobo)
## Environment Variables

1. `COBOT_ROOT` - absolute path of the project root.
2. `COBOT_PREFIX` - prefix to use for issuing bot commands.
3. `BOT_ADMINS` - Admins of the errbot instance.
4. `ROOMS` - Space separated list of rooms to join on startup. e.g.
   `ROOMS="coala/coala coala/coala/corobo"`
5. `BACKEND` - Backend to use, default is Gitter.
6. `GH_TOKEN` - GitHub personal access token to create issues, invite people to
   org, assign and unassign issues, etc. - Mandatory for LabHub to work for
   GitHub.
7. `GL_TOKEN` - GitLab personal access token to create, assign, unassign
   issues, etc. - Mandatory for LabHub to work for GitLab.
8. `GH_ORG_NAME` - Name of github organization - Mandatory for LabHub GitHub
9. `GL_ORG_NAME` - Name of gitlab organization - Mandatory for LabHub GitLab
10. `WA_TOKEN` - wolframalpha APP_ID to access wolfram API.
11. `IGNORE_USERNAMES` - space separated list of usernames to ignore messages
    from.

## Environment Variables for answers microservice

1. `ANSWER_END` - Endpoint of `answers` microservice(in `answers/` directory). It is exposed at port
   `8000`.

## Setup without docker

1. Install the dependencies
   `pip install -r requirements.txt`
2. Set environment variables `COBOT_ROOT`, `COBOT_TOKEN` to the path of corobo
   repo and gitter token for cobot. Set other environment variables mentioned
   above if required
3. Run errbot: `cd COBOT_ROOT &&  errbot`

## Setup with docker

1. Grab the image `docker pull meetmangukiya/corobo`
2. Run the image :D:
    ```
    docker run --rm -e COBOT_TOKEN="this-is-chatbot-token" \
                    -e COBOT_PREFIX="gitmate" \
                    -e BOT_ADMINS="sils meetmangukiya" \
                    -e BACKEND="Slack" \
                    -e GH_TOKEN="this-is-the-bots-github-token" \
                    -e GL_TOKEN="this-is-the-bots-gitlab-token" \
                    -e GH_ORG_NAME="gitmate" \
                    -e GL_ORG_NAME="gitmate" \
                    meetmangukiya/corobo
    ```

## Under Brewing

There are a few plugins that may be coala specific. But we are working on making
it more configurable and adaptable for other orgs.
