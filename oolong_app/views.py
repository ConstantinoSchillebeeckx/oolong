from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import modelformset_factory
from django.forms import modelform_factory
from django.apps import apps
from django.shortcuts import redirect

from django.utils import timezone
import django_tables2 as tables

import json

from .forms import UserLoginForm, MetricForm, QuestionnaireForm
from .models import Activity, Question, AvailableResponse, Questionnaire
from .tables import _Generic

@login_required 
def index(request):
    '''Renders the homepage.'''

    context = {
    }

    response = render(request, 'index.html', context)

    return response

@login_required 
@csrf_protect 
def submit_success(request):

    return render(request, 'submit_success.html', {})

@login_required 
@csrf_protect 
def questionnaire(request):

    qid = request.GET.get('qid', None)
    if not qid:
        qid = 'Happiness'


    # defines how user traverses questionnaires
    # key: starting form
    # value: redirect to form
    path = {
        'Happiness':'Anxiety',
        'Anxiety':'Depression',
        'Depression':'Summary'
    }
    
    next_qid = path.get(qid,None)

    try:
        questionnaire = Questionnaire.objects.get(name=qid)
    except:
        questionnaire = None

    # get our list of questions for this questionnaire
    # [(question_id, question_str),()]
    questions = list(Question.objects.filter(questionnaire_id=qid).values_list('id','question'))

    # get the available responses for the questions
    # [(response_score, response_label),()]
    responses = [(None,'----')]
    tmp = AvailableResponse.objects.filter(questionnaire_id=qid).values_list('score','label')
    responses.extend(list(tmp))
    responses_dict = {k:v for k,v in responses if k}

    form = QuestionnaireForm(
                request.POST or None, 
                q=questions, 
                choices=responses,
                user=request.user.id,
           )

    if form.is_valid():
        form.save()
    
        if next_qid:
            # redirect to next questionnaire
            return redirect('/questionnaire?qid=%s' %next_qid)
        else:
            # questionnaires finished
            return redirect('/submit_success/')

    return render(
                request, 
                'questionnaire.html', 
                {
                    'form':form,
                    'questionnaire': questionnaire,
                    'responses': json.dumps(responses_dict) # not currently used
                }
           )

@login_required 
@csrf_protect 
def edit_metric(request):

    metric_form, activity, table = None, None, None
    success, error = False, False
    activity_id=request.GET.get('activity', None)

    if activity_id:

        # lookup our model name based on the select
        activity = Activity.objects.get(id=activity_id)
        activity_name = activity.name

        # model associated with activity
        # NOTE: this assumes the activity name is the same as the model name
        model = apps.get_model('oolong_app', activity_name)

        extra_columns = []
        for l in model._meta.get_fields():
            l = str(l).split('.')[-1] # strip off the model name
            if not 'id' in l and not 'time_stamp' in l:
                extra_columns.append((l,tables.Column()))

        user_activities = model.objects.filter(user_id=request.user.id)

        table = _Generic(user_activities, extra_columns=extra_columns)

    context = {'metric_form': metric_form,
               'success': success,
               'error': error,
               'activities': Activity.objects.all(),
               'selected_activity': activity,
               'activities_table': table,
              }


    return render(
                request, 
                'metric.html', 
                context,
           )

@login_required 
@csrf_protect 
def submit_metric(request):
    '''
    This view works by having:
    1.  A list of buttons with hyperlinks populated by `Activity`
        It is a GET form which redirects with jQuery to ?activity=ID where
        ID is set based on the select. This ID is then used to load the proper
        form derived from the model associated with that ID.
    2.  metric_form
        The primary form that captures the recorded metric; this form is
        dynamically loaded based on which value for the select was chosen;
        based on that selection, the corresponding django model is chosen and
        used to populate the form.
    '''
    metric_form, activity = None, None
    success, error = False, False
    activity_id=request.GET.get('activity', None)

    if activity_id:

        # lookup our model name based on the select
        activity = Activity.objects.get(id=activity_id)
        activity_name = activity.name

        # model associated with activity
        # NOTE: this assumes the activity name is the same as the model name
        model = apps.get_model('oolong_app', activity_name)

        form = modelform_factory(model, form=MetricForm)

        if form:

            if request.method == 'GET':
                initial = {'start':timezone.localtime(timezone.now())}
                metric_form = form()
            else:
                metric_form = form(request.POST)
                print('view', dict(request.POST)['time_stamp'])
                print(timezone.now())
                print(timezone.localtime(timezone.now()))

                if metric_form.is_valid():

                    try:
                        a = metric_form.save(commit=False)
                        a.user_id = request.user.id
                        a.save()
                    except Exception as e:
                        print(e)
                        error = True
                    else:
                        success = True
                        metric_form = None

                        

    return render(
                request, 
                'metric.html', 
                {
                    'metric_form': metric_form,
                    'success': success,
                    'error': error,
                    'activities': Activity.objects.all(),
                    'selected_activity': activity,
                }
           )


