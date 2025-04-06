import {
    CLIENT_ID,
    CLIENT_SECRET,
    AGRIWEBB_AUTHORIZAtION_URL,
    AGRIWEBB_TOKEN_URL,
    BASE_URL,
    AGRIWEBB_SCOPES
} from "../../config"

export const oAuth2Install = (organization = null) => {
    const url = new URL(AGRIWEBB_AUTHORIZAtION_URL)

    url.searchParams.set('response_type', 'code')
    url.searchParams.set('client_id', CLIENT_ID)
    url.searchParams.set('redirect_uri', BASE_URL + "/authorization/callback")
    if (orientation)
        url.searchParams.set('organization', organization)
    // url.searchParams.set('scope', SCOPE)
    // url.searchParams.set('state', state)

    return url.href
}

const generateAuthorizationHeader = () => {
    const credentials = `${CLIENT_ID}:${CLIENT_SECRET}`;
    const base64Credentials = btoa(credentials);
    return `Basic ${base64Credentials}`;
};

export const exchangeAuthorizationCode = async (authorizationCode, redirectUri) => {
    const data = new URLSearchParams({
        grant_type: 'authorization_code',
        code: authorizationCode,
        redirect_uri: redirectUri,
        client_id: CLIENT_ID,
        client_secret: CLIENT_SECRET, // Optional: Only if not using Basic Auth in the header
    });

    try {
        const response = await fetch(AGRIWEBB_TOKEN_URL, {
            method: 'POST',
            headers: {
                'Authorization': generateAuthorizationHeader(),
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: data.toString(),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Failed to exchange code: ${errorData.error_description || response.statusText}`);
        }

        const tokenData = await response.json();

        const {access_token, token_type, expires_in, refresh_token} = tokenData;

        console.log('Access Token:', access_token);
        console.log('Token Type:', token_type);
        console.log('Expires In:', expires_in);
        console.log('Refresh Token:', refresh_token);

        return {access_token, token_type, expires_in, refresh_token};
    } catch (error) {
        console.error('Error exchanging authorization code for access token:', error.message);
        throw error;
    }
};