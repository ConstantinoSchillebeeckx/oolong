from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea, NumberInput
from django.utils.safestring import mark_safe
from django.forms import BaseModelFormSet
from django.utils.timezone import localtime, now

from .models import Activity, Sleep, Eat, Drink, Question, Response
from .models import Medication, Sex, Bathroom, Relax, Exercise


class QuestionnaireForm(forms.Form):
    '''
    Generic questionnaire form; note that it's defined entirely
    by the kwargs we initiate the form with.

    https://jacobian.org/writing/dynamic-form-generation/
    '''

    def __init__(self, *args, **kwargs):
        q = kwargs.pop('q') # questions
        choices = kwargs.pop('choices')
        user = kwargs.pop('user')

        super(QuestionnaireForm, self).__init__(*args, **kwargs)
        widget = forms.Select(attrs={'class':'form-control'})
        hidden = forms.HiddenInput(attrs={'value':user})

        self.fields['user'] = forms.CharField(widget=hidden, label='user')

        for q_id, q_str in q:
            self.fields['qid_%s' % q_id] = forms.ChoiceField(
                                                choices=choices,
                                                label=q_str,
                                                widget=widget
                                           )

    def clean(self):
        # ensure user hasn't already filled out this form today

        form_data = super(QuestionnaireForm, self).clean()
        user_id = form_data.get('user',None)

        q_ids = [l[0] for l in self.get_answers()]

        # get the timestamp from the last submitted response
        a = (Response.objects
                     .filter(user_id=user_id)
                     .filter(question_id__in=q_ids)
                     .order_by('-date')
                     .first())

        if a:
            diff = localtime(now()) - a.date
            hr_diff = diff.total_seconds() / 3600.0
            min_diff = 12 # minumum 12 hrs between submits

            if hr_diff < min_diff:
                    raise forms.ValidationError('You cannot submit this questionnaire more than once per day.')

        return form_data


    def get_answers(self):
        # returns the tuple (question_id, score)
        for name, value in self.cleaned_data.items():
            if name.startswith('qid_'):
                qid = int(name.replace('qid_',''))
                yield (qid, value)


    def save(self, commit=True, *args, **kwargs):
        super(QuestionnaireForm, self).__init__(*args, **kwargs)
        user = self.cleaned_data.get('user',None)

        for (question_id, score) in self.get_answers():
            r = Response(
                    question_id = question_id,
                    score = score,
                    user_id = user
                )
            r.save()

    


class MetricForm(ModelForm):
    '''
    Generic form used for metrics.
    '''
    required_css_class = 'required'

    def clean(self):
        '''
        If `Value` is provided, so must `Units`

        If `End` is provided, it must be after 'Time stamp`
        '''
        cleaned_data = super().clean()
        value = cleaned_data.get('value', None)
        units = cleaned_data.get('units', None)
        time_stamp = cleaned_data.get('time_stamp', None)
        end = cleaned_data.get('end', None)


        if value and not units:
            msg=mark_safe(
                "If providing a <code>Value</code>, "
                "you must also provide <code>Units</code>."
            )
            self.add_error('units', forms.ValidationError(msg))

        if end and time_stamp and end < time_stamp:
            msg=mark_safe(
                "If providing an <code>End</code> timestamp, "
                "it must occurr after starting <code>Time stamp</code>."
            )
            self.add_error('end', forms.ValidationError(msg))



    class Meta:
        exclude = ['user']
        widgets = {
            'notes': Textarea(attrs={'rows': 3}),
            'item': Textarea(attrs={'rows': 2}),
            'medication': Textarea(attrs={'rows': 2}),
            'value': NumberInput(attrs={"pattern":"[0-9]*"}),
        }

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

