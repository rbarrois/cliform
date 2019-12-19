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
                utils.ExpectMsg(">>> Name?"),
                utils.ExpectQuery(reply="John Doe"),
                utils.ExpectMsg(">>> Email?"),
                utils.ExpectQuery(reply="john.doe@example.com"),
                utils.ExpectMsg(""),
                utils.ExpectMsg("=== Summary ==="),
                utils.ExpectMsg("Name:   John Doe"),
                utils.ExpectMsg("Email:  john.doe@example.com"),
                utils.ExpectMsg(">>> Confirm? ([Y]es/[N]o)"),
                utils.ExpectQuery(reply=''),
                utils.ExpectMsg(""),
                utils.ExpectMsg("`ExampleForm` has been submitted:"),
                utils.ExpectMsg("  {'name': 'John Doe', 'email': 'john.doe@example.com'}")
            ],
        )

    def test_bad_input(self) -> None:
        self.assertSequence(
            FormPrompter(),
            [
                utils.ExpectMsg(">>> Name?"),
                utils.ExpectQuery(reply="John Doe"),
                utils.ExpectMsg(">>> Email?"),
                utils.ExpectQuery(reply="john"),
                utils.ExpectMsg("!! Enter a valid email address."),
                utils.ExpectMsg(">>> Email?"),
                utils.ExpectQuery(reply="john.doe@example.com"),
                utils.ExpectMsg(""),
                utils.ExpectMsg("=== Summary ==="),
                utils.ExpectMsg("Name:   John Doe"),
                utils.ExpectMsg("Email:  john.doe@example.com"),
                utils.ExpectMsg(">>> Confirm? ([Y]es/[N]o)"),
                utils.ExpectQuery(reply=''),
                utils.ExpectMsg(""),
                utils.ExpectMsg("`ExampleForm` has been submitted:"),
                utils.ExpectMsg("  {'name': 'John Doe', 'email': 'john.doe@example.com'}")
            ],
        )
