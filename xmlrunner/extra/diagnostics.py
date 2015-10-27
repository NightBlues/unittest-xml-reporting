"""Integartion with diagnostics module."""

from diagnostics.storages import FileStorage
from diagnostics.models import ExceptionInfo

from xmlrunner.result import _TestInfo
from xmlrunner.runner import XMLTestRunner as _XMLTestRunner


class DiagnosticsTestInfo(_TestInfo):

    def __init__(self, test_result, test_method, outcome=SUCCESS, err=None, subTest=None):
        super(DiagnosticsTestInfo, self).__init__(test_result, test_method, outcome=outcome, err=err, subTest=subTest)
        self._details_path = self._exception_details_path(err)

    def _exception_details_path(self, err):
        """Return file name with details about exception err"""
        if isinstance(err, basestring) or err is None:
            return ""
        return FileStorage(".")._build_path_to_file(ExceptionInfo(err))

    def get_failure_attributes(self):
        res = super(DiagnosticsTestInfo, self).get_failure_attributes(*args, **kwargs)
        res["details"] = self._details_path
        return res


class XMLTestRunner(_XMLTestRunner):
    def __init__(self, output='.', outsuffix=None, stream=sys.stderr,
                 descriptions=True, verbosity=1, elapsed_times=True,
                 failfast=False, buffer=False, encoding=UTF8):
        super(XMLTestRunner).__init__(
            output='.', outsuffix=None, stream=sys.stderr,
            descriptions=True, verbosity=1, elapsed_times=True,
            failfast=False, buffer=False, encoding=UTF8, info_cls=DiagnosticsTestInfo)
