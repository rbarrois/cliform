# -*- coding: utf-8 -*-
# Copyright (c) The cliform project
# This code is distributed under the two-clause BSD License.

import typing as T

from django import forms

import cliform
import cliform.django

from . import utils


class ExampleForm(forms.Form):
    name = forms.CharField(label="Name")
    email = forms.EmailField(label="Email")

    def save(self) -> T.Dict:
        return self.cleaned_data


class FormPrompter(cliform.django.FormPrompter):
    form_class = ExampleForm


class SimpleFormTests(utils.InteractionTestCase):
    def test_nominal(self) -> None:
        self.assertSequence(
            FormPrompter(),
            [
                utils.Expect(">>> Name?", "John Doe"),
                utils.Expect(">>> Email?", "john.doe@example.com"),
                utils.Expect("", None),
                utils.Expect("=== Summary ===", None),
                utils.Expect("Name:   John Doe", None),
                utils.Expect("Email:  john.doe@example.com", None),
                utils.Expect(">>> Confirm? ([Y]es/[N]o)", ''),
                utils.Expect("", None),
                utils.Expect("`ExampleForm` has been submitted:", None),
                utils.Expect("  {'name': 'John Doe', 'email': 'john.doe@example.com'}", None)
            ],
        )

    def test_bad_input(self) -> None:
        self.assertSequence(
            FormPrompter(),
            [
                utils.Expect(">>> Name?", "John Doe"),
                utils.Expect(">>> Email?", "john"),
                utils.Expect("!! Enter a valid email address.", None),
                utils.Expect(">>> Email?", "john.doe@example.com"),
                utils.Expect("", None),
                utils.Expect("=== Summary ===", None),
                utils.Expect("Name:   John Doe", None),
                utils.Expect("Email:  john.doe@example.com", None),
                utils.Expect(">>> Confirm? ([Y]es/[N]o)", ''),
                utils.Expect("", None),
                utils.Expect("`ExampleForm` has been submitted:", None),
                utils.Expect("  {'name': 'John Doe', 'email': 'john.doe@example.com'}", None)
            ],
        )
