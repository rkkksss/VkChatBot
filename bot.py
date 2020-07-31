import vk_api
import json
import random
import places
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

token = "d978fd60f2c4cddad148ad0bac1f664e42c8eff2e7469c5bd249cabacfad63a70451148683ec9ac82f626"
# token = "144b69655e74010ec63f440d6aad0caec0b5385007e8e986b11487d4dffdb7690278f2c93ba9c23aef3f8"

PLACES_MESSAGE = "Здесь ты можешь посмотреть список достопримечательностей города Жуковский и узнать больше о них, для этого напиши номер интересующего тебя объекта"
WAYS_MESSAGE = "Пока что мы составили только 2 туристических маршрута, в будущем их будет больше :) \n"
WAYS_MESSAGE_2 = "Напиши 1, чтобы увидеть пешеходный маршрут или 2, чтобы увидеть маршрут с использованием личного автомобиля"
HELP_TO_CITY_MESSAGE = "" # TODO
INTERACTIVE_MAP_MESSAGE = "Мы создали интерактивную карту! Посмотреть и потыкать можно по ссылке - http://datamaplab.ru/heritage/map.html."

vk = vk_api.VkApi(token=token)

longpoll = VkBotLongPoll(vk, 187761032)

main_keyboard = VkKeyboard(one_time=True)
main_keyboard.add_button('Достопримечательности города Жуковский', color=VkKeyboardColor.PRIMARY, payload='{"button": 1}')
main_keyboard.add_line()
main_keyboard.add_button('Туристические маршруты в г. Жуковском', color=VkKeyboardColor.PRIMARY, payload='{"button": 2}')
main_keyboard.add_line()
main_keyboard.add_button('Помощь городу Жуковский', color=VkKeyboardColor.PRIMARY, payload='{"button": 3}')
main_keyboard.add_line()
main_keyboard.add_button('Показать интерактивную карту', color=VkKeyboardColor.PRIMARY, payload='{"button": 4}')

ways_keyboard = VkKeyboard(one_time=True)
ways_keyboard.add_button("Пешеходный маршрут", color=VkKeyboardColor.PRIMARY, payload='{"button":1')
ways_keyboard.add_line()
ways_keyboard.add_button("Автомобильный маршрут", color=VkKeyboardColor.PRIMARY, payload='{"button":1')

helping_keyboard = VkKeyboard(one_time=True) # TODO
helping_keyboard.add_button("aaa")
helping_keyboard.add_line()
helping_keyboard.add_button("bbb")
helping_keyboard.add_line()
helping_keyboard.add_button("ccc")



user_state = {}
# States:
MAIN_MENU = 0
MENU_PLACES = 1
MENU_WAYS = 2
MENU_HELPING = 3
MENU_MAP = 4


def write_msg(user_id, message, keyboard=None, payload=None):
    if payload is None:
        payload = {}
    vk.method('messages.send', {'user_id': user_id,
                                'random_id': random.randint(0, 2 ** 63),
                                'message': message,
                                'keyboard': keyboard,
                                })


def get_number_from_message(message: str):
    num = ''
    message = message.strip()
    for c in message:
        if c.isnumeric():
            num += c
        else:
            break
    return int(num) if num else None


def go_to_main_menu(user_id):
    write_msg(user_id, "Выбери действие:", keyboard=main_keyboard.get_keyboard())
    user_state[user_id] = MAIN_MENU


def go_to_places_menu(user_id):
    names = []
    for index, place in enumerate(places.places_list):
        names.append("{}) {}".format(index, place))
    write_msg(user_id, PLACES_MESSAGE)
    write_msg(user_id, "\n".join(names))
    user_state[user_id] = MENU_PLACES


def go_to_ways_menu(user_id):
    write_msg(user_id, WAYS_MESSAGE)
    write_msg(user_id, "Выбери маршрут:", keyboard=ways_keyboard.get_keyboard())
    user_state[user_id] = MENU_WAYS


def go_to_helping_menu(user_id):
    write_msg(user_id, "Как ты хочешь помочь?", keyboard=helping_keyboard.get_keyboard())
    user_state[user_id] = MENU_HELPING


def send_map(user_id):
    write_msg(user_id, INTERACTIVE_MAP_MESSAGE)


def get_button_number(payload):
    if payload is not None:
        payload = json.loads(payload)
    if payload is not None and 'button' in payload:
        return payload['button']
    else:
        return None


def not_a_button(user_id, keyboard):
    write_msg(user_id, "Я не понял :(. Нажми на кнопочку!", keyboard=keyboard.get_keyboard())


def mainLoop():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            from_id = event.obj.from_id

            if from_id not in user_state:
                write_msg(from_id, "Привет, это чат-бот города Жуковский!")
                go_to_main_menu(from_id)
            elif user_state[from_id] == MAIN_MENU:
                button_number = get_button_number(event.obj.payload)

                if button_number == 1:
                    go_to_places_menu(from_id)
                elif button_number == 2:
                    go_to_ways_menu(from_id)
                elif button_number == 3:
                    go_to_helping_menu(from_id)
                elif button_number == 4:
                    send_map(from_id)
                else:
                    not_a_button(from_id, main_keyboard)

            elif user_state[from_id] == MENU_PLACES:
                number = get_number_from_message(event.obj.text)
                if number is None:
                    write_msg(from_id, "Нужно написать число!")
                else:
                    write_msg(from_id, "Ура, ты написал число {}".format(number))
                    go_to_main_menu(from_id)

mainLoop()
