# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.redirects.util import redirect

redirectpatterns = (
    # kept seprarate from urls.py
    redirect(r"^careers/internships/$", "careers.home", name="careers.internships", permanent=False, locale_prefix=False),
)
