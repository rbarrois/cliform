# -*- coding: utf-8 -*-
# Copyright (c) The cliform project
# This code is distributed under the two-clause BSD License.

__version__ = '0.1.0'
__author__ = 'Raphaël Barrois <raphael.barrois+cliform@polytechnique.org>'

import typing as T


class Display(T.Text):
    pass


class Query(T.Text):
    pass


Prompt = T.Union[Display, Query]
Input = T.NewType('Input', T.Text)
InteractLoop = T.Generator[Prompt, T.Optional[Input], None]


class Prompter:
    def interact(self) -> InteractLoop:
        raise NotImplementedError()


class Interacter:
    def __init__(self, stdin: T.TextIO, stdout: T.TextIO):
        self.stdin = stdin
        self.stdout = stdout

    def _display(self, prompt: Prompt) -> None:
        self.stdout.write(prompt + '\n')

    def run(self, prompter: Prompter) -> None:
        loop = prompter.interact()
        reply = None
        while True:
            value = loop.send(reply)
            self._display(value)
            if isinstance(value, Query):
                reply = Input(input())
