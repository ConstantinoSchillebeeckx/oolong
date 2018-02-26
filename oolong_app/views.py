from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect

from .forms import *

@login_required 
def index(request):
    '''Renders the homepage.'''

    context = {
    }

    response = render(request, 'index.html', context)

    return response


@login_required 
@csrf_protect 
def metric(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        pass

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MetricForm()

    return render(request, 'metric.html', {'form': form})


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
