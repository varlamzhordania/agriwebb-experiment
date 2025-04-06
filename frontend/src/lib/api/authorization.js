import {CLIENT_ID, AGRIWEBB_AUTHORIZAtION_URL, BASE_URL, AGRIWEBB_SCOPES} from "../../config"

export const oAuth2Install = (organization = null) => {
    const url = new URL(AGRIWEBB_AUTHORIZAtION_URL)

    url.searchParams.set('response_type', 'code')
    url.searchParams.set('client_id', CLIENT_ID)
    url.searchParams.set('redirect_uri', BASE_URL)
    // url.searchParams.set('scope', SCOPE)
    // url.searchParams.set('state', state)

    return url.href

}