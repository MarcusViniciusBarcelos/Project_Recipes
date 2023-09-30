
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['password'], 'type your password')
        add_placeholder(self.fields['password2'], 'Repet your password')

    first_name = forms.CharField(
        error_messages={'required': 'write your first name'},
        label='First Name'
    )

    last_name = forms.CharField(
        error_messages={'required': 'write your last name'},
        label='Last Name'
    )

    username = forms.CharField(
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have less than 150 characters',
        },
        label='username',
        help_text=(
            'Username must have letters, numbers or one of those @.+-_. '
            'The length should be between 4 and 150 characters.'
        ),
        min_length=4, max_length=150,
    )

    email = forms.EmailField(
        error_messages={'required': 'This field must not be empty'},
        label='E-mail',
        help_text='the e-mail must be a valid e-mail address',
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty',
        },
        label='Password',
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators=[strong_password]
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Repeat your password',
        error_messages={
            'required': 'This field must not be empty',
        },
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User e-mail is already in use', code='invalid',
            )

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Password and Password2 must be equal', code='invalid')

            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [password_confirmation_error, ]
            })
