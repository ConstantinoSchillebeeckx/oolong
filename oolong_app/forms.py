from django import forms
from django.contrib.auth.models import User


#  user login form model
class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=32)
    password = forms.CharField(label='Password', max_length=512, widget=forms.PasswordInput)


#  user signup form model
class UserSignupForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=32)
    last_name = forms.CharField(label='Last name', max_length=32)
    email = forms.CharField(label='Email', max_length=512)
    username = forms.CharField(label=' Username', max_length=32)
    password1 = forms.CharField(label='Password', max_length=512, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Retype password', max_length=512, widget=forms.PasswordInput)
    secret_password = forms.CharField(label='Secret password', max_length=512, widget=forms.PasswordInput)

''' signup form functions '''

# determine whether or not username exists in crib_user
def user_in_database(username):
    return User.objects.filter(username=username).exists()


# determine if a given input is 6 or more characters
def input_is_long_enough(input, length):
    return len(input) >= length


# determine if two passwords match
def given_passwords_match(password1, password2):
    return password1 == password2


# does user know the CRIB password
def correct_secret_password(password):
    return password == 'triplechocolatebrownie'


# determine if all input is valid according to functions defined above
def input_is_valid(first_name, last_name, username, password1, password2, secret_password):
    return input_is_long_enough(password2, 6) and given_passwords_match(password1, password2) and correct_secret_password(secret_password)

