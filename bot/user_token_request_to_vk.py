import os_handler as oh
import vk_api


# Не используется в основной программе
def get_user_token(login, password):
    vk_session = vk_api.VkApi(login, password)
    vk_session.auth(token_only=True)
    return vk_session.token['access_token']


if __name__ == '__main__':

    user_login = oh.get_info('user_login')
    user_password = oh.get_info('user_password')
    token = get_user_token(user_login, user_password)
    oh.write_token('user_token', token)



