from random import randrange
from pprint import pprint
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os_handler as oh
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

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
                elif request.lower() in ['нет', 'не ищу', "пока"]:
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

def send_keyboard(user_id, url):
    token = oh.get_info('group_token')
    vk_session = vk_api.VkApi(token=token)
    bot_longpoll = VkLongPoll(vk_session)
    res = False

    keyboard = VkKeyboard(one_time=False, inline=True)
    # кнопка next
    keyboard.add_button(label='Дальше', color=VkKeyboardColor.NEGATIVE, payload={'type': 'button_type', 'command': 'break'})
    # кнопка с URL
    keyboard.add_openlink_button(label='Показать', link=url)
    keyboard.add_line()
    # кнопка favor
    keyboard.add_button(label='В избранное', color=VkKeyboardColor.PRIMARY, payload={'type': 'button_type', 'command': "add_to_favorite"})


    # Уникальные варианты из списка ВК
    vk_session.method('messages.send', {'user_id': user_id,
                                        'keyboard': keyboard.get_keyboard(),
                                        'message': 'Ну как?',
                                        'random_id': randrange(10 ** 7),
                                        'v': 5.131})

    for event in bot_longpoll.listen():

        if event.to_me == True and event.type == VkEventType.MESSAGE_NEW:
            if event.text == 'Дальше':
                return res
            elif event.text == 'В избранное':
                res = True


            # vk_session.method('messages.sendMessageEventAnswer', {
            #     'event_id': event.event_id,
            #     'user_id': event.user_id,
            #     'peer_id': event.peer_id,
            #     'event_data': json.dumps(event.payload),
            #     'v': 5.131})

