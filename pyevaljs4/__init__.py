__package__ = 'pyevaljs4'

from .pyevaljs import RunTime, JSException, RunTimeNotFoundException
from .__version__ import version


def compile_(js_code: str = None, mode: str = None):
    """
    Compile js code
    :param js_code: js source code
    :param mode: Execution mode, the default is '.js', meaning it will execute with '.js' behavior.
                Other optional values include '.cjs' and '.mjs', etc.
    :return: RunTime
    """
    if js_code is None:
        js_code = ""

    if mode is None:
        mode = ".js"

    return RunTime._compile(js_code, mode)
