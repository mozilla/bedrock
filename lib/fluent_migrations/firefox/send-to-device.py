from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

send_to = "firefox/sendto.lang"

def migrate(ctx):
    """Migrate bedrock/base/templates/macros.html, part {index}."""

    ctx.add_transforms(
        "send_to_device.ftl",
        "send_to_device.ftl",
        [

            FTL.Message(
                id=FTL.Identifier("send-to-device-send-firefox"),
                value=REPLACE(
                    "firefox/sendto.lang",
                    "Send Firefox to your smartphone or tablet",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    }
                )
            ),
        ]
    )

    ctx.add_transforms(
        "send_to_device.ftl",
        "send_to_device.ftl",
        transforms_from("""
send-to-device-your-download-link = {COPY(send_to, "Your download link was sent.",)}
send-to-device-sorry-we-cant-send = {COPY(send_to, "Sorry, we can’t send SMS messages to this phone number.",)}
send-to-device-sorry-this-number = {COPY(send_to, "Sorry. This number isn’t valid. Please enter a U.S. phone number.",)}
send-to-device-please-enter-an-email = {COPY(send_to, "Please enter an email address.",)}
send-to-device-an-error-occured = {COPY(send_to, "An error occurred in our system. Please try again later.",)}
send-to-device-enter-your-email = {COPY(send_to, "Enter your email",)}
send-to-device-enter-your-email-or-phone = {COPY(send_to, "Enter your email or phone number",)}
send-to-device-enter-your-email-or-phone-10-digit = {COPY(send_to, "Enter your email or 10-digit phone number",)}
send-to-device-send = {COPY(send_to, "Send",)}
send-to-device-sms-service-available-in-select = {COPY(send_to, "SMS service available in select countries only. SMS &amp; data rates may apply.",)}
send-to-device-sms-service-available-to-us = {COPY(send_to, "SMS service available to U.S. phone numbers only. SMS &amp; data rates may apply.",)}
send-to-device-intended-recipient-email-sms = {COPY(send_to, "The intended recipient of the email or SMS must have consented.",)}
send-to-device-intended-recipient-email = {COPY(send_to, "The intended recipient of the email must have consented.",)}
send-to-device-check-your-device-email-sms = {COPY(send_to, "Check your device for the email or text message!",)}
send-to-device-check-your-device-email = {COPY(send_to, "Check your device for the email!",)}
send-to-device-send-to-another= {COPY(send_to, "Send to another device",)}
""", send_to=send_to)
        )
