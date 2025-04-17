from django.urls import path

from . import views

app_name = 'main'


urlpatterns = [
    path('oauth2/authorize/', views.agriwebb_authorize, name='agriwebb_authorize'),
    path('oauth2/callback/', views.agriwebb_oauth2_callback, name='agriwebb_oauth2_callback'),
]
