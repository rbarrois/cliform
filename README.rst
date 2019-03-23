cliform
=======

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

    $ python add_user.py
    > First name?
    John
    > Last name?
    Doe
    > Email?
    fake@nope
    !! Error: Please enter a valid email address
    > Email?
    johndoe@example.com
    > Superuser? ([Y]es/[N]o)
    yep
    !! Error: Enter a valid yes/no flag
    > Superuser? ([Y]es/[N]o)
    Y
    === Summary ===
    First name:     John
    Last name:      Doe
    Email:          johndoe@example.com
    Superuser:      True
    > Confirm? ([Yes]/[No])
    
    Yay! Created user: <User: John Doe>

