# -*- coding: utf-8 -*-
# Copyright (c) The cliform project
# This code is distributed under the two-clause BSD License.

import re
import typing
import unittest

import cliform



class Expect(typing.NamedTuple):
    """An expected prompt, and the reply to send."""
    prompt: cliform.Prompt
    reply: typing.Optional[cliform.Input]


class SequenceRunner:
    _expected: typing.List[Expect]

    def __init__(self, expected: typing.List[Expect]):
        # self._expected: the list of expected prompts, and the replies
        self._expected = expected

    def interact(self, prompter: cliform.Prompter):
        loop = prompter.interact()
        reply = None
        for expected, answer in self._expected:
            value = loop.send(reply)
            if not re.match(expected, value):
                raise ValueError("Prompt %r doesn't match expected %r" % (value, expected))
            if isinstance(value, cliform.Query):
                reply = answer
            else:
                reply = None
        assert reply is None
        loop.close()


class InteractionTestCase(unittest.TestCase):
    def assertSequence(self, prompter, expected):
        runner = SequenceRunner(expected)
        runner.interact(prompter)
