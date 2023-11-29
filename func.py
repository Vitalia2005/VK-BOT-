from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import schedule, threading
import time
import vk_api, vk
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from bs4 import BeautifulSoup
import requests

keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Погода', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('Погода на период', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('Таймер', color=VkKeyboardColor.NEGATIVE)

group_key = 'vk1.a.sOlkwAFQ_x2TRX-LvtlbY2p6ZQSNMVPDV9bEU6saBBTTUrC6HYOZnauZ51IBLzO-k5vEv2koEKBtC3hTMGnoC6IGTb6c1z5DN00xWs_qEx60frJraNgBt_51eBxPf5opaXp87w9y-ibsS9AWb1kPuEZyWU2KXGMMsDd136y7nGJwZ5tLwsuFa5McfdH6qW9oyAMC243BkQKySDQ-qErJvw'


class User:
    def __init__(self, user_id):
        self.id = user_id
        self.weather_button = False
        self.period_button = False
        self.city_button = False
        self.period_drygoi = False
        self.drygoi_per = False
        self.drygoi = False
        self.period = False
        self.timer = False
        self.time_button_city = False
        self.time_button_city_drygoi = False
        self.drygoi_timer = False
        self.timer_c = False
        self.town = get_city(user_id)
        self.timer_city = None
        self.timee = '12:00'
        self.per_city = self.town

    def __eq__(self, other):
        return self.id == other

    def restart(self):
        self.weather_button = False
        self.period_button = False
        self.period_drygoi = False
        self.drygoi_per = False
        self.drygoi = False
        self.period = False
        self.timer = False
        self.time_button_city = False
        self.time_button_city_drygoi = False
        self.drygoi_timer = False
        self.timer_c = False


TOKEN = 'vk1.a.i79WUQuV_SYr8-I4eLUAmWlKRjpmKmRytNRs100Ew4Erv7j1936K-CaousYcs8dyg2jChDMY6sanX-cndTYFpEYH-5nmtMu6TSPY6t0E3H1Bsv4zW_YlHGilqbZtOvsvVuIgFuqeZYZvS9HH2uArs2oHrPd81duBy8AIBfrsepcAaXtWu5nP-DKdcAiJvbHW'

'https://oauth.vk.com/authorize?client_id=51752937&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.131&state=123456'


def send_m(vk, event, city):
    vk.messages.send(user_id=event.user_id,
                     random_id=get_random_id(),
                     message=get_weather(city))


def get_city(user_id):
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()
    us = vk.users.get(user_id=user_id, fields='city')[0]
    if 'city' in us:
        return us['city']['title']
    return None


def get_many_weather(city):
    request = requests.get('https://sinoptik.ua/погода-' + city + '/10-дней')
    b = BeautifulSoup(request.text, "html.parser")
    p3 = b.select('.temperature .p3')
    if p3:
        weather1 = p3[0].getText()
        p4 = b.select('.temperature .p4')
        weather2 = p4[0].getText()
        p5 = b.select('.temperature .p5')
        weather3 = p5[0].getText()
        p6 = b.select('.temperature .p6')
        weather4 = p6[0].getText()
        result = []
        result.append(
            'Сегодня: ' + 'Утром: ' + weather1 + ' ' + weather2 + ' Днем: ' + weather3 + ' ' + weather4 + '\n')

        p4 = b.select('.main')
        weather5 = p4
        for el in weather5:
            result.append(str(int(el.select('.date')[0].getText())) + ' ' + el.select('.month')[0].getText() + ': ' +
                          el.select('.temperature')[0].getText() + '\n')
        return result
    return None


def get_weather(city):
    request = requests.get('https://sinoptik.ua/погода-' + city + '/10-дней')
    b = BeautifulSoup(request.text, "html.parser")
    p3 = b.select('.temperature .p3')
    if p3:
        weather1 = p3[0].getText()
        p4 = b.select('.temperature .p4')
        weather2 = p4[0].getText()
        p5 = b.select('.temperature .p5')
        weather3 = p5[0].getText()
        p6 = b.select('.temperature .p6')
        weather4 = p6[0].getText()
        result = 'Сегодня: ' + 'Утром: ' + weather1 + ' ' + weather2 + ' Днем: ' + weather3 + ' ' + weather4 + '\n'
        return result
    return None


# Кнопка Другой после кнопки Погода
def drygoi(user):
    user.drygoi = True
    return 'Введите город'


# Кнопка Другой (город) после кнопки Период
def period_drygoi(user):
    user.period_drygoi = True
    user.period_button = False
    return 'Введите город'


# Обычная погода city
def send_weather(user, city):
    w = get_weather(city)
    user.drygoi = False
    user.weather_button = False
    if w:
        return w
    else:
        return 'Такого города не существует'


# Погода с выбором города
def pogoda(user):
    user.weather_button = True
    if user.town:
        keyboard_city = VkKeyboard(one_time=True)
        keyboard_city.add_button('Другой', color=VkKeyboardColor.POSITIVE)
        keyboard_city.add_button(user.town, color=VkKeyboardColor.NEGATIVE)
        return keyboard_city, 'Выберите город на клавиатуре'
    else:
        user.drygoi = True
        return None, 'Введите город'


def nachat(user):
    global keyboard
    print(user.town)
    if user.town:
        if not user.city_button:
            keyboard.add_line()
            keyboard.add_button('Погода ' + user.town, color=VkKeyboardColor.NEGATIVE)
            user.city_button = True
    return 'Выберите действие на клавиатуре'


