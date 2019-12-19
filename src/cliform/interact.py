# -*- coding: utf-8 -*-
# Copyright (c) The cliform project
# This code is distributed under the two-clause BSD License.


import collections
import typing as T

# General interaction
# ===================


class Display(T.Text):
    """Display some text; no reply expected."""
    pass


class Query:
    """Expect some input."""


class Input(T.Text):
    """Raw user-provided text."""


BaseOutput = T.Union[Display, Query]
BaseLoop = T.Generator[T.Union[Display, Query], T.Optional[Input], None]


# Semantic interactions
# =====================


class Info(T.NamedTuple):
    """Information to show to the user"""
    message: T.Text
    want_input: bool = False


class Error(T.NamedTuple):
    """An error message."""
    message: T.Text
    field: T.Optional[T.Text] = None
    want_input: bool = False


class Summary(T.NamedTuple):
    """A summary of the forms to be submitted."""
    fields: T.Mapping[T.Text, T.Any]
    want_input: bool = False


class TextInput(T.NamedTuple):
    title: T.Text
    want_input: bool = True


class Option(T.NamedTuple):
    prefix: T.Text
    letter: T.Text
    suffix: T.Text


class ChoiceInput:
    title: T.Text
    options: T.Mapping[T.Text, T.Text]
    split_options: T.Mapping[T.Text, Option]
    default_first: bool = False
    want_input: bool = True

    def __init__(self, title, options, default_first=False) -> None:
        self.title = title
        self.options = options
        self.default_first = default_first
        self.split_options = self.parse_options(self.options)

    def parse_options(self, options) -> T.Mapping[T.Text, Option]:
        split_options = collections.OrderedDict()
        for letter, text in options.items():
            letter = letter.lower()
            position = text.lower().index(letter)
            split_options[letter] = Option(
                prefix=text[:position],
                letter=text[position],
                suffix=text[position + 1:],
            )
        return split_options

    @classmethod
    def generate_options(cls, values: T.Iterable[T.Text]) -> T.Mapping[T.Text, T.Text]:
        options: T.Dict[T.Text, T.Text] = collections.OrderedDict()
        orphans = []
        for option in values:
            for char in option.lower():
                if not char.isalpha():
                    continue
                if char not in options:
                    options[char] = option
                    break
            else:
                orphans.append(option)
        for rank, orphan in enumerate(orphans):
            options[str(rank)] = orphan
        return options


class BoolInput(ChoiceInput):
    def __init__(self, title: T.Text, default: T.Optional[bool]):
        options = [
            ('y', 'Yes'),
            ('n', 'No'),
        ]
        default_first = default is not None
        if default is False:
            options.reverse()
        super().__init__(title, options=collections.OrderedDict(options), default_first=default_first)


Prompt = T.Union[TextInput, ChoiceInput, BoolInput]
Output = T.Union[Info, Error, Summary, Prompt]


PromptLoop = T.Generator[Output, Input, Input]
InteractLoop = T.Generator[Output, T.Optional[Input], None]


class Prompter:
    def interact(self) -> InteractLoop:
        raise NotImplementedError()

    def expand(self, output: Output) -> T.Iterable[T.Text]:
        if isinstance(output, Info):
            yield output.message
        elif isinstance(output, Error):
            if output.field:
                yield "!! {0}: {1}".format(output.field, output.message)
            else:
                yield "!! {0}".format(output.message)
        elif isinstance(output, Summary):
            yield "=== Summary ==="
            width = (max(len(name) for name in output.fields) // 4 + 1) * 4
            line_format = "{0:<%d}{1}" % width
            for field, value in output.fields.items():
                yield line_format.format(field + ':', value)

        # Inputs
        elif isinstance(output, TextInput):
            yield ">>> {0}?".format(output.title)
        else:
            assert isinstance(output, ChoiceInput)
            yield ">>> {0}? ({1})".format(
                output.title,
                '/'.join(
                    '%s[%s]%s' % (prefix, letter.upper(), suffix)
                    for prefix, letter, suffix in output.split_options.values()
                ),
            )

    def loop(self) -> BaseLoop:
        interact_loop = self.interact()
        reply = None
        while True:
            value = interact_loop.send(reply)
            for line in self.expand(value):
                reply = yield Display(line)
                assert reply is None

            if value.want_input:
                reply = yield Query()


class BaseInteracter:
    def display(self, message: T.Text) -> None:
        raise NotImplementedError()

    def get_input(self) -> T.Text:
        raise NotImplementedError()

    def run(self, prompter: Prompter) -> None:
        loop = prompter.loop()
        reply = None
        while True:
            value = loop.send(reply)
            if isinstance(value, Display):
                self.display(value)
            elif isinstance(value, Query):
                reply = Input(self.get_input())


class StdioInteracter(BaseInteracter):
    """Interact with stdin/stdout."""
    def __init__(self, stdin: T.TextIO, stdout: T.TextIO):
        self.stdin = stdin
        self.stdout = stdout

    def display(self, message):
        self.stdout.write(message + '\n')

    def get_input(self):
        return input()
