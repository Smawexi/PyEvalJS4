__package__ = 'pyevaljs4'

import logging
import json
import os
import subprocess
import tempfile
import weakref
import threading
from typing import Any
from functools import partial

from .exceptions import JSException, RunTimeNotFoundException
from ._program import NODE_PROGRAM, ASYNC_EVAL, ASYNC_CALL, SYNC_CALL
from .utils import get_node_env
from .settings import ASYNC_CALL_FLAGS

_logger = logging.getLogger('pyevaljs4')


class RunTime:

    def __init__(self):
        self._node = None
        self._node_env = get_node_env()
        self._path = None
        self._initialize = False
        self._finalizer = None
        self._lock = threading.Lock()

    def _init(self):
        with self._lock:
            if not self._initialize:
                try:
                    self._node = subprocess.Popen(
                        [self._node_env, self._path],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        universal_newlines=True,
                        encoding='utf-8'
                    )
                except Exception as e:
                    os.remove(self._path)
                    raise RunTimeNotFoundException("RunTime(nodejs) not found error") from e

                self._finalizer = weakref.finalize(self, self._close)
                self._initialize = True

    @classmethod
    def _compile(cls, source: str, suffix: str):
        self = cls()
        fd, path = tempfile.mkstemp(suffix=suffix, dir='.')
        with open(fd, 'w', encoding='utf-8') as fp:
            fp.write(NODE_PROGRAM.format(source=json.dumps(source)))
        self._path = path
        self._init()
        return self

    def eval(self, code: str) -> Any:
        if not code:
            return

        if code[:5] == 'await':
            return self._async_eval(code)

        return self._eval(code)

    def _eval(self, code: str):
        return self._execute(statement=code)

    def _async_eval(self, code: str):
        statement = ASYNC_CALL_FLAGS + ASYNC_EVAL.format(code)
        return self._execute(statement)

    def call(self, func: str, *args, arg_list: list = None, async_js_func=False) -> Any:
        if arg_list is not None:
            _args = arg_list
        else:
            _args = [arg for arg in args]

        return self._call(func, _args, async_js_func)

    def _call(self, func: str, args: list, async_js_func=False):
        if async_js_func:
            statement = ASYNC_CALL.format(flags=ASYNC_CALL_FLAGS, func=func, args=args)
        else:
            statement = SYNC_CALL.format(func=func, args=args)

        return self._execute(statement=statement)

    def _execute(self, statement: str):
        with self._lock:
            self._node.stdin.write(statement)
            self._node.stdin.flush()
            result = self._get_result()

        if result["exception"]:
            raise JSException(result['exception'])

        return result['result']

    def _get_result(self):
        _result = {'result': None, 'exception': None}
        while True:
            out = self._node.stdout.readline()
            if out[:14] == "[[<<result>>]]":
                try:
                    result = json.loads(out[14:])
                    _result['result'] = result
                except json.JSONDecodeError:
                    if out[14:].strip() != "undefined":
                        _logger.error("Not supported this behaviour")
                    _result['result'] = None
            elif out[:17] == "[[<<exception>>]]":
                _result['exception'] = out[17:]
            else:
                continue

            return _result

    def _close(self):
        os.remove(self._path)
        self._node.stdin.close()
        self._node.stdout.close()
        self._node.wait()

    def close(self):
        self._finalizer()

    @property
    def is_closed(self):
        if self._finalizer is not None:
            return not self._finalizer.alive

        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __getattr__(self, name):
        return partial(self.call, name)
