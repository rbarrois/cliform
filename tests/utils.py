# -*- coding: utf-8 -*-
# Copyright (c) The cliform project
# This code is distributed under the two-clause BSD License.

import re
import typing as T
import unittest

import cliform
import cliform.interact


class ExpectMsg(T.NamedTuple):
    """An expected text display."""
    message: T.Text

    def check(self, value) -> None:
        if value != self.message:
            raise ValueError("Unexpected message %r; expecting %r" % (value, self.message))


class ExpectRe(T.NamedTuple):
    """Expect a message, matching with a regex."""
    regex: T.Text

    def check(self, value) -> None:
        if not re.match(self.regex, value):
            raise ValueError("Unexpected message %r; doesn't match %r" % (value, self.regex))


class ExpectQuery(T.NamedTuple):
    """Expect a request; and the reply to send."""
    reply: T.Text


Expect = T.Union[ExpectMsg, ExpectRe, ExpectQuery]


class SequenceRunner:
    _expected: T.Iterable[Expect]

    def __init__(self, expected: T.Iterable[Expect]):
        # self._expected: the list of expected prompts, and the replies
        self._expected = expected

    def interact(self, prompter: cliform.Prompter) -> None:
        loop = prompter.loop()
        reply = None
        for expected in self._expected:
            value = loop.send(reply)
            if isinstance(value, cliform.interact.Query):
                if not isinstance(expected, ExpectQuery):
                    raise ValueError("Unexpected query; expecting display %r" % expected)
                reply = expected.reply
            else:
                if isinstance(expected, ExpectQuery):
                    raise ValueError("Unexpected message %r; expecting query" % value)
                else:
                    expected.check(value)

                reply = None
        assert reply is None
        loop.close()


class InteractionTestCase(unittest.TestCase):
    def assertSequence(self, prompter: cliform.Prompter, expected: T.Sequence[Expect]) -> None:
        runner = SequenceRunner(expected)
        runner.interact(prompter)
