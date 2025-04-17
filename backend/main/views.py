from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect

from .agriwebb import AgriWebb
from .models.auth import AgriWebbToken


def agriwebb_authorize(request: HttpRequest) -> JsonResponse:
    agriwebb = AgriWebb()

    organization = request.GET.get('organization', None)

    authorization_url, state = agriwebb.get_authorization_url(organization)

    request.session['auth_state'] = state
    if organization:
        request.session['organization'] = organization

    return redirect(authorization_url)


def agriwebb_oauth2_callback(request: HttpRequest) -> JsonResponse:
    authorization_response = request.get_full_path()
    agriwebb = AgriWebb()
    state = request.session['auth_state']
    token_data = agriwebb.authenticate(authorization_response, state)

    agriwebb_token = AgriWebbToken.objects.create(
        user=request.user,
        access_token=token_data['access_token'],
        refresh_token=token_data['refresh_token'],
        token_type=token_data['token_type'],
        expires_in_seconds=token_data['expires_in'],
    )

    organization = request.session.get('organization', None)

    if organization:
        agriwebb_token.set_organization(organization)

    return JsonResponse({'message': "Authentication successful."})
