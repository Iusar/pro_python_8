from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os_handler as oh

# Можно сделать класс методами но я не вижу разницы. Поэтому просто функции подряд

# Вступительный диалог.
def write_msg(user_id, message):
    token = oh.get_info('group_token')
    vk_session = vk_api.VkApi(token=token)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()
    # Возвращаем имя клиента
    user_name = vk.users.get(user_ids=user_id)[0].get('first_name')
    # Уникальные варианты из списка ВК
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                if request.lower() == "привет":
                    write_msg(event.user_id, f"Привет, {user_name}! ). Ищешь новых знакомств?")
                elif request.lower() in ['да', 'ага', 'ищу']:
                    return 'OK'
                elif request.lower() == "пока":
                    write_msg(event.user_id, "Пока((")
                else:
                    write_msg(event.user_id, "Не поняла вашего ответа...")

# Функция для отдельных вопросов
def ask_info_for_request(user_id, message):
    token = oh.get_info('group_token')
    vk_session = vk_api.VkApi(token=token)
    longpoll = VkLongPoll(vk_session)

    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                return event.text

# Функция для оотправки
def write_answer(user_id, message):
    token = oh.get_info('group_token')
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    # Уникальные варианты из списка ВК
    vk_session.method('messages.send', {'user_id': user_id, 'message': message,   'random_id': randrange(10 ** 7)})

# Функция для оотправки ответа с фотками(не обязательно)
def send_photo(user_id, attachment):
    token = oh.get_info('group_token')
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    # Уникальные варианты из списка ВК
    vk_session.method('messages.send', {'user_id': user_id, 'attachment': attachment, 'random_id': randrange(10 ** 7)})