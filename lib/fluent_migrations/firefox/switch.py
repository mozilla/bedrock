from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

switch = "firefox/switch.lang"

def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/switch.html, part {index}."""

    ctx.add_transforms(
        "firefox/switch.ftl",
        "firefox/switch.ftl",
        transforms_from("""
switch-switch-from-chrome = {COPY(switch, "Switch from Chrome to Firefox in just a few minutes",)}
switch-switching-to-firefox-is-fast = {COPY(switch, "Switching to Firefox is fast, easy and risk-free, because Firefox imports your bookmarks, autofills, passwords and preferences from Chrome.",)}
switch-switching-to-firefox-page-description = {COPY(switch, "Switching to Firefox is fast, easy and risk-free. Firefox imports your bookmarks, autofills, passwords and preferences from Chrome.",)}
switch-select-what-to-take = {COPY(switch, "Select what to take from Chrome.",)}
switch-let-firefox-do-the-rest = {COPY(switch, "Let Firefox do the rest.",)}
switch-enjoy-the-web-faster = {COPY(switch, "Enjoy the web faster, all set up for you.",)}
switch-download-and-switch = {COPY(switch, "Download and switch",)}
switch-use-firefox-and-still-chrome = {COPY(switch, "You can use Firefox and still have Chrome. Chrome won’t change on your machine one bit.",)}
switch-share-with-your-friends = {COPY(switch, "Share with your friends how to switch to Firefox",)}
switch-share-to-facebook = {COPY(switch, "Share to Facebook",)}
switch-firefox-makes-switching-fast-tweet = {COPY(switch, "🔥 Firefox makes switching from Chrome really fast. Try it out!",)}
switch-send-a-tweet = {COPY(switch, "Send a tweet",)}
switch-switch-to-firefox = {COPY(switch, "Switch to Firefox",)}
switch-hey = {COPY(switch, "Hey,",)}
switch-firefox-makes-switching-fast-email = {COPY(switch, "Firefox makes switching from Chrome really fast. I like it a lot, and you should try it.",)}
switch-check-it-out = {COPY(switch, "Check it out and let me know what you think:",)}
switch-send-an-email = {COPY(switch, "Send an email",)}
switch-still-not-convinced = {COPY(switch, "Still not convinced that switching to Firefox is easy?",)}
""", switch=switch)
        )
