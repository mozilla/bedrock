from __future__ import absolute_import

import fluent.syntax.ast as FTL
from fluent.migrate import COPY, REPLACE
from fluent.migrate.helpers import TERM_REFERENCE, VARIABLE_REFERENCE, transforms_from

windows_64_bit = "firefox/windows-64-bit.lang"


def migrate(ctx):
    """Migrate bedrock/firefox/templates/firefox/browsers/windows-64-bit.html, part {index}."""

    ctx.add_transforms(
        "firefox/windows-64-bit.ftl",
        "firefox/windows-64-bit.ftl",
        [
            FTL.Message(
                id=FTL.Identifier("windows-64-bit-firefox-for-windows"),
                value=REPLACE(
                    windows_64_bit,
                    "Firefox for Windows 64-bit",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("windows-64-bit-users-on-64-bit-windows"),
                value=REPLACE(
                    windows_64_bit,
                    "Users on 64-bit Windows who download Firefox can get our 64-bit version by default. That means you get a more secure version of Firefox.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
windows-64-bit-64-bit = {COPY(windows_64_bit, "64-bit",)}
""",
            windows_64_bit=windows_64_bit,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("windows-64-bit-a-more-secure-firefox"),
                value=REPLACE(
                    windows_64_bit,
                    "A more secure Firefox.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("windows-64-bit-users-on-64-bit-windows-crashes"),
                value=REPLACE(
                    windows_64_bit,
                    'Users on 64-bit Windows who download Firefox can get our 64-bit version by default. That means you get a more secure version of Firefox, one that also <a href="%(crashes)s">crashes a whole lot less</a>. How much less? In our tests so far, 64-bit Firefox reduced crashes by 39%% on machines with 4GB of RAM or more.',
                    {
                        "%%": FTL.TextElement("%"),
                        "%(crashes)s": VARIABLE_REFERENCE("crashes"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
windows-64-bit-whats-the-difference = {COPY(windows_64_bit, "What’s the difference between 32-bit and 64-bit?",)}
""",
            windows_64_bit=windows_64_bit,
        )
        + [
            FTL.Message(
                id=FTL.Identifier("windows-64-bit-heres-the-key-thing"),
                value=REPLACE(
                    windows_64_bit,
                    "Here’s the key thing to know: 64-bit applications can access more memory and are less likely to crash than 32-bit applications. Also, with the jump from 32 to 64 bits, a security feature called <a href=%(ASLR)s>Address Space Layout Randomization (ASLR)</a> works better to protect you from attackers. Linux and macOS users, fret not, you already enjoy a Firefox that’s optimized for 64-bit.",
                    {
                        "%%": "%",
                        "%(ASLR)s": VARIABLE_REFERENCE("ASLR"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Linux": TERM_REFERENCE("brand-name-linux"),
                        "macOS": TERM_REFERENCE("brand-name-mac"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("windows-64-bit-how-do-you-get-64"),
                value=REPLACE(
                    windows_64_bit,
                    "How do you get 64-bit Firefox?",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("windows-64-bit-if-youre-running"),
                value=REPLACE(
                    windows_64_bit,
                    'If you’re running 64-bit Windows (<a href="%(version)s">here’s how to check</a>), your Firefox may already be 64-bit. <a href="%(check)s">Check your Firefox version</a> (in the “About Firefox” window) and look for “(32-bit)” or “(64-bit)” after the version number:',
                    {
                        "%%": "%",
                        "%(version)s": VARIABLE_REFERENCE("version"),
                        "%(check)s": VARIABLE_REFERENCE("check"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("windows-64-bit-if-you-see-32-bit-older"),
                value=REPLACE(
                    windows_64_bit,
                    "If you see “(32-bit)” and you are running Firefox 56.0 or older, updating to the latest Firefox version should automatically upgrade you to 64-bit.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("windows-64-bit-if-you-see-32-bit-newer"),
                value=REPLACE(
                    windows_64_bit,
                    "If you see “(32-bit)” and are running Firefox 56.0.1 or newer, then your computer may not meet the minimum memory requirement for 64-bit (3 GB RAM or more). You can still manually install 64-bit Firefox, if you choose.",
                    {
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                    },
                ),
            ),
            FTL.Message(
                id=FTL.Identifier("windows-64-bit-if-you-need-to-run"),
                value=REPLACE(
                    windows_64_bit,
                    'If you need to run 32-bit Firefox or manually install 64-bit Firefox, you can simply download and re-run the Windows (32-bit or 64-bit) Firefox installer from the <a href="%(all)s">Firefox platforms and languages download page.</a>',
                    {
                        "%%": "%",
                        "%(all)s": VARIABLE_REFERENCE("all"),
                        "Firefox": TERM_REFERENCE("brand-name-firefox"),
                        "Windows": TERM_REFERENCE("brand-name-windows"),
                    },
                ),
            ),
        ]
        + transforms_from(
            """
windows-64-bit-take-control-of-your = {COPY(windows_64_bit, "Take control of your browser.",)}
""",
            windows_64_bit=windows_64_bit,
        ),
    )
