from __future__ import absolute_import

from pipeline.conf import settings
from pipeline.compressors import SubProcessCompressor


class CleanCSSCompressor(SubProcessCompressor):
    def compress_css(self, css):
        command = (settings.CLEANCSS_BINARY, settings.CLEANCSS_ARGUMENTS)
        return self.execute_command(command, css)
