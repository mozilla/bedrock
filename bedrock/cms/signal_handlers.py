# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
from typing import TYPE_CHECKING, Type

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string

from wagtail.signals import page_published, page_unpublished, post_page_move
from wagtail_localize_smartling.signals import individual_translation_imported

from bedrock.cms.utils import warm_page_path_cache

if TYPE_CHECKING:
    from wagtail_localize.models import Translation
    from wagtail_localize_smartling.models import Job


logger = logging.getLogger(__name__)


def notify_of_imported_translation(
    sender: Type["Job"],
    instance: "Job",
    translation: "Translation",
    **kwargs,
):
    """
    Signal handler for receiving news that a translation has landed from
    Smartling.

    For now, sends a notification email to all Admins
    """
    UserModel = get_user_model()

    admin_emails = UserModel.objects.filter(
        is_superuser=True,
        is_active=True,
    ).values_list("email", flat=True)
    admin_emails = [email for email in admin_emails if email]  # Safety check to ensure no empty email addresses are included

    if not admin_emails:
        logger.warning("Unable to send translation-imported email alerts: no admins in system")
        return

    email_subject = "New translations imported into Bedrock CMS"

    job_name = instance.name
    translation_source_name = str(instance.translation_source.get_source_instance())

    smartling_cms_dashboard_url = f"{settings.WAGTAILADMIN_BASE_URL}/cms-admin/smartling-jobs/inspect/{instance.pk}/"

    email_body = render_to_string(
        template_name="cms/email/notifications/individual_translation_imported__body.txt",
        context={
            "job_name": job_name,
            "translation_source_name": translation_source_name,
            "translation_target_language_code": translation.target_locale.language_code,
            "smartling_cms_dashboard_url": smartling_cms_dashboard_url,
        },
    )

    send_mail(
        subject=email_subject,
        message=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=admin_emails,
    )
    logger.info(f"Translation-imported notification sent to {len(admin_emails)} admins")


individual_translation_imported.connect(notify_of_imported_translation, weak=False)


def trigger_cache_warming(sender, **kwargs):
    # Run after the post-migrate signal is sent for the `cms` app
    warm_page_path_cache()


def rebuild_path_cache_after_page_move(sender, **kwargs):
    # Check if a page has moved up or down within the tree
    # (rather than just being reordered). If it has really moved
    # then we should update the cache
    if kwargs["url_path_before"] == kwargs["url_path_after"]:
        # No URLs are changing - nothing to do here!
        return

    # The page is moving, so we need to rebuild the entire pre-empting-lookup cache
    warm_page_path_cache()


post_page_move.connect(rebuild_path_cache_after_page_move)

page_published.connect(trigger_cache_warming)
page_unpublished.connect(trigger_cache_warming)
