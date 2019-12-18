# -*- coding: utf-8 -*-
# Copyright (c) The cliform project
# This code is distributed under the two-clause BSD License.

__version__ = '0.1.0'
__author__ = 'Raphaël Barrois <raphael.barrois+cliform@polytechnique.org>'

import typing

class Display(typing.Text):
    pass

class Query(typing.Text):
    pass

Prompt = typing.Union[Display, Query]
Input = typing.NewType('Input', typing.Text)


class Prompter:
    def interact(self) -> typing.Generator[Prompt, typing.Optional[Input], None]:
        raise NotImplementedError()


class Interacter:
    def __init__(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout

    def _display(self, prompt: Prompt):
        self.stdout.write(prompt + '\n')

    def run(self, prompter: Prompter):
        loop = prompter.interact()
        reply = None
        while True:
            value = loop.send(reply)
            self._display(value)
            if isinstance(value, Query):
                reply = Input(input())
