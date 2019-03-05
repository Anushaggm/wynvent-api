# coding=utf-8

import requests

from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount
from allauth.socialaccount.providers.facebook.views import fb_complete_login
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from allauth.socialaccount.helpers import complete_social_login

from applications.accounts.social_providers import GoogleProvider
from applications.accounts.serializer import UserProfileSerializer

FB_GRAPH_API_USER_DATA_URL = 'https://graph.facebook.com/me?fields=id,name&access_token='


class UserSocialRegisterMixin(OAuth2Adapter):

    def facebook_signup(self, request, access_token):
        try:
            app = SocialApp.objects.get(provider="facebook")
            token = SocialToken(app=app, token=access_token)

            fb_login = fb_complete_login(request, app, token)
            fb_login.token = token
            fb_login.state = SocialLogin.state_from_request(request)

            ret = complete_social_login(request, fb_login)

            response_data = {}

            if request.user.is_authenticated():
                if request.user.username == "":
                    request.user.username = request.data['email']
                    request.user.email = request.data['email']
                    request.user.first_name = request.data['fname']
                    request.user.last_name = request.data['lname']
                    request.user.save()
                data = UserProfileSerializer(request.user).data
                return data
            else:
                return {
                'error': "User with this email already exists."
            }
        except Exception as e:
            return {
                'error': str(e)
            }

    def validate_facebook_userdata(self, request, accesstoken):

        request_data = request.data
        keys = request_data.keys()

        url = FB_GRAPH_API_USER_DATA_URL+accesstoken
        resp = requests.get(url=url)
        fb_user_data = resp.json()
        request_user_data = {'first_name':request_data.get('fname'),'last_name':request_data.get('lname'),'email':request_data.get('email')}

        valid = all(item in fb_user_data.items() for item in request_user_data.items())
        return valid

    def google_signup(self, request, access_token):
        try:
            self.provider_id = GoogleProvider.id
            self.access_token_url = 'https://accounts.google.com/o/oauth2/token'
            self.authorize_url = 'https://accounts.google.com/o/oauth2/auth'
            self.profile_url = 'https://www.googleapis.com/oauth2/v3/tokeninfo'

            app = SocialApp.objects.get(provider="google")
            token = SocialToken(app=app, token=access_token)

            resp = requests.get(self.profile_url,
                            params={'id_token': token.token,
                                    'alt': 'json'})
            resp.raise_for_status()
            extra_data = resp.json()
            login = self.get_provider() \
                .sociallogin_from_response(request,
                                           extra_data)
            login.token = token
            login.state = SocialLogin.state_from_request(request)

            ret = complete_social_login(request, login)

            if request.user.is_authenticated():
                if request.user.username == "":
                    request.user.username = request.data['email']
                    request.user.email = request.data['email']
                    request.user.first_name = request.data['fname']
                    request.user.last_name = request.data['lname']
                    request.user.save()
                data = UserProfileSerializer(request.user).data
                return data
            else:
                return {
                    'error': "Cannot complete signup."
            }
        except Exception as e:
            print(e, "Google ID####")
            return {
                'error': str(e)
            }

    def validate_social_account(self, access_token, provider):
        can_signup = False
        if provider == 'facebook':
            url = FB_GRAPH_API_USER_DATA_URL+access_token
            resp = requests.get(url=url)
            fb_user_data = resp.json()
            if 'id' in fb_user_data.keys():
                can_signup = True
                uid = fb_user_data['id']
                accounts = SocialAccount.objects.filter(uid=uid, provider='facebook')
                return (True,can_signup) if accounts.count() > 0 else (False,can_signup)
        elif provider == 'google':
            profile_url = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
            resp = requests.get(profile_url,
                            params={'id_token': access_token,
                                    'alt': 'json'})

            google_plus_data = resp.json()
            if 'sub' in google_plus_data.keys():
                can_signup = True
                uid = google_plus_data['sub']
                accounts = SocialAccount.objects.filter(uid=uid, provider='google')
                return (True,can_signup) if accounts.count() > 0 else (False, can_signup)
        return (False,can_signup)