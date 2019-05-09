from builtins import object
import sys
from contextlib import contextmanager
from io import StringIO
from tempfile import TemporaryFile
from textwrap import dedent


class TempFileMixin(object):
    """Provide a method for getting a temp file that is removed when closed."""
    def tempfile(self, data=None):
        tempf = TemporaryFile(mode='w+', encoding='utf-8')
        if data:
            tempf.write(dedent(data))
            tempf.seek(0)
        return tempf


@contextmanager
def capture_stdio():
    oldout, olderr = sys.stdout, sys.stderr
    newio = [StringIO(), StringIO()]
    sys.stdout, sys.stderr = newio
    yield newio
    sys.stdout, sys.stderr = oldout, olderr
    newio[0] = newio[0].getvalue().rstrip()
    newio[1] = newio[1].getvalue().rstrip()
