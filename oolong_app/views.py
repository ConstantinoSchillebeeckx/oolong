from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf

#@login_required 
@csrf_protect 
def index(request):
    '''Renders the homepage.'''

    context = {
        'csrf' : csrf,
    }

    response = render(request, 'index.html', context)

    return response
