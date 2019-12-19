# -*- coding: utf-8 -*-
# Copyright (c) The cliform project
# This code is distributed under the two-clause BSD License.

import typing as T
import unittest

import cliform
import cliform.interact


class Expect(T.NamedTuple):
    """An expected prompt, and the reply to send."""
    prompt: T.Text
    reply: T.Optional[T.Text]


class SequenceRunner:
    _expected: T.Iterable[Expect]

    def __init__(self, expected: T.Iterable[Expect]):
        # self._expected: the list of expected prompts, and the replies
        self._expected = expected

    def interact(self, prompter: cliform.Prompter) -> None:
        loop = prompter.interact()
        reply = None
        for expected, answer in self._expected:
            value = loop.send(reply)
            if expected != value:
                raise ValueError("Prompt %r doesn't match expected %r" % (value, expected))
            if isinstance(value, cliform.interact.Query):
                reply = answer
            else:
                reply = None
        assert reply is None
        loop.close()


class InteractionTestCase(unittest.TestCase):
    def assertSequence(self, prompter: cliform.Prompter, expected: T.Sequence[Expect]) -> None:
        runner = SequenceRunner(expected)
        runner.interact(prompter)
