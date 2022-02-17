from bot import message_to_vk
from bot import requests_to_vk
from os_handler import write_result
from datetime import datetime
from db_handler import Base_operator

if __name__ == '__main__':

    user_id = 681175888
    group_id = 207956541
    # Экземпляр апдейта базы
    db_update = Base_operator()

    if message_to_vk.write_msg(user_id, 'Привет') == 'OK':
        # Фиксируем время запроса (нужно для названия json и для индетификатора в базе данных
        time_reg = str(datetime.now().date()) + "." + str(datetime.now().time()).replace(":", "-")
        # Отправляем запрос
        age_from = message_to_vk.ask_info_for_request(user_id, 'С какого возраста будем искать')
        age_to = message_to_vk.ask_info_for_request(user_id, 'До какого возраста будем искать')
        sex = message_to_vk.ask_info_for_request(user_id, '1 - женщина , 2 - мужчина, 3 - любой (по умолчанию)')
        status = message_to_vk.ask_info_for_request(user_id, '1- не женат (не замужем), '
                                                             '2 - встречается, '
                                                             '3: помолвлен(-а), '
                                                             '4: женат (замужем), '
                                                             '5 - всё сложно, '
                                                             '6 - активном поиске, '
                                                             '7 - влюблен(-а), '
                                                             '8 - в гражданском браке')

        hometown = str(message_to_vk.ask_info_for_request(user_id, 'Выберите город').title())
        favorite_person=bool
        # Отправляем запрос
        users = requests_to_vk.request_to_vk(user_id, age_from, age_to, sex, status, hometown)

        # Запись нового клиента в базу
        db_update.add_client(user_id=user_id)

        # Запись самого запроса в базу user_id, time_reg, age_from, age_to, sex, status, hometown
        db_update.add_search_reguest(user_id=user_id,
                                     time_reg=time_reg,
                                     age_from=age_from,
                                     age_to=age_to,
                                     sex=sex,
                                     status=status,
                                     hometown=hometown)

        # Выполняем выборку всех найденных раенее персон в список для пользователя
        found_persons_earlier = db_update.find_showed_persons(user_id)

        # Определил заранее будущий json
        overall_result = []
        # Перебор найденных пользоветелей пока не наберем 10 заданных ниже условиям
        for user in users.get('items'):

            # Проверка на количество найденных пользователей по условию не больше 10 за раз
            if len(overall_result) == 10:
                break

            # Проверка на закрытый профиль
            if user.get('is_closed') is True:
                continue

            # Проверка на наличие в базе запросов эот этого пользователя
            if user.get('id') in found_persons_earlier:
                continue

            # Забираем список фото пользователя
            photo_request = requests_to_vk.get_photos_request_to_vk(user.get('id'))

            # Проверка на количество фотографий (не менее трех)
            if len(photo_request) < 3:
                continue
            # Для ответа пользователю
            found_user_first_name = user.get('first_name')
            found_user_last_name = user.get('last_name')
            # Топ три фото
            owner = user.get('id')
            photo_1 = photo_request[0].get('id')
            photo_2 = photo_request[1].get('id')
            photo_3 = photo_request[2].get('id')
            # Ответ "attachment": "photo-57846937_457307562"
            message_to_vk.write_answer(user_id, found_user_first_name + ' ' + found_user_last_name)
            message_to_vk.send_photo(user_id, 'photo' + str(owner) + '_' + str(photo_1))
            message_to_vk.send_photo(user_id, 'photo' + str(owner) + '_' + str(photo_2))
            message_to_vk.send_photo(user_id, 'photo' + str(owner) + '_' + str(photo_3))

            favorite_person = message_to_vk.send_keyboard(user_id, 'https://vk.com/id' + str(user.get('id')))


            # Дополняем лист
            overall_result.append(dict({'link': 'https://vk.com/id' + str(user.get('id')), 'top_photos': [photo_1, photo_2, photo_3]}))

            db_update.add_showed_persons(user_id=user_id,
                                         time_reg=time_reg,
                                         showed_person_id=user.get('id'),
                                         favorite_person=favorite_person)

        # Отправляем на сохранить как json
        write_result(str('Search request ' + time_reg), overall_result)


        # Собственно всё. Прогрэм терминейтед.
