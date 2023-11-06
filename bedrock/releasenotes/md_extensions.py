# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re

from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor

UNCLOSED_IMG_TAG_PATTERN = re.compile(
    r"(?P<unclosed_img_tag><img[^>]*?>)(?<!\/>)(?!<\/img>)",
    re.MULTILINE,
)


class CloseImgTagPostprocessor(Postprocessor):
    def run(self, text):
        return re.sub(UNCLOSED_IMG_TAG_PATTERN, r"\g<unclosed_img_tag></img>", text)


class CloseImgTagExtension(Extension):
    def extendMarkdown(self, md):
        md.postprocessors.register(CloseImgTagPostprocessor(md), "close_img", 20)
