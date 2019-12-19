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
            yield cliform.interact.Display("Hello")
            yield cliform.interact.Display("World")
            reply = yield cliform.interact.Prompt("Enter your name")
            assert reply == "John Doe"
            yield cliform.interact.Display("Welcome, %s" % reply)

    def test_interacter(self) -> None:
        self.assertSequence(
            self.NaivePrompter(),
            [
                utils.Expect("Hello", None),
                utils.Expect("World", None),
                utils.Expect("Enter your name", "John Doe"),
                utils.Expect("Welcome, John Doe", None),
            ],
        )

    def test_bad_output(self) -> None:
        with self.assertRaises(ValueError):
            self.assertSequence(
                self.NaivePrompter(),
                [
                    utils.Expect("Hello", None),
                    utils.Expect("Earth", None),
                    utils.Expect("Enter your name", "John Doe"),
                    utils.Expect("Welcome, John Doe", None),
                ],
            )

    def test_too_short(self) -> None:
        with self.assertRaises(AssertionError):
            self.assertSequence(
                self.NaivePrompter(),
                [
                    utils.Expect("Hello", None),
                    utils.Expect("World", None),
                    utils.Expect("Enter your name", "John Doe"),
                ],
            )

    def test_too_long(self) -> None:
        with self.assertRaises(StopIteration):
            self.assertSequence(
                self.NaivePrompter(),
                [
                    utils.Expect("Hello", None),
                    utils.Expect("World", None),
                    utils.Expect("Enter your name", "John Doe"),
                    utils.Expect("Welcome, John Doe", None),
                    utils.Expect("Good bye!", None),
                ],
            )

    def test_no_prompt(self) -> None:
        with self.assertRaises(AssertionError):
            self.assertSequence(
                self.NaivePrompter(),
                [
                    utils.Expect("Hello", None),
                    utils.Expect("World", "John Doe"),
                    utils.Expect("Enter your name", None),
                    utils.Expect("Welcome, John Doe", None),
                ],
            )
