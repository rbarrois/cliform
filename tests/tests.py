from django.test import TestCase

from . import utils


class InteractionTestCase(TestCase):
    def assertSequence(self, prompter, expected):
        runner = utils.SequenceRunner(expected)
        stdout = io.StringIO()
        stdin = io.StringIO()
        pass


class SimpleFormTests(TestCase):
    pass
