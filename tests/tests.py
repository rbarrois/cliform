# -*- coding: utf-8 -*-
# Copyright (c) The cliform project
# This code is distributed under the two-clause BSD License.

from django.test import TestCase

import cliform

from . import utils


class SimpleFormTests(TestCase):
    pass


class MetaTests(utils.InteractionTestCase):
    """Test the test helpers"""
    class NaivePrompter(cliform.Prompter):
        def interact(self):
            yield cliform.Display("Hello")
            yield cliform.Display("World")
            reply = yield cliform.Query("Enter your name")
            assert reply == "John Doe"
            yield cliform.Display("Welcome, %s" % reply)

    def test_interacter(self):
        self.assertSequence(
            self.NaivePrompter(),
            [
                utils.Expect("Hello", None),
                utils.Expect("World", None),
                utils.Expect("Enter your name", "John Doe"),
                utils.Expect("Welcome, John Doe", None),
            ],
        )

    def test_bad_output(self):
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

    def test_too_short(self):
        with self.assertRaises(AssertionError):
            self.assertSequence(
                self.NaivePrompter(),
                [
                    utils.Expect("Hello", None),
                    utils.Expect("World", None),
                    utils.Expect("Enter your name", "John Doe"),
                ],
            )

    def test_too_long(self):
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

    def test_no_prompt(self):
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
