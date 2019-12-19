# -*- coding: utf-8 -*-
# Copyright (c) The cliform project
# This code is distributed under the two-clause BSD License.

from django import forms

import cliform
import cliform.django

from . import utils


class SimpleForm(forms.Form):
    name = forms.CharField(label="Name")
    email = forms.EmailField(label="Email")


class ComplexForm(forms.Form):
    name = forms.CharField(label="Name")
    email = forms.EmailField(label="Email")
    is_staff = forms.BooleanField(label="Is Staff")
    is_superuser = forms.BooleanField(required=False)
    profile = forms.ChoiceField(choices=[
        ('intern', "Intern"),
        ('fulltime', "Full-Time"),
        ('contractor', "Contractor"),
    ], required=False)


class SimpleFormTests(utils.InteractionTestCase):
    def setUp(self):
        class FormPrompter(cliform.django.FormPrompter):
            form_class = SimpleForm
            data = None

            def on_submit(self, data):
                self.data = data

        self.prompter = FormPrompter()

    def test_nominal(self) -> None:
        self.assertSequence(
            self.prompter,
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
                utils.ExpectMsg("`SimpleForm` has been submitted:"),
                utils.ExpectRe(r'  {.*}'),
            ],
        )
        self.assertEqual({
            'email': 'john.doe@example.com',
            'name': "John Doe",
        }, self.prompter.data)

    def test_bad_input(self) -> None:
        self.assertSequence(
            self.prompter,
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
                utils.ExpectMsg("`SimpleForm` has been submitted:"),
                utils.ExpectRe(r'  {.*}'),
            ],
        )
        self.assertEqual({
            'email': 'john.doe@example.com',
            'name': "John Doe",
        }, self.prompter.data)


class ComplexFormTests(utils.InteractionTestCase):
    def setUp(self):
        class FormPrompter(cliform.django.FormPrompter):
            form_class = ComplexForm
            data = None

            def on_submit(self, data):
                self.data = data

        self.prompter = FormPrompter()

    def test_nominal(self) -> None:
        self.assertSequence(
            self.prompter,
            [
                utils.ExpectMsg(">>> Name?"),
                utils.ExpectQuery(reply="John Doe"),
                utils.ExpectMsg(">>> Email?"),
                utils.ExpectQuery(reply="john.doe@example.com"),
                utils.ExpectMsg(">>> Is Staff? ([Y]es/[N]o)"),
                utils.ExpectQuery(reply=""),
                utils.ExpectMsg(">>> Is superuser? ([Y]es/[N]o)"),
                utils.ExpectQuery(reply=""),
                utils.ExpectMsg(">>> Profile? ([I]ntern/[F]ull-Time/[C]ontractor)"),
                utils.ExpectQuery(reply='f'),
                utils.ExpectMsg(""),
                utils.ExpectMsg("=== Summary ==="),
                utils.ExpectMsg("Name:           John Doe"),
                utils.ExpectMsg("Email:          john.doe@example.com"),
                utils.ExpectMsg("Is Staff:       True"),
                utils.ExpectMsg("Is superuser:   False"),
                utils.ExpectMsg("Profile:        fulltime"),
                utils.ExpectMsg(">>> Confirm? ([Y]es/[N]o)"),
                utils.ExpectQuery(reply=''),
                utils.ExpectMsg(""),
                utils.ExpectMsg("`ComplexForm` has been submitted:"),
                utils.ExpectRe(r'  {.*}'),
            ],
        )
        self.assertEqual({
            'email': 'john.doe@example.com',
            'name': "John Doe",
            'is_staff': True,
            'is_superuser': False,
            'profile': 'fulltime',
        }, self.prompter.data)
