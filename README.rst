cliform
=======

This library presents a Django Form as a series of terminal questions,
to be filled in by a command line user.

The goal is to provide a simple, automatable command-line interface that still
shares the same validation rules as web-based forms.

.. image:: https://secure.travis-ci.org/rbarrois/cliform.png?branch=master
    :target: http://travis-ci.org/rbarrois/cliform/

.. image:: https://img.shields.io/pypi/v/cliform.svg
    :target: https://cliform.readthedocs.io/en/latest/changelog.html
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/cliform.svg
    :target: https://pypi.python.org/pypi/cliform/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/wheel/cliform.svg
    :target: https://pypi.python.org/pypi/cliform/
    :alt: Wheel status

.. image:: https://img.shields.io/pypi/l/cliform.svg
    :target: https://pypi.python.org/pypi/cliform/
    :alt: License

Links
-----

- Package on `PyPI`_: http://pypi.python.org/pypi/cliform/
- Doc on `ReadTheDocs <http://readthedocs.org/>`_: https://cliform.readthedocs.io/
- Source on `GitHub <http://github.com/>`_: http://github.com/rbarrois/cliform/
- Build on `Travis CI <http://travis-ci.org/>`_: http://travis-ci.org/rbarrois/cliform/



Getting started
===============

Install the package from `PyPI`_, using pip:

.. code-block:: sh

    pip install cliform

Or from GitHub:

.. code-block:: sh

    $ git clone git://github.com/rbarrois/cliform.git


Import it in your code:


.. code-block:: python

    import cliform.django

Interactive prompt
------------------

This package can be used to provide an interactive prompt for a given form:

.. code-block:: python

    # myapp/management/commands/adduser.py

    import cliform.django

    from ...forms import UserForm

    class Command(cliform.django.InteractivePromptCommand):
        help = "Add a user"

        form = UserForm




Fill a Django Form through a CLI prompt:

.. code-block:: python

    import cliform

    import django
    from django import forms
    from django.contrib.auth import models

    django.setup()

    class UserForm(forms.ModelForm):
        class Meta:
            model = models.User
            fields = [
                'first_name',
                'last_name',
                'email',
                'is_superuser',
            ]

    prompter = cliform.Prompter(
        form_class=UserForm,
        final_check=True,
        mode=cliform.PromptMode.UNTIL_VALID,
    )
    form = prompter.prompt()
    print("Yay! Created user: {}".format(form.save()))


And on the command line:

.. code-block:: sh

    $ ./manage.py adduser
    >>> First name?
    > John
    >>> Last name?
    > Doe
    >>> Email?
    > fake@nope
    !! Error: Please enter a valid email address
    >>> Email?
    > johndoe@example.com
    >>> Superuser? ([Y]es/[N]o)
    > yep
    !! Error: Enter a valid yes/no flag
    >>> Superuser? ([Y]es/[N]o)
    > Y

    === Summary ===
    First name:     John
    Last name:      Doe
    Email:          johndoe@example.com
    Superuser:      True
    >>> Confirm? ([Yes]/[No])
    > 
    > [Default: yes]

    `UserForm` has been submitted:
        Result: <User: John Doe>



Features
--------

- Handle multiple choices, with easy shortcuts (e.g boolean field)
- Validate fields as early as possible
- Hide password values
- Handle default values
- Use colour for prompt/options/default values
- Confirm before saving

Roadmap:

    - Interact with the ``messages`` framework
    - Allow field ordering customization
    - Pre-fill fields through command-line flags
    - Read from json/toml/... file
    - Accept a standardized input through ``stdin``


Contributing
============

In order to contribute to the source code:

- Open an issue on `GitHub`_: https://github.com/rbarrois/cliform/issues
- Fork the `repository <https://github.com/rbarrois/cliform>`_
  and submit a pull request on `GitHub`_
- Or send me a patch (mailto:raphael.barrois+cliform@polytechnique.org)

When submitting patches or pull requests, you should respect the following rules:

- Coding conventions are based on :pep:`8`
- The whole test suite must pass after adding the changes
- The test coverage for a new feature must be 100%
- New features and methods should be documented in the *Reference* section
  and included in the *ChangeLog*
- Include your name in the *Contributors* section

.. note:: All files should contain the following header::

          # -*- encoding: utf-8 -*-
          # Copyright (c) The cliform project


.. _PyPI: http://pypi.python.org/

