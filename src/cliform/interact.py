# -*- coding: utf-8 -*-
# Copyright (c) The cliform project
# This code is distributed under the two-clause BSD License.


import collections
import typing as T
from dataclasses import dataclass

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


@dataclass
class Info:
    """Information to show to the user"""
    message: T.Text
    want_input: bool = False


@dataclass
class Error:
    """An error message."""
    message: T.Text
    field: T.Optional[T.Text] = None
    want_input: bool = False


@dataclass
class Summary:
    """A summary of the forms to be submitted."""
    fields: T.Mapping[T.Text, T.Any]
    want_input: bool = False


@dataclass
class Prompt:
    title: T.Text

    def convert(self, reply: T.Text) -> T.Any:
        raise NotImplementedError()


@dataclass
class TextInput(Prompt):
    title: T.Text
    want_input: bool = True

    def convert(self, reply: T.Text):
        return reply


@dataclass
class OptionKey:
    value: T.Any


OptionShortcut = T.NewType('OptionShortcut', T.Text)


@dataclass
class Option:
    key: OptionKey
    shortcut: OptionShortcut
    prefix: T.Text
    suffix: T.Text


@dataclass
class ChoiceInput(Prompt):
    choices: T.Mapping[OptionShortcut, Option]
    default_first: bool = False

    @classmethod
    def from_shortcuts(
            cls, title: T.Text,
            options: T.Iterable[T.Tuple[OptionKey, OptionShortcut, T.Text]], default_first=False):
        choices: T.Dict[OptionShortcut, Option] = collections.OrderedDict()
        for key, shortcut, text in options:
            try:
                position = text.lower().index(shortcut.lower())
            except ValueError:
                # Shortcut absent from string
                position = 0
            choices[shortcut] = Option(
                key=key,
                shortcut=shortcut,
                prefix=text[:position],
                suffix=text[position + 1:],
            )
        return cls(
            title=title,
            choices=choices,
            default_first=default_first,
        )

    @classmethod
    def from_texts(cls, title: T.Text, options: T.Iterable[T.Tuple[OptionKey, T.Text]], default_first=False):

        choices: T.List[T.Tuple[OptionKey, OptionShortcut, T.Text]] = []
        shortcuts: T.Set[T.Text] = set()
        orphans = []
        for key, option in options:
            for char in option.lower():
                if not char.isalpha():
                    continue
                if char not in shortcuts:
                    choices.append((key, OptionShortcut(char), option))
                    shortcuts.add(char)
                    break
            else:
                orphans.append(option)
        for rank, orphan in enumerate(orphans):
            choices.append((key, OptionShortcut(str(rank)), orphan))
        return cls.from_shortcuts(
            title=title,
            options=choices,
            default_first=default_first,
        )

    def convert(self, reply: T.Text) -> T.Text:
        shortcut = OptionShortcut(reply)
        if shortcut in self.choices:
            return self.choices[shortcut].key.value
        elif self.default_first and not reply:
            return list(self.choices.values())[0].key.value
        else:
            return reply


def BoolInput(title: T.Text, default: T.Optional[bool]) -> ChoiceInput:
    options = [
        (OptionKey(True), "Yes"),
        (OptionKey(False), "No"),
    ]
    if default is False:
        options.reverse()
    return ChoiceInput.from_texts(
        title=title,
        options=options,
        default_first=default is not None,
    )


Output = T.Union[Info, Error, Summary, Prompt]


PromptLoop = T.Generator[Output, Input, Input]
InteractLoop = T.Generator[Output, T.Optional[Input], None]


class Prompter:
    ERROR_PREFIX = '!!'
    INPUT_PREFIX = '>>>'
    SUMMARY_HEADER = '=== Summary ==='

    def interact(self) -> InteractLoop:
        raise NotImplementedError()

    def expand(self, output: Output) -> T.Iterable[T.Text]:
        if isinstance(output, Info):
            yield output.message
        elif isinstance(output, Error):
            if output.field:
                yield "{} {}: {}".format(self.ERROR_PREFIX, output.field, output.message)
            else:
                yield "{} {}".format(self.ERROR_PREFIX, output.message)
        elif isinstance(output, Summary):
            yield self.SUMMARY_HEADER
            width = (max(len(name) for name in output.fields) // 4 + 1) * 4
            line_format = "{0:<%d}{1}" % width
            for field, value in output.fields.items():
                yield line_format.format(field + ':', value)

        # Inputs
        elif isinstance(output, TextInput):
            yield "{} {}?".format(self.INPUT_PREFIX, output.title)
        else:
            assert isinstance(output, ChoiceInput)
            yield "{} {}? ({})".format(
                self.INPUT_PREFIX,
                output.title,
                '/'.join(
                    '%s[%s]%s' % (o.prefix, o.shortcut.upper(), o.suffix)
                    for o in output.choices.values()
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

            if isinstance(value, Prompt):
                reply = yield Query()
                assert reply is not None
                reply = value.convert(reply)


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
