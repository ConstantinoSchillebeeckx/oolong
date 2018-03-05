from django.conf.urls import include, url
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submit_metric/$', views.submit_metric, name='submit_metric'),
    url(r'^edit_metric/$', views.edit_metric, name='edit_metric'),
    url(r'^questionnaire/$', views.questionnaire, name='questionnaire'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^signup/$', views.user_signup, name='signup'),
    url(r'^log_out/$', views.user_logout, name='log_out'),
    url(r'^submit_success/$', views.submit_success, name='success'),
    url(
        r'^favicon.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('favicon.ico'),
            permanent=False),
        name="favicon"
    ),
]
