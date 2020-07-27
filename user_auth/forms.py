from django import forms
from .models import User
from phonenumber_field.formfields import PhoneNumberField
my_default_errors = {
    'required': 'Это поле обязательно к заполнению',
    'invalid': 'Номер телефона должен быть введен в формате: +77777777777'
}
from django.contrib.auth.forms import AuthenticationForm



class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone']
        labels = {
            'phone': 'Номер телфона',
        }
        widgets = {'phone': forms.TextInput(attrs={
            'data-mask': '+7(700)-000-0000',
        })}


class UserAuthForm(forms.Form):
    phone = PhoneNumberField(label='Телефон', widget=forms.TextInput(attrs={'placeholder': 'Пример: +77777777777'}), error_messages=my_default_errors, required=True)
    password = forms.CharField(widget=forms.PasswordInput)

class UserResetPassoword(forms.Form):
    phone = PhoneNumberField(label='Телефон', widget=forms.TextInput(attrs={'placeholder': 'Пример: +77777777777'}),error_messages=my_default_errors, required=True)
