from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect

from .agriwebb import AgriWebb


def agriwebb_authorize(request: HttpRequest) -> JsonResponse:
    agriwebb = AgriWebb()

    authorization_url, state = agriwebb.get_authorization_url()

    request.session['auth_state'] = state

    return redirect(authorization_url)


def agriwebb_oauth2_callback(request: HttpRequest) -> JsonResponse:
    authorization_response = request.get_full_path()
    agriwebb = AgriWebb()
    state = request.session['auth_state']
    token = agriwebb.authenticate(authorization_response, state)

    return JsonResponse({'token': token})
