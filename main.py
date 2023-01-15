import os.path
import random
import time
# from background import keep_alive
from config import tg_bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from string import ascii_letters, ascii_uppercase
from random import sample
from aiogram.utils.markdown import hbold, hunderline, hitalic, hcode

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

l_min = 4
l_max = 24


def generate_pass(pass_length):
    abc = ascii_letters  # все английские буквы маленькие и большие
    number = '1234567890'
    special = '[]{}()!@#$%^&*'
    # соединим все, сделав букв чуть больше чем цифр и символов
    all_symbols = (abc * 4 + number + special) * 4
    # сгенерируем пароль длиной на 3 символа меньше...
    password = sample(all_symbols, pass_length - 3)
    # ..добавим одну большую букву
    password.append(random.choice(ascii_uppercase))
    # ..одну цифру
    password.append(random.choice(number))
    # ..и один символ
    password.append(random.choice(special))
    # и всё перемешаем
    random.shuffle(password)
    # а потом соединим в троку
    password = ''.join(password)
    return password


@dp.message_handler(commands=['minmax'])
async def minmax_command(message: types.Message):
    global l_min, l_max
    c, a, b = message.text.split()
    if int(a) < 4:
        await message.reply(
            'Как ни крути, нельзя создать пароль меньше 4 символов. 🤷‍')
    l_min = int(a)
    l_max = int(b)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(
        'Привет. Напиши сколько ты хотел бы, чтобы было символов в пароле.')


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(
        f'Я генерирую пароли от {l_min} до {l_max} символов.\n'
        f'Но если ты хочешь задать другой минимум и максимум, введи специальную команду'
        f' "/minmax n m" , где n - минимальное, m максимальное число символов пароля'
    )


@dp.message_handler()
async def get_password(message: types.Message):
    pass_length = message.text

    try:
        pass_length = int(pass_length)
        if pass_length > l_max or pass_length < l_min:
            # file_path = os.path.join()
            print('demo-media/pics/nelzya.jpg')
            caption = f'Нельзя просто так взять и задать пароль меньше {hcode(l_min)} или больше {hcode(l_max)}'
            await bot.send_photo(message.chat.id,
                                 open('demo-media/pics/nelzya.jpg', 'rb'),
                                 caption=caption)
        else:
            password = generate_pass(pass_length)
            await message.answer('Чуточку терпения) Генерирую...')
            time.sleep(2)
            await message.answer(f'Ваш пароль: {password}')
            await bot.send_photo(message.chat.id, open('demo-media/pics/ok.jpg', 'rb'))
    except Exception as ex2:
        print(ex2)
        await message.answer(f'Необходимо ввести числа от {l_min} до {l_max}')


if __name__ == '__main__':
    executor.start_polling(dp)
