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
from django.contrib.auth.models import User

import django_tables2 as tables
from django_tables2 import RequestConfig
from datetime import timedelta
from django.utils.timezone import localdate, now, make_aware
from django.utils.dateparse import parse_datetime
from django.db.models.functions import TruncDate
from django.db.models import Case, When, FloatField, F

import pytz

import simplejson as json

from .forms import UserLoginForm, MetricForm, QuestionnaireForm, ResponseForm
from .forms import UserSignupForm, user_in_database, input_is_valid
from .models import Activity, Question, AvailableResponse, Questionnaire
from .models import Response, PlotResponse, Drink
from .tables import _Generic, ResponseTable

@login_required 
def index(request):
    '''Renders the homepage.'''

    context = {
    }

    response = render(request, 'index.html', context)

    return response

@login_required 
def plot(request):

    activity_id = request.GET.get('activity', None)
    dat, activity = None, None
    try:
        activity = Activity.objects.get(pk=activity_id)
    except Exception as ex:
        pass

    if not activity:
        # by default, show the mood plot

        # date at which I started using new scoring scheme
        date = make_aware(parse_datetime("2018-03-31 0:00:00"))
        dat = (PlotResponse.objects
                           .filter(user=request.user)
                           .filter(date__gt=date))
    elif str(activity) == 'Drink':
        '''
        I wanted to use a view here, which already converted the units
        and aggregated the volumes. This doesn't work however because
        the view doesn't properly group on date; it seems like it does
        the group on UTC versions of the date, not the local user date.
        '''
        dat = Drink.objects.filter(user=request.user).order_by('time_stamp')
        dat = dat.annotate(date=TruncDate('time_stamp'),
                fl_oz=Case(
                    When(units='ml', then=F('volume')*0.033814),
                    default=F('volume'),
                    output_field=FloatField()
                )
              )

    plotdat = None
    if dat and dat.count():
        plotdat = json.dumps(list(dat.values()), default=str)

    context = {
        'plotdat': plotdat,
        'activities': Activity.objects.all().order_by('id'),
        'activity': activity,
        'btn_class':'btn-success',
        'action':'plot',
    }

    response = render(request, 'plot.html', context)

    return response

@login_required 
@csrf_protect 
def submit_success(request):

    return render(request, 'submit_success.html', {})

@login_required 
@csrf_protect 
def edit_questionnaire(request):

    response_id = request.GET.get('id', None)
    q, form, questionnaire, table = None, None, None, None
    error, success = False, False
    today = True if 'today' in request.GET else False
    yesterday = True if 'yesterday' in request.GET else False

    if not response_id or 'sort' in request.GET:
        # if first arriving, show all submitted responses in a table
        table = get_responses_table(request, today, yesterday)
    else:
        # if editing a response
        a = Response.objects.get(id=response_id)
        q = Question.objects.get(id=a.question_id)
        questionnaire = Questionnaire.objects.get(name=q.questionnaire_id)

        # available responses for this questions
        responses = list(AvailableResponse.objects
                                          .filter(questionnaire_id=q.questionnaire_id)
                                          .order_by('score')
                                          .values_list('score','label'))

        form = ResponseForm(request.POST or None, instance=a, choices=responses)

        if form.is_valid():
            try:
                a = form.save(commit=False)
                a.id = response_id # set PK so we can do a save()
                a.save()
            except Exception as e:
                print(e)
                error = True
            else:
                success = "Questionnaire properly updated."
                form = None
                table = get_responses_table(request, None, None)

    if table:
        per_page = 33 # there are 33 questions total
        RequestConfig(request, paginate={'per_page': per_page}).configure(table)

    return render(
                request, 
                'questionnaire.html', 
                {
                    'form':form,
                    'questionnaire': questionnaire,
                    'question': q,
                    'table': table,
                    'success': success,
                    'error': error,
                }
           )


def get_responses_table(request, today, yesterday):


    responses = Response.objects.filter(user_id=request.user.id)


    if today or yesterday:
        start, end = filter_date(yesterday)
        responses = responses.filter(date__gt=start).filter(date__lt=end)


    table = ResponseTable(responses, order_by=("-date","question"))

    return table

def filter_date(yesterday):
    # return either today's date or yesterday's date
    # `yesterday` is a bool
    date = str(localdate(now()) - timedelta(yesterday))
    start = make_aware(parse_datetime(date + " 0:00:00"))
    end = make_aware(parse_datetime(date + " 23:59:59"))

    return start, end