def pogoda_na_period(user):
    if user.town:
        user.period_button = True
        keyboard_city = VkKeyboard(one_time=True)
        keyboard_city.add_button('Другой', color=VkKeyboardColor.POSITIVE)
        keyboard_city.add_button(user.town, color=VkKeyboardColor.NEGATIVE)
        user.per_city = user.town
        return keyboard_city, 'Выберите город'
    else:
        user.period_drygoi = True
        return None, 'Введите город'


def period_drygoi_button(user, t):
    user.period_drygoi = False
    user.per_city = t
    w = get_weather(t)
    if w:
        user.period_button = False
        user.period = True
        keyboard_periods = VkKeyboard(one_time=True)
        keyboard_periods.add_button('3 дня', color=VkKeyboardColor.POSITIVE)
        keyboard_periods.add_button('7 дней', color=VkKeyboardColor.POSITIVE)
        keyboard_periods.add_button('Другой', color=VkKeyboardColor.NEGATIVE)
        return keyboard_periods, 'Выберите период'
    else:
        user.restart()
        return keyboard, 'Такого города не существует'


# Погода town
def pp(t):
    city = t[7::]
    w = get_weather(city)
    if w:
        return w
    else:
        return 'Такого города не существует'


def choose_period(user, t):
    if t == '3 дня':
        user.period = False
        w = get_many_weather(user.per_city)
        if w:
            return keyboard, ('\n').join(w[0:3])
        else:
            user.restart()
            return None, 'Ошибка. Такого города не существует'
    elif t == '7 дней':
        user.period = False
        w = get_many_weather(user.per_city)
        if w:
            return keyboard, ('\n').join(w[0:7])
    elif t == 'Другой':
        user.period = False
        user.drygoi_per = True
        return None, 'Введите число дней (макс. 10)'
    else:
        return keyboard, 'Неверный период'


def drygoi_period(user, t):
    try:
        val = int(t)
        user.drygoi_per = False
        user.period = False
        if val <= 10 and val >= 1:
            w = get_many_weather(user.per_city)
            if w:
                return keyboard, ('\n').join(w[0:val])
            else:
                user.restart()
                return keyboard, 'Такого города не существует'
        else:
            user.restart()
            return keyboard, 'Число должно быть от 1 до 10'
    except ValueError:
        user.restart()
        return keyboard, 'Это не число'


def timer(user):
    user.timer = True
    keyboard_timer = VkKeyboard(one_time=True)
    keyboard_timer.add_button('7:00', color=VkKeyboardColor.POSITIVE)
    keyboard_timer.add_button('12:00', color=VkKeyboardColor.POSITIVE)
    keyboard_timer.add_button('Другой', color=VkKeyboardColor.NEGATIVE)
    return keyboard_timer, 'Выберите время, в которое присылать вам погоду. Время указано в московском часовом поясе'


def timer_vr(user, t):
    if t == '7:00' or t == '12:00':
        user.timee = '07:00' if t == '7:00' else t
        user.timer = False
        user.timer_c = True
        user.time_button_city = True
        keyboard_city_timer = VkKeyboard(one_time=True)
        keyboard_city_timer.add_button('Другой', color=VkKeyboardColor.POSITIVE)
        if user.town:
            keyboard_city_timer.add_button(user.town, color=VkKeyboardColor.NEGATIVE)
            user.timer_city = user.town
            return keyboard_city_timer, 'Выберите город'
        else:
            user.time_button_city_drygoi = True
            user.time_button_city = False
            return None, 'Введите город'
    elif t == 'Другой':
        user.timer = False
        user.drygoi_timer = True
        return None, 'Введите время в формате чч:мм в московском часовом поясе'
    else:
        user.restart()
        return keyboard, 'Неверный формат данных'


def timer_city(user, t):
    user.drygoi_timer = False
    user.time_button_city = True
    if len(t.split(':')) == 2 and len(t.split(':')[0]) == 2 and len(t.split(':')[0]) == 2:
        user.timee = t
    else:
        user. restart()
        return keyboard, 'Ошибка. Неверный формат.'
    if user.town:
        keyboard_city_timer = VkKeyboard(one_time=True)
        keyboard_city_timer.add_button('Другой', color=VkKeyboardColor.POSITIVE)
        keyboard_city_timer.add_button(user.town, color=VkKeyboardColor.NEGATIVE)
        user.timer_city = user.town
        return keyboard_city_timer, 'Выберите город'
    else:
        user.time_button_city_drygoi = True
        user.time_button_city = False
        return None, 'Введите город'


def timer_drygoi_gorod(user):
    user.time_button_city_drygoi = True
    user.time_button_city = False
    return 'Введите город'


def set_timer(user, event):
    user.time_button_city_drygoi = False
    try:
        user.timer_city = event.text
        user.time_button_city = False
        schedule.every().day.at(user.timee, 'Europe/Moscow').do(send_m, vk, event, user.timer_city)
        return 'Таймер успешно установлен на ' + user.timee
    except Exception:
        user.restart()
        return 'Ошибка, неверный формат даных.'


def period(user, t):
    user.per_city = t
    w = get_weather(user.per_city)
    if w:
        user.period_drygoi = False
        user.period_button = False
        user.period = True
        keyboard_periods = VkKeyboard(one_time=True)
        keyboard_periods.add_button('3 дня', color=VkKeyboardColor.POSITIVE)
        keyboard_periods.add_button('7 дней', color=VkKeyboardColor.POSITIVE)
        keyboard_periods.add_button('Другой', color=VkKeyboardColor.NEGATIVE)
        return keyboard_periods, 'Выберите период'
    else:
        user.restart()
        return keyboard, 'Такого города не существует'
