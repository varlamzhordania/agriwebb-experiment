from requests_oauthlib import OAuth2Session
from django.conf import settings

class AgriWebb:
    def __init__(
            self,
            client_id=settings.AGRIWEBB_CLIENT_ID,
            client_secret=settings.AGRIWEBB_CLIENT_SECRET,
            redirect_uri=settings.AGRIWEBB_REDIRECT_URI,
            token_url=settings.AGRIWEBB_TOKEN_URL,
            authorization_url=settings.AGRIWEBB_AUTHORIZATION_URL,
            api_url=settings.AGRIWEBB_API_URL,
    ):
        """
        Initializes the AgriWebb class.

        :param client_id: OAuth2 Client ID
        :param client_secret: OAuth2 Client Secret
        :param redirect_uri: The redirect URI for OAuth2
        :param token_url: OAuth2 token URL for obtaining access tokens
        :param authorization_url: The URL where users are redirected to authorize access
        :param api_url: URL of the AgriWebb GraphQL API
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_url = token_url
        self.authorization_url = authorization_url
        self.api_url = api_url
        self.token = None

    def get_authorization_url(self, organization=None):
        """
        Generates the authorization URL and redirects the user to the AgriWebb login page.
        """
        oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri)

        authorization_url, state = oauth.authorization_url(self.authorization_url)

        if organization:
            authorization_url = authorization_url + "&organization=" + organization

        return authorization_url, state

    def authenticate(self, authorization_response, state=None):
        """
        Handles the OAuth2 callback and exchanges the authorization code for an access token.

        :param state: state that was given during authorization url.
        :param authorization_response: The URL provided after user authorization containing the authorization code.
        """
        oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri, state=state)
        self.token = oauth.fetch_token(
            self.token_url,
            authorization_response=authorization_response,
            client_secret=self.client_secret
        )

        # Probably we want to store tokens right now
        return self.token