@login_required 
@csrf_protect 
def submit_questionnaire(request):

    ''' find next questionnaire '''

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

    ''' build form '''

    # get our list of questions for this questionnaire
    # [(question_id, question_str),()]
    questions = list(Question.objects
                             .filter(questionnaire_id=qid)
                             .values_list('id','question'))

    # get the available responses for the questions
    # [(response_id, response_label),()]
    responses = list(AvailableResponse.objects
                                      .filter(questionnaire_id=qid)
                                      .order_by('score')
                                      .values_list('score','label'))
    responses_dict = {k:v for k,v in responses if k}

    form = QuestionnaireForm(
                request.POST or None, 
                q=questions, 
                choices=responses,
                user=request.user.id,
                default=questionnaire.default_response,
           )

    ''' validate form '''

    if form.is_valid():
        form.save()
    
        if next_qid:
            # redirect to next questionnaire
            return redirect('/submit_questionnaire?qid=%s' %next_qid)
        else:
            # questionnaires finished
            return redirect('/submit_success/')

    return render(
                request, 
                'questionnaire.html', 
                {
                    'form':form,
                    'questionnaire': questionnaire,
                    'responses': json.dumps(responses_dict) # not currently used see https://github.com/ConstantinoSchillebeeckx/oolong/issues/2
                }
           )


@login_required 
@csrf_protect 
def edit_metric(request):

    metric_form, activity, table = None, None, None
    date_filter=None,
    success, error = False, False
    activity_id=request.GET.get('activity', None)
    metric_id=request.GET.get('id', None)
    today = True if 'today' in request.GET else False
    yesterday = True if 'yesterday' in request.GET else False
    delete = True if 'delete' in request.GET else False

    if activity_id:

        ''' generate form '''

        # lookup our model name based on the activity
        activity = Activity.objects.get(id=activity_id)
        activity_name = activity.name

        # model associated with activity
        # NOTE: this assumes the activity name is the same as the model name
        model = apps.get_model('oolong_app', activity_name)
        form = modelform_factory(model, form=MetricForm)

        # if editing a metric instance
        # load the form with this id
        if metric_id:
            a = model.objects.get(id=metric_id)
            metric_form = form(instance=a)

        # if deleting this metric instance
        if metric_id and activity_id and delete:
            a.delete()
            success = 'Metric successfully deleted.'
            metric_id = None
            metric_form = None

        ''' validate and save form data '''

        # if submitting changed form data
        if request.method == 'POST':
            metric_form = form(request.POST, instance=a)

            if metric_form.is_valid():
                try:
                    a = metric_form.save(commit=False)
                    a.id = metric_id # set PK so we can do a save()
                    a.user_id = request.user.id
                    a.save()
                except Exception as e:
                    print(e)
                    error = True
                else:
                    success = 'Metric successfully updated.'
                    metric_form = None

        ''' get table of metrics '''

        # if no previous metric specified, or we've just saved an edit
        # show the table of all available saved metrics
        if not metric_id or request.method == 'POST':

            # lookup extra columns for given model
            # to make tables2 dynamic
            extra_columns = []
            for l in model._meta.get_fields():
                l = l.name # strip off model name
                if not 'id' in l and not 'time_stamp' in l:
                    col = (l,tables.Column())

                    # TODO find a better way to automatically
                    # check whether a field is DateTime type
                    if l == 'end':
                        col = (l,tables.DateTimeColumn(format='Y-m-d H:i:s'))
                    extra_columns.append(col)

            if today or yesterday:
                start, end = filter_date(yesterday)
                user_activities = (model.objects
                                        .filter(user_id=request.user.id)
                                        .filter(time_stamp__gt=start)
                                        .filter(time_stamp__lt=end)
                                        .values())
            else:
                user_activities = (model.objects
                                        .filter(user_id=request.user.id)
                                        .values())
            user_activities = list(user_activities)

            # manually add in activity_id so that
            # the TemplateColumn has access to it
            # used to render the edit button
            for l in user_activities:
                l['activity'] = activity_id

            table = _Generic(user_activities, extra_columns=extra_columns)
            RequestConfig(request, paginate={'per_page': 25}).configure(table)

    context = {'metric_form': metric_form,
               'success': success,
               'error': error,
               'activities': Activity.objects.all().order_by('id'),
               'selected_activity': activity,
               'metric_table': table,
               'action':'edit',
               'btn_class':'btn-warning',
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
                if activity_name == 'Medication':
                    # load previous meds for convenience
                    last_med = model.objects.latest('id')
                    last_med.time_stamp = None
                    metric_form = form(instance=last_med)
                else:
                    metric_form = form()
                    
            else:
                metric_form = form(request.POST)

                if metric_form.is_valid():

                    try:
                        a = metric_form.save(commit=False)
                        a.user_id = request.user.id
                        a.save()
                    except Exception as e:
                        print(e)
                        error = True
                    else:
                        success = 'Metric successfully submitted.'
                        metric_form = None

    return render(
                request, 
                'metric.html', 
                {'metric_form': metric_form,
                 'success': success,
                 'error': error,
                 'activities': Activity.objects.all().order_by('id'),
                 'selected_activity': activity,
                 'action':'submit',
                 'btn_class':'btn-info',
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