@csrf_protect
def user_login(request):

    '''Renders the login page.'''

    # if arriving via url
    if request.method == 'GET':

        # redirect to homepage if user is already logged in
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')

        # otherwise, create login form as defined in forms.py
        form = UserLoginForm()

        # bundle it up into a context package with a csrftoken
        context = {
            'csrf': csrf,
            'form': form, # login form
        }

        # render the login template with the context package
        response = render(request, 'registration/login.html', context)

        return response

    # if arriving via submit button
    else:

        # create login form using user inputs
        form = UserLoginForm(request.POST)

        # if django can process the form input
        if form.is_valid():

            # store user inputs into variables
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # return a user object if the inputs check out
            user = authenticate(username=username, password=password)

            # if the user object is valid
            if user is not None:

                # log the user in and redirect to the homepage
                login(request, user)
                return HttpResponseRedirect('/')

            # if the user object is not valid
            else:

                # create error message and package is with a newly rendered form
                context = {
                    'csrf': csrf,
                    'error': 'Username or password is incorrect.',
                    'form': UserLoginForm(),
                }

                # reload page with error message
                return render(request, 'registration/login.html', context)


def user_signup(request):

    '''Renders the signup page.'''

    # if arriving via url
    if request.method == 'GET':

        # create signup form as defined in forms.py
        form = UserSignupForm()

        # bundle it up with a csrftoken to render page
        context = {
            'csrf': csrf,
            'form': form,
        }

        # return and render
        response = render(request, 'registration/signup.html', context)
        return response

    # if arriving via submit button
    else:

        # retrieve user inputs from frontend
        form = UserSignupForm(request.POST)

        if form.is_valid():

            # store user inputs into variables
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            secret_password = form.cleaned_data['secret_password']

            # determine if user input doesn't already exist in user table
            user_already_exists = user_in_database(username)

            # determine if user input fits validation requirements
            user_input_is_validated = input_is_valid(
                first_name,
                last_name,
                username,
                password1,
                password2,
                secret_password)


            # create new user if user input is valid
            if (not user_already_exists) and user_input_is_validated:

                # create and save new built-in Django User instance
                user = User.objects.create_user(
                    username,
                    email,
                    password1)

                # edit User to add custom fields and save
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                # validate user
                user = authenticate(username=username, password=password1)

                # if user credentials are valid
                if user is not None:

                    # log in user
                    login(request, user)

                    # reload homepage
                    return HttpResponseRedirect('/')

                else:

                    context = {
                        'csrf': csrf,
                        'error': 'User could not be validated. Please contact the administrator.',
                        'form': UserSignupForm(),
                    }

                    # reload signup page with error message
                    return render(request, 'registration/signup.html', context)


        # create error message if username already exists or input not validated
        if user_already_exists:
            error_message = 'A user with that username already exists.'
        elif not user_input_is_validated:
            error_message = 'Error with your passwords. Passwords must be at least 6 characters long, passwords must match, and you must know the correct secret password.'

        context = {
            'csrf': csrf,
            'error': error_message,
            'form': UserSignupForm(),
        }

        # reload signup page with error message
        return render(request, 'registration/signup.html', context)


@csrf_protect
def user_logout(request):
    '''A custom logout function.'''

    # log user out
    logout(request)

    # automatically redirect to login page
    return HttpResponseRedirect('/')  
