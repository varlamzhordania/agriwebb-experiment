import requests

from django.conf import settings
from django.urls import reverse
from urllib.error import HTTPError
from requests_oauthlib import OAuth2Session

from .models.auth import AgriWebbToken


class AgriWebb:
    def __init__(
            self,
            client_id=None,
            client_secret=None,
            redirect_uri=None,
            token_url=None,
            authorization_url=None,
            api_url=None,
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
        self.client_id = client_id or getattr(settings, 'AGRIWEBB_CLIENT_ID', None)
        if not self.client_id:
            raise ValueError("AGRIWEBB_CLIENT_ID is required")

        self.client_secret = client_secret or getattr(settings, 'AGRIWEBB_CLIENT_SECRET', None)
        if not self.client_secret:
            raise ValueError("AGRIWEBB_CLIENT_SECRET is required")

        if redirect_uri:
            self.redirect_uri = redirect_uri
        else:
            reverse_name = getattr(settings, 'AGRIWEBB_REDIRECT_URI', None)
            if not reverse_name:
                raise ValueError("AGRIWEBB_REDIRECT_URI (reverse name) is required")
            try:
                redirect_path = reverse(reverse_name)
            except Exception as e:
                raise ValueError(f"Could not resolve redirect URI with name '{reverse_name}': {e}")

            base_url = getattr(settings, 'SERVER_DOMAIN', None) or getattr(
                settings,
                'ADMIN_URL',
                None
            )
            if not base_url:
                raise ValueError("SERVER_DOMAIN or ADMIN_URL must be defined in settings")

            self.redirect_uri = base_url + redirect_path

        self.token_url = token_url or getattr(settings, 'AGRIWEBB_TOKEN_URL', None)
        if not self.token_url:
            raise ValueError("AGRIWEBB_TOKEN_URL is required")

        self.authorization_url = authorization_url or getattr(
            settings,
            'AGRIWEBB_AUTHORIZATION_URL',
            None
        )
        if not self.authorization_url:
            raise ValueError("AGRIWEBB_AUTHORIZATION_URL is required")

        self.api_url = api_url or getattr(settings, 'AGRIWEBB_API_URL', None)
        if not self.api_url:
            raise ValueError("AGRIWEBB_API_URL is required")

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
        token = oauth.fetch_token(
            self.token_url,
            authorization_response=authorization_response,
            client_secret=self.client_secret
        )

        return token

    def refresh(self, token_id):
        """
        Refreshes the access token using the refresh token from the AgriWebbToken object.

        :param token_id: The ID of the AgriWebbToken record to refresh
        :return: The new token data after refreshing.
        """
        try:
            token = AgriWebbToken.objects.get(id=token_id)
        except AgriWebbToken.DoesNotExist:
            raise ValueError("Token not found")

        oauth = OAuth2Session(
            self.client_id, token={
                'access_token': token.access_token,
                'token_type': token.token_type,
                'refresh_token': token.refresh_token
            }
        )

        try:
            new_token = oauth.refresh_token(
                self.token_url,
                client_id=self.client_id,
                client_secret=self.client_secret
            )

            token.refresh(
                new_token['access_token'],
                new_token['refresh_token'],
                new_token['expires_in']
            )
            return new_token

        except HTTPError as e:
            raise Exception(f"Failed to refresh token: {e}")

    def get_graphql_data(self, token_id, query, variables=None):
        """
        Sends a GraphQL query to the AgriWebb API and returns the data.

        :param token_id: ID of the token stored in the database.
        :param query: The GraphQL query string.
        :param variables: The variables for the query, if any.
        :return: The JSON response containing the query result.
        """
        try:
            token = AgriWebbToken.objects.get(id=token_id)
        except AgriWebbToken.DoesNotExist:
            raise ValueError("Token not found")

        headers = {
            "Authorization": f"{token.token_type or 'Bearer'} {token.access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "query": query,
            "variables": variables or {}
        }

        response = requests.post(self.api_url, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"Failed to get data: {response.text}")

        data = response.json()

        if 'errors' in data:
            raise Exception(f"GraphQL Error: {data['errors']}")

        return data['data']

    def animals(
            self,
            token_id,
            farm_id,
            filter=None,
            sort=None,
            limit=None,
            skip=None,
            observation_date=None,
            capabilities=None
    ):
        """
        Retrieves the list of animals from the AgriWebb GraphQL API.

        :param token_id: ID of the token stored in the database.
        :param farm_id: The ID of the farm.
        :param filter: Filter criteria for the animals (optional).
        :param sort: Sorting criteria (optional).
        :param limit: Limit the number of results (optional).
        :param skip: Skip a number of results (optional).
        :param observation_date: Date of observation (optional).
        :param capabilities: List of capabilities (optional).
        :return: The list of animals.
        """
        query = """
         query animals(
           $farmId: String!
           $filter: AnimalFilter
           $sort: [AnimalSort!]
           $limit: Int
           $skip: Int
           $observationDate: Timestamp
           $_capabilities: [String]
         ) {
           animals(
             farmId: $farmId
             filter: $filter
             sort: $sort
             limit: $limit
             skip: $skip
             observationDate: $observationDate
             _capabilities: $_capabilities
           ) {
             ... # need to list the fields needed
           }
         }
         """

        variables = {
            "farmId": farm_id,
            "filter": filter,
            "sort": sort,
            "limit": limit,
            "skip": skip,
            "observationDate": observation_date,
            "_capabilities": capabilities
        }

        return self.get_graphql_data(token_id, query, variables)

    def farms(self, token_id, farm_ids=None):
        """
        Retrieves the list of farms from the AgriWebb GraphQL API.

        :param token_id: ID of the token stored in the database.
        :param farm_ids: A list of farm IDs to filter by (optional).
        :return: The list of farms.
        """
        query = """
        query farms(
          $farmIds: [String]
        ) {
          farms(
            farmIds: $farmIds
          ) {
            ... # need to list the fields needed
          }
        }
        """

        variables = {
            "farmIds": farm_ids
        }

        return self.get_graphql_data(token_id, query, variables)

    def animals_with_count(
            self,
            token_id,
            farm_id,
            filter=None,
            sort=None,
            limit=None,
            skip=None,
            observation_date=None,
            capabilities=None
    ):
        """
        Retrieves the list of animals with a count from the AgriWebb GraphQL API.

        :param token_id: ID of the token stored in the database.
        :param farm_id: The ID of the farm.
        :param filter: Filter criteria for the animals (optional).
        :param sort: Sorting criteria (optional).
        :param limit: Limit the number of results (optional).
        :param skip: Skip a number of results (optional).
        :param observation_date: Date of observation (optional).
        :param capabilities: List of capabilities (optional).
        :return: The list of animals with count.
        """
        query = """
        query animalsWithCount(
          $farmId: String!
          $filter: AnimalFilter
          $sort: [AnimalSort!]
          $limit: Int
          $skip: Int
          $observationDate: Timestamp
          $_capabilities: [String]
        ) {
          animalsWithCount(
            farmId: $farmId
            filter: $filter
            sort: $sort
            limit: $limit
            skip: $skip
            observationDate: $observationDate
            _capabilities: $_capabilities
          ) {
            animals {
              ... # need to list the fields needed
            }
            count
          }
        }
        """

        variables = {
            "farmId": farm_id,
            "filter": filter,
            "sort": sort,
            "limit": limit,
            "skip": skip,
            "observationDate": observation_date,
            "_capabilities": capabilities
        }

        return self.get_graphql_data(token_id, query, variables)
