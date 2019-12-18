# -*- coding: utf-8 -*-
# Copyright (c) The cliform project
# This code is distributed under the two-clause BSD License.

import typing as T

from django import forms

from . import Prompter, InteractLoop, Prompt, Input, Query, Display


def walk_errors(error: forms.ValidationError) -> T.Iterable[T.Text]:
    for message in error:
        if isinstance(message, tuple):
            field, messages = message
            for line in messages:
                yield "%s: %s" % (field, line)
        else:
            yield message


class FormPrompter(Prompter):
    form_class: T.Type[forms.Form]

    def _get_field(self, field: forms.Field) -> T.Generator[Prompt, Input, Input]:
        while True:
            value = yield Query(">>> %s?" % field.label)
            try:
                field.clean(value)
            except forms.ValidationError as e:
                for error in walk_errors(e):
                    yield Display("!! " + error)
            else:
                return value

    def interact(self) -> InteractLoop:
        base_form = self.form_class()
        values = {}
        for field_name, field in base_form.fields.items():
            values[field_name] = yield from self._get_field(field)

        form = self.form_class(values)
        form.is_valid()
        yield Display("")
        yield Display("=== Summary ===")
        width = (max(len(name) for name in form.fields) // 4 + 1) * 4
        line_format = "{0:<%d}{1}" % width

        for field_name, field in form.fields.items():
            yield Display(line_format.format(field.label + ':', values[field_name]))

        reply = yield Query(">>> Confirm? ([Y]es/[N]o)")

        if reply is not None and reply.lower() in ['', 'y']:
            result = form.save()

        yield Display('')
        yield Display("`%s` has been submitted:" % self.form_class.__name__)
        yield Display("  {!r}".format(result))
