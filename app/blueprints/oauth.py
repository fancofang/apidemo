import os
from flask import Blueprint, url_for, jsonify
from app.extensions import oauth, db
from app.libs.error_code import AuthFailed
from app.libs.token import generate_auth_token, combine_token_info
from app.models import User

oauth_bp = Blueprint('oauth', __name__)

github = oauth.register(
    name='github',
    client_id= os.getenv('GITHUB_CLIENT_ID'),
    client_secret= os.getenv('GITHUB_CLIENT_SECRET'),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v3/',
    client_kwargs={'scope': 'openid email profile'},
)

facebook = oauth.register(
    name='facebook',
    client_id=os.getenv('FACEBOOK_CLIENT_ID'),
    client_secret=os.getenv('FACEBOOK_CLIENT_SECRET'),
    access_token_url='https://graph.facebook.com/v2.12/oauth/access_token',
    access_token_params=None,
    authorize_url='https://www.facebook.com/v2.12/dialog/oauth',
    authorize_params=None,
    api_base_url='https://graph.facebook.com/v2.12',
    client_kwargs={'scope': 'email'}
)


twitter = oauth.register(
    name='twitter',
    client_id=os.getenv('TWITTER_CLIENT_ID'),
    client_secret=os.getenv('TWITTER_CLIENT_SECRET'),
    request_token_url='https://api.twitter.com/oauth/request_token',
    request_token_params=None,
    access_token_url='https://api.twitter.com/oauth/access_token',
    access_token_params=None,
    authorize_url='https://api.twitter.com/oauth/authenticate',
    authorize_params=None,
    api_base_url='https://api.twitter.com/1.1/',
    client_kwargs=None
)

providers = {
    'github': github,
    'twitter': twitter,
    'facebook':facebook,
    'google':google

}

profile_endpoints = {
    'github': 'user',
    'google': 'userinfo',
    'facebook': 'user',
    'twitter': 'account/verify_credentials.json?include_email=true'
}


def get_social_profile(provider, access_token):
    profile_endpoint = profile_endpoints[provider.name]
    resp = provider.get(profile_endpoint, token=access_token)
    profile = resp.json()

    if provider.name == 'twitter':
        email = profile.get('email')
    elif provider.name == 'google':
        email = profile.get('email')
    else:
        email = profile.get('email')
    return email


@oauth_bp.route('/login/<provider_name>')
def login(provider_name):
    # provider = oauth.create_client(provider_name)
    redirect_uri = url_for('.authorize', provider_name=provider_name, _external=True)
    return providers[provider_name].authorize_redirect( redirect_uri)

@oauth_bp.route('/authorize/<provider_name>')
def authorize(provider_name):
    provider = oauth.create_client(provider_name)
    token = provider.authorize_access_token()
    if token is None:
        raise AuthFailed()

    email = get_social_profile(provider,token)
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            email=email,
            register_from=provider_name
        )
        db.session.add(user)
        db.session.commit()
    identity = user.verify_oauth(email)
    expiration = 3600
    token,expires_in = generate_auth_token(identity['uid'],
                                provider_name.capitalize(),
                                identity['scope'],
                                expiration)
    t = combine_token_info(token=token, scope= identity['scope'], exp=expires_in)
    return jsonify(t), 201