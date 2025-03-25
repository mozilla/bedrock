# Task queue

As part of the 2024 Wagtail CMS work, we have added a task queue to process longer-running jobs in the background.

The queue is supplied by `django-rq`, which sits on top of `rq` and uses Redis as the storage backend.

Once infra has been set up fully to support this, documentation will be expanded, but for local development you can start a worker to process jobs in the queue with:

``` bash
make run-local-task-queue
```

Note that you will need Redis running on its default port of 6379. Redis is started by default when using Dockerized Bedrock locally.
