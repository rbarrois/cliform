# -*- coding: utf-8 -*-
# Copyright (c) The cliform project
# This code is distributed under the two-clause BSD License.

import collections
import typing as T

from django import forms

from . import interact


def walk_errors(error: forms.ValidationError) -> T.Iterable[T.Text]:
    for message in error:
        if isinstance(message, tuple):
            field, messages = message
            for line in messages:
                yield "%s: %s" % (field, line)
        else:
            yield message


class FormPrompter(interact.Prompter):
    form_class: T.Type[forms.Form]

    def _get_field(self, field: forms.Field) -> interact.PromptLoop:
        label = field.label or ''
        while True:
            value = yield interact.TextInput(label)
            try:
                field.clean(value)
            except forms.ValidationError as e:
                for error in walk_errors(e):
                    yield interact.Error(message=error)
            else:
                return value

    def interact(self) -> interact.InteractLoop:
        base_form = self.form_class()
        values = {}
        for field_name, field in base_form.fields.items():
            values[field_name] = yield from self._get_field(field)

        form = self.form_class(values)
        form.is_valid()

        summary = collections.OrderedDict()
        for name, field in form.fields.items():
            summary[field.label] = values[name]

        yield interact.Info("")
        yield interact.Summary(summary)

        reply = yield interact.BoolInput(title="Confirm", default=True)

        if reply is not None and reply.lower() in ['', 'y']:
            result = form.save()

        yield interact.Info('')
        yield interact.Info("`%s` has been submitted:" % self.form_class.__name__)
        yield interact.Info("  {!r}".format(result))
