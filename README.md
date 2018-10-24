# corobo

[![Codecov branch](https://img.shields.io/codecov/c/github/coala/corobo/master.svg)](https://codecov.io/gh/coala/corobo)
[![Semaphore branch](https://semaphoreci.com/api/v1/coala/corobo/branches/master/badge.svg)](https://semaphoreci.com/coala/corobo)
[![Gitter Room](https://img.shields.io/badge/gitter-join%20chat%20%E2%86%92-brightgreen.svg)](https://gitter.im/coala/corobo)

## About

`corobo` is a Python based chatbot that could be connected to many messaging
platforms including Slack, HipChat, Telegram, IRC, XMPP, Tox, Campfire, Gitter,
Skype. Check all the backends available
[here](http://errbot.io/en/latest/features.html#multiple-server-backends)

This repository is mainly a collection of plugins that are written for
[errbot](http://errbot.io). Errbot is a Python based chatbot framework.

As described on Errbot website:
> Errbot is a chatbot, a daemon that connects to your favorite chat service
  and brings your tools into the conversation.

It handles sending messages to correct rooms/person, receiving messages,
calling your command routines on matching commands, etc. These command routines
are added by writing plugins, which are collected and loaded by Errbot when it
is ran.

## Features

Read more about what `corobo` could do for you
[here](https://github.com/coala/corobo/blob/master/docs/corobo.rst).

## Environment Variables

1. `BOT_ROOT` - absolute path of the project root.
2. `BOT_PREFIX` - prefix to use for issuing bot commands.
3. `BOT_ADMINS` - Space separated list of admins of the errbot instance.
4. `ROOMS` - Space separated list of rooms to join on startup. e.g.
   `ROOMS="coala/coala coala/coala/corobo"`
5. `BACKEND` - Backend to use.
   Default is Text, or Gitter when `BOT_TOKEN` is set.
5. `BOT_TOKEN` - Token used to connect to the backends - Mandatory for
   backends except Text.
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
2. Set environment variables mentioned above if required
   `export COBOT_TOKEN=...`, or edit config.py
3. Run `errbot`

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
