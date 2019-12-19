# -*- coding: utf-8 -*-
# Copyright (c) The cliform project
# This code is distributed under the two-clause BSD License.

import cliform
import cliform.interact

from . import utils


class MetaTests(utils.InteractionTestCase):
    """Test the test helpers"""
    class NaivePrompter(cliform.Prompter):
        def interact(self) -> cliform.interact.InteractLoop:
            yield cliform.interact.Info("Hello")
            yield cliform.interact.Info("World")
            reply = yield cliform.interact.TextInput("Enter your name")
            assert reply == "John Doe"
            yield cliform.interact.Info("Welcome, %s" % reply)

    def test_interacter(self) -> None:
        self.assertSequence(
            self.NaivePrompter(),
            [
                utils.ExpectMsg("Hello"),
                utils.ExpectMsg("World"),
                utils.ExpectMsg(">>> Enter your name?"),
                utils.ExpectQuery(reply="John Doe"),
                utils.ExpectMsg("Welcome, John Doe"),
            ],
        )

    def test_bad_output(self) -> None:
        with self.assertRaises(ValueError):
            self.assertSequence(
                self.NaivePrompter(),
                [
                    utils.ExpectMsg("Hello"),
                    utils.ExpectMsg("Earth"),
                    utils.ExpectMsg(">>> Enter your name?"),
                    utils.ExpectQuery(reply="John Doe"),
                    utils.ExpectMsg("Welcome, John Doe"),
                ],
            )

    def test_too_short(self) -> None:
        with self.assertRaises(AssertionError):
            self.assertSequence(
                self.NaivePrompter(),
                [
                    utils.ExpectMsg("Hello"),
                    utils.ExpectMsg("World"),
                    utils.ExpectMsg(">>> Enter your name?"),
                    utils.ExpectQuery(reply="John Doe"),
                ],
            )

    def test_too_long(self) -> None:
        with self.assertRaises((StopIteration, RuntimeError)):
            self.assertSequence(
                self.NaivePrompter(),
                [
                    utils.ExpectMsg("Hello"),
                    utils.ExpectMsg("World"),
                    utils.ExpectMsg(">>> Enter your name?"),
                    utils.ExpectQuery(reply="John Doe"),
                    utils.ExpectMsg("Welcome, John Doe"),
                    utils.ExpectMsg("Good bye!"),
                ],
            )

    def test_no_prompt(self) -> None:
        with self.assertRaises(ValueError):
            self.assertSequence(
                self.NaivePrompter(),
                [
                    utils.ExpectMsg("Hello"),
                    utils.ExpectMsg("World"),
                    utils.ExpectQuery(reply="John Doe"),
                    utils.ExpectMsg(">>> Enter your name?"),
                    utils.ExpectMsg("Welcome, John Doe"),
                ],
            )
