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

    def _input_for_field(self, label, field: forms.Field) -> interact.Prompt:
        if isinstance(field, forms.BooleanField):
            return interact.BoolInput(
                title=label,
                default=True if field.required else None,
            )
        elif isinstance(field, forms.ChoiceField):
            options = []
            for key, value in field.choices:
                if isinstance(value, str):
                    options.append((interact.OptionKey(key), value))
                else:
                    options.extend([
                        (interact.OptionKey(subkey), subvalue)
                        for subkey, subvalue in value
                    ])

            return interact.ChoiceInput.from_texts(
                title=label,
                options=options,
                default_first=field.required,
            )
        else:
            return interact.TextInput(label)

    def _make_label(self, field_name, label) -> T.Text:
        if label:
            return label
        return field_name.replace('_', ' ').capitalize()

    def _get_field(self, field_name: T.Text, field: forms.Field) -> interact.PromptLoop:
        label = self._make_label(field_name, field.label)
        while True:
            value = yield self._input_for_field(label, field)
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
            values[field_name] = yield from self._get_field(field_name, field)

        form = self.form_class(values)
        form.is_valid()

        summary = collections.OrderedDict()
        for name, field in form.fields.items():
            label = self._make_label(name, field.label)
            summary[label] = form.cleaned_data[name]

        yield interact.Info("")
        yield interact.Summary(summary)

        reply = yield interact.BoolInput(title="Confirm", default=True)

        if reply:
            result = form.cleaned_data
            self.on_submit(result)
            yield interact.Info('')
            yield interact.Info("`%s` has been submitted:" % self.form_class.__name__)
            yield interact.Info("  {!r}".format(result))

        else:
            yield interact.Error("Aborting")

