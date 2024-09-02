from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class RegisterForm(UserCreationForm):
    agree_terms = forms.BooleanField(
        required=True,
        label="I agree all statements in Terms of service",
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'last_name',
            'password1',
            'password2'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'agree_terms':
                field.widget.attrs.update({'class': 'form-check-input me-2'})
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'

















