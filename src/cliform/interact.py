# -*- coding: utf-8 -*-
# Copyright (c) The cliform project
# This code is distributed under the two-clause BSD License.


import typing as T


class Display(T.Text):
    """Display some text; no reply expected."""
    pass


class Prompt(T.Text):
    """Display some text, expecting a reply."""
    pass


class Input(T.Text):
    """Raw user-provided text."""


Output = T.Union[Display, Prompt]


PromptLoop = T.Generator[Output, Input, Input]
InteractLoop = T.Generator[Output, T.Optional[Input], None]


class Prompter:
    def interact(self) -> InteractLoop:
        raise NotImplementedError()


class StdioInteracter:
    """Interact with stdin/stdout."""
    def __init__(self, stdin: T.TextIO, stdout: T.TextIO):
        self.stdin = stdin
        self.stdout = stdout

    def _display(self, prompt: Output) -> None:
        self.stdout.write(prompt + '\n')

    def run(self, prompter: Prompter) -> None:
        loop = prompter.interact()
        reply = None
        while True:
            value = loop.send(reply)
            self._display(value)
            if isinstance(value, Prompt):
                reply = Input(input())
