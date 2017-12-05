After creating your `Pull Request`, it is under the review process. This can be deduced from the `process/pending review` label. Now you have to wait for the reviewers to review your PR. You should *not* ask for reviews on our Gitter channel - we review those PRs continuously.

We're usually swamped with reviews, while you are waiting **please review other people's PRs** at [coala.io/review](https://coala.io/review): that helps you and will make your review happen faster as well. As a rule of thumb, *for every review you receive, give at least one review to someone else!*

For a good review, look at every commit on its own and place `ack <sha>` (commit is ready) or `unack <sha>` (commit needs work) comments on the pull request, be sure to remove other spacing like tabs. If you're done with a pull request, you can use `{bot_prefix} mark wip <pull URL>` to mark it *work in progress* finally.
