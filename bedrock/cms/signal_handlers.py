# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
from typing import TYPE_CHECKING, Type

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string

from wagtail_localize_smartling.signals import translation_imported

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
        template_name="cms/email/notifications/translation_imported__body.txt",
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


translation_imported.connect(notify_of_imported_translation, weak=False)
