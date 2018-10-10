from social.backends.oauth import BaseOAuth2
# from comum.models.base import UserProfile


class IfrnIdOAuth2(BaseOAuth2):
    name = 'ifrnid'
    AUTHORIZATION_URL = 'http://sso/id/acesso/oauth/authorize/'
    ACCESS_TOKEN_METHOD = 'POST'
    ACCESS_TOKEN_URL = 'http://sso:8000/id/acesso/oauth/token/'
    ID_KEY = 'cpf'
    RESPONSE_TYPE = 'code'
    REDIRECT_STATE = True
    STATE_PARAMETER = True
    USER_DATA_URL = 'http://sso:8000/id/acesso/api/v1/me/'
    
    def user_data(self, access_token, *args, **kwargs):
        print("ACCESS_TOKEN=%s" % access_token)
        print(args)
        print(kwargs)
        print(kwargs['response']['token_type'])
        data = {'token_type': kwargs['response']['token_type'], 'access_token': access_token}
        print("ACCESS_TOKEN=END")
        response = self.request(
            url=self.USER_DATA_URL,
            data={'scope': kwargs['response']['scope']},
            method='POST',
            headers={
                'Authorization': '{token_type} {access_token}'.format(**data)
            }
        )
        print("USER_DATA: token={access_token}, response={response}, ".format({'access_token': access_token, 'response': response}))
        return response.json()

    def get_user_details(self, response):
        """
        Retorna um dicionário mapeando os fields do settings.AUTH_USER_MODEL.
        você pode fazer aqui outras coisas, como salvar os dados do usuário
        (`response`) em algum outro model.
        """
        print("RESPONSE=%s" % response)
        splitted_name = response['name'].split()
        first_name, last_name = splitted_name[0], ''
        if len(splitted_name) > 1:
            last_name = splitted_name[-1]
        return response
        # return {
        #     'username': response['cpf'],
        #     'first_name': first_name.strip(),
        #     'last_name': last_name.strip(),
        #     'email': response['email'],
        # }

    def extra_data(self, user, uid, response, details=None, *args, **kwargs):
        print("extra_data(user=%s, uid=%s, response=%s, details=%s, args=%s, kwargs=%s)" % (user, uid, response, details, args, kwargs))
        # if not UserProfile.objects.filter(user__pk=user.pk).exists():
        #     # Criando o profile básico do Usuário.
        #     user_profile = UserProfile()
        #     user_profile.nome = response['name']
        #     user_profile.cpf = response['cpf']
        #     user_profile.email = response['email']
        #     user_profile.user = user
        #     user_profile.is_recem_criado = True
        #     user_profile.save()
        return super(IfrnIdOAuth2, self).extra_data(user, uid, response, details, *args, **kwargs)
