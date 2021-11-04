# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from hashlib import sha256
from typing import Dict, Tuple, Union

from django.conf import settings
from django.core.management.base import BaseCommand
from django.test import RequestFactory
from django.utils.timezone import now as tz_now

import boto3
from sentry_sdk import capture_exception

from bedrock.contentful.api import ContentfulPage
from bedrock.contentful.constants import (
    COMPOSE_MAIN_PAGE_TYPE,
    MAX_MESSAGES_PER_QUEUE_POLL,
)
from bedrock.contentful.models import ContentfulEntry


def data_hash(data: Dict) -> str:
    str_data = json.dumps(data, sort_keys=True)
    return sha256(str_data.encode("utf8")).hexdigest()


class Command(BaseCommand):
    rf = RequestFactory()

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            dest="quiet",
            default=False,
            help="If no error occurs, swallow all output.",
        ),
        parser.add_argument(
            "-f",
            "--force",
            action="store_true",
            dest="force",
            default=False,
            help="Load the data even if nothing new from Contentful.",
        ),

    def log(self, msg) -> None:
        if not self.quiet:
            print(msg)

    def handle(self, *args, **options) -> None:
        self.quiet = options["quiet"]
        self.force = options["force"]
        if settings.CONTENTFUL_SPACE_ID and settings.CONTENTFUL_SPACE_KEY:
            if self.force:
                self.log("Running forced update from Contentful data")
            else:
                self.log("Checking for updated Contentful data")

            update_ran, added, updated = self.refresh()

            if update_ran:
                self.log(f"Done. Added: {added}. Updated: {updated}")
            else:
                self.log(f"Nothing to pull from Contentful")
        else:
            # This will always get shown, even if --quiet is passed
            print("Contentful credentials not configured")

    def refresh(self) -> Tuple[bool, int, int]:
        update_ran = False
        added = -1
        updated = -1

        poll_contentful = self.force or self._queue_has_viable_messages()

        if poll_contentful:
            added, updated = self._refresh_from_contentful()
            update_ran = True

        return update_ran, added, updated

    def _get_message_action(self, msg: str) -> Union[str, None]:
        # Format for these messages is:
        # ContentManagement.Entry.publish,<currently_irrelevant_string>,<currently_irrelevant_string>
        try:
            label, _, _ = msg.split(",")
            _, _, action = label.split(".")
            return action
        except (AttributeError, ValueError) as e:
            self.log(f"Problem getting message action from {msg}: {e}")
            capture_exception(e)
            return None

    def _purge_queue(self, queue) -> None:
        """Remove all entries in the queue, without inspecting them

        Split out for clarity - there are a few caveats about queue purging from
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.purge_queue

        > The message deletion process takes up to 60 seconds.
        > We recommend waiting for 60 seconds regardless of your queue's size.

        This is fine, as we run this every 5 mins.

        > Messages sent to the queue before you call PurgeQueue might be received
        > but are deleted within the next minute.

        This is _probably_ fine - if a "publish" message arrives 'late' and is deleted
        rather than acted on, that's fine, because we only purge after a "go" action,
        so we'll already be updating from Contentful.

        > Messages sent to the queue after you call PurgeQueue might be deleted
        > while the queue is being purged.

        This one is a bit riskier, so we should keep an eye on real-world behaviour.
        It might be useful to do a forced rebuild a couple of times a day, to be safe.
        """
        self.log("Purging the rest of the queue")
        queue.purge()

    def _queue_has_viable_messages(self) -> bool:
        """
        When pages/entries change, Contentful uses a webhook to push a
        message into a queue. Here, we get all enqueued messages and if ANY ONE
        of them has an action of a 'go' type, we count that as enough and
        we re-sync all of our Contentful content.

        If we get a 'go' signal, we explicitly drain the queue rather than waste
        network I/O on pointless checking. If we don't get a 'go' signal at all,
        we still effectively have purged the queue, just iteratively.

        What action types count as a 'go' signal?

        * auto_save -> YES
        * create -> YES
        * publish -> YES
        * save -> YES if on Dev (ie, preview mode)
        * unarchive -> YES

        * archive -> NO (because we need to remove the page in Bedrock first)
        * unpublish  -> NO (for similar reasons as above)
        * delete -> NO (ditto)
        """

        poll_queue = True
        may_purge_queue = False
        viable_message_found = False

        GO_ACTIONS = {"create", "publish", "unarchive"}
        EXTRA_DEV_GO_ACTIONS = {"save", "auto_save"}

        if settings.DEV:
            GO_ACTIONS = GO_ACTIONS.union(EXTRA_DEV_GO_ACTIONS)

        if not settings.CONTENTFUL_NOTIFICATION_QUEUE_ACCESS_KEY_ID:
            self.log(
                "AWS SQS Credentials not configured for Contentful webhook",
            )
            # We don't want things to block/fail if we don't have SQS config.
            # Instead, in this situation, it's better to just assume we got
            # a 'go' signal and poll Contentful anyway.
            return True

        sqs = boto3.resource(
            "sqs",
            region_name=settings.CONTENTFUL_NOTIFICATION_QUEUE_REGION,
            aws_access_key_id=settings.CONTENTFUL_NOTIFICATION_QUEUE_ACCESS_KEY_ID,
            aws_secret_access_key=settings.CONTENTFUL_NOTIFICATION_QUEUE_SECRET_ACCESS_KEY,
        )
        queue = sqs.Queue(settings.CONTENTFUL_NOTIFICATION_QUEUE_URL)

        while poll_queue:
            msg_batch = queue.receive_messages(
                WaitTimeSeconds=settings.CONTENTFUL_NOTIFICATION_QUEUE_WAIT_TIME,
                MaxNumberOfMessages=MAX_MESSAGES_PER_QUEUE_POLL,
            )

            if len(msg_batch) == 0:
                self.log("No messages in the queue")
                break

            for sqs_msg in msg_batch:
                msg_body = sqs_msg.body
                action = self._get_message_action(msg_body)
                if action in GO_ACTIONS:
                    # we've found a viable one, so that's great. Drain down the queue and move on
                    viable_message_found = True
                    self.log(f"Got a viable message: {msg_body}")
                    may_purge_queue = True
                    poll_queue = False  # no need to get more messages
                    break
                else:
                    # Explicitly delete the message and move on to the next one.
                    # Note that we don't purge the entire queue even if all of the
                    # current messages are inviable, because we don't want the risk
                    # of a viable message being lost during the purge process.
                    sqs_msg.delete()
                    continue

        if not viable_message_found:
            self.log(f"No viable message found in queue")

        if may_purge_queue:
            self._purge_queue(queue)

        return viable_message_found

    def _refresh_from_contentful(self) -> Tuple[int, int]:
        self.log("Pulling from Contentful")
        updated_count = 0
        added_count = 0
        content_ids = []

        # TODO: Stop syncing only selected content types and process the (paginated) lot
        for ctype in settings.CONTENTFUL_CONTENT_TYPES:
            for entry in ContentfulPage.client.entries(
                {
                    "content_type": ctype,
                    "include": 0,
                }
            ).items:
                content_ids.append((ctype, entry.sys["id"]))

        for ctype, page_id in content_ids:
            request = self.rf.get("/")
            request.locale = "en-US"
            try:
                page = ContentfulPage(request, page_id)
                page_data = page.get_content()
            except Exception:
                # problem with the page, load other pages
                capture_exception()
                continue

            # Compose-authored pages have a page_type of `page`
            # but really we want the entity the Compage page references
            if ctype == COMPOSE_MAIN_PAGE_TYPE:
                # TODO: make this standard when we _only_ have Compose pages,
                # because they all have a parent type of COMPOSE_MAIN_PAGE_TYPE
                ctype = page_data["page_type"]

            locale = page_data["info"]["locale"]
            hash = data_hash(page_data)
            slug = page_data["info"]["slug"]

            try:
                obj = ContentfulEntry.objects.get(contentful_id=page_id)
            except ContentfulEntry.DoesNotExist:
                self.log(f"Creating new ContentfulEntry for {ctype}:{page_id}")
                ContentfulEntry.objects.create(
                    contentful_id=page_id,
                    content_type=ctype,
                    locale=locale,
                    data_hash=hash,
                    data=page_data,
                    slug=slug,
                )
                added_count += 1
            else:
                if self.force or hash != obj.data_hash:
                    self.log(f"Updating existing ContentfulEntry for {ctype}:{page_id}")
                    obj.locale = locale
                    obj.data_hash = hash
                    obj.data = page_data
                    obj.last_modified = tz_now()
                    obj.slug = slug
                    obj.save()
                    updated_count += 1

        return added_count, updated_count
