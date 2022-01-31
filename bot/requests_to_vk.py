import vk_api
import os_handler as oh
import requests


# основной поисковой запрос
def request_to_vk(user_id, age_from, age_to, sex, status, hometown):

    vk_session = vk_api.VkApi(token=oh.get_info('user_token'))
    vk = vk_session.get_api()

    # Запрос
    users = vk.users.search(user_id=user_id,
                            age_from=age_from,
                            age_to=age_to,
                            sex=sex,
                            status=status,
                            hometown=hometown,
                            count=1000)
    return users

 # Получаем словарь из вконтакте для метода main_function

def get_photos_request_to_vk(vk_user_id):

    vk_params = {"owner_id": vk_user_id, 'album_id': 'profile', 'count': 5, 'access_token': oh.get_info('user_token'), 'photo_sizes': '1', 'extended': 1, 'v': 5.131}
    photos_from_vk = requests.get('https://api.vk.com/method/photos.get', params=vk_params)
    if photos_from_vk.status_code == 200:
        json_from_vk = photos_from_vk.json()['response']['items']
        return json_from_vk
    else:
        print(f'error :( {photos_from_vk.status_code}')
        pass


