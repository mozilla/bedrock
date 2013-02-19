from tempfile import TemporaryFile
from textwrap import dedent


class TempFileMixin(object):
    """Provide a method for getting a temp file that is removed when closed."""
    def tempfile(self, data=None):
        tempf = TemporaryFile()
        if data:
            tempf.write(dedent(data))
            tempf.seek(0)
        return tempf
