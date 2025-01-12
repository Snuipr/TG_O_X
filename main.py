import psycopg2
import random
import asyncio
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram import Bot, Dispatcher
from aiogram.types import Message


def add_new_user(id_user):
    player_user = random.choice(['x', 'o'])
    try:
        con = psycopg2.connect(dbname='krestiki_noliki', user='postgres', password='1', host='localhost', port='5432')
        print('Успешно')
    except:
        print("Ошибка подключения к базе данных")
        exit()
    cursor = con.cursor()
    try:
        insert_query = """ INSERT INTO krestiki(id, player, game_map) 
                                                VALUES (%s, %s, %s)"""
        cursor.execute(insert_query,(id_user, player_user, 111111111))
        con.commit()
        print("Успех")
    except:
        print("Ошибка добавления пользователя")
    cursor.close()  # закрываем курсор
    con.close()  # закрываем соединение


def get_table_info(id_user):
    id = []
    try:
        con = psycopg2.connect(dbname='krestiki_noliki', user='postgres', password='1', host='localhost', port='5432')
        print('Успешно')
    except:
        print("Ошибка подключения к базе данных")
        exit()
    cursor = con.cursor()
    cursor.execute("""SELECT id FROM krestiki""")
    cus = cursor.fetchall()
    for i in cus:
        id.append(i[0])
    if id_user in id:
        cursor.execute("""SELECT * from krestiki where id = %s and id = %s""",
                       (id_user, id_user))
        record = cursor.fetchall()
        return record
    cursor.close()
    con.close()
    add_new_user(id_user)
    con = psycopg2.connect(dbname='krestiki_noliki', user='postgres', password='1', host='localhost', port='5432')
    cursor = con.cursor()
    cursor.execute("""SELECT * from krestiki where id = %s and id = %s""",
                   (id_user, id_user))
    record = cursor.fetchall()
    cursor.close()
    con.close()  # закрываем соединение
    return record



def update_table(id_user, game_map, player, win = 0, lose = 0, draw = 0):
    infro = get_table_info(id_user)
    info = infro[0]
    try:
        con = psycopg2.connect(dbname='krestiki_noliki', user='postgres', password='1', host='localhost', port='5432')
        print('Успешно')
    except:
        print("Ошибка подключения к базе данных")
        exit()
    cursor = con.cursor()
    try:
        cursor.execute(""" UPDATE krestiki SET player=%s, win=%s, lose=%s, draw=%s, game_map=%s WHERE id=%s""",
                       (player, info[2]+win, info[3]+lose, info[4]+draw, game_map,  info[0]))
        con.commit()
        print("Успех")
    except:
        print("Ошибка изменения записи")
    cursor.close()  # закрываем курсор
    con.close()  # закрываем соединение
def checker_map(map):
    count = 0
    game_list = [map[i] for i in range(3)]
    deog_list = [map[i][j] for i in range(3) for j in range(3) if i == j]
    for i in range(3):
        s = []
        for j in range(3):
            s.append(map[j][i])
        game_list.append(s)
    s = []
    for x in range(2, -1, -1):
        s.append(map[count][x])
        count += 1
    game_list.append(deog_list)
    game_list.append(s)
    for i in game_list:
        if i.count("x") == 3:
            return 1
        if i.count("o") == 3:
            return 2
    return 0
def get_game_map(game_info):
    slovar = {1: "#", 2: "x", 3: "o"}
    answer = []
    s = []
    for i in str(game_info):
        n = slovar[int(i)]
        s.append(n)
        if len(s) == 3:
            answer.append(s)
            s = []
    return answer
def get_table_map(game_map):
    slovar = {'#': 1, 'x': 2, 'o': 3}
    answer = ''
    for i in game_map:
        for j in i:
            answer += str(slovar[j])
    return int(answer)

def restart_game(id_user, win = 0, lose = 0, draw = 0):
    game_map = 111111111
    player = random.choice(['x', 'o'])
    update_table(id_user, game_map, player, win, lose, draw)



kb1 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='0'), KeyboardButton(text='1'), KeyboardButton(text='2')],
                                    [KeyboardButton(text='3'), KeyboardButton(text='4'), KeyboardButton(text='5')],
                                    [KeyboardButton(text='6'), KeyboardButton(text='7'), KeyboardButton(text='8')],
                                    [KeyboardButton(text='Начать заново')]],
                          resize_keyboard=True)

bot = Bot(token='7639555111:AAFAvfiO18kgl23zHzwHKn38tWac9frIJcw')
ds = Dispatcher()


@ds.message()
async def start(message: Message):
    id_user = message.from_user.id
    game_info = get_table_info(id_user)[0]
    game_map = get_game_map(game_info[5])
    player = game_info[1]
    if message.text == "/start":
        await message.answer(f'Игру начинает {player} \n {game_map[0]} \n {game_map[1]} \n {game_map[2]}',
                             reply_markup=kb1)
    if str(message.text) == 'Начать заново':
        restart_game(id_user)
        game_info = get_table_info(id_user)[0]
        game_map = get_game_map(game_info[5])
        player = game_info[1]
        await message.answer('Игра начинается заново')
        await message.answer(f'Игру начинает {player}\n {game_map[0]} \n {game_map[1]} \n {game_map[2]}')
        return None
    if message.text.isdigit():
        if game_map[int(message.text) // 3][int(message.text) % 3] == '#':
            game_map[int(message.text) // 3][int(message.text) % 3] = player
            k = game_map[0].count('#') + game_map[1].count('#') + game_map[2].count('#')
            if k == 0:
                await message.answer(f'Ничья \n {game_map[0]}\n {game_map[1]}\n {game_map[2]}')
                restart_game(id_user, draw=1)
                game_info = get_table_info(id_user)[0]
                game_map = get_game_map(game_info[5])
                player = game_info[1]
                await message.answer('Игра начинается заново')
                await message.answer(f'Игру начинает {player}\n {game_map[0]} \n {game_map[1]} \n {game_map[2]}')
                return None
            if checker_map(game_map) == 1:
                await message.answer(f'Победа Крестика \n {game_map[0]}\n {game_map[1]}\n {game_map[2]}')
                restart_game(id_user, win=1)
                game_info = get_table_info(id_user)[0]
                game_map = get_game_map(game_info[5])
                player = game_info[1]
                await message.answer('Игра начинается заново')
                await message.answer(f'Игру начинает {player}\n {game_map[0]} \n {game_map[1]} \n {game_map[2]}')
                return None
            if checker_map(game_map) == 2:
                await message.answer(f'Победа Нолика \n {game_map[0]}\n {game_map[1]}\n {game_map[2]}')
                restart_game(id_user, lose=1)
                game_info = get_table_info(id_user)[0]
                game_map = get_game_map(game_info[5])
                player = game_info[1]
                await message.answer('Игра начинается заново')
                await message.answer(f'Игру начинает {player}\n {game_map[0]} \n {game_map[1]} \n {game_map[2]}')
                return None
            if player == "x":
                player = "o"
            elif player == "o":
                player = "x"
            table_map = get_table_map(game_map)
            update_table(id_user, table_map, player)
            game_info = get_table_info(id_user)[0]
            game_map = get_game_map(game_info[5])
            player = game_info[1]
            await message.answer(f'Теперь ход {player} \n {game_map[0]} \n {game_map[1]} \n {game_map[2]}')
        else:
            await message.answer('Извините это поле занято')


async def main():
    await ds.start_polling(bot)


asyncio.run(main())
                return None
            if checker_map(game_map) == 2:
                await message.answer(f'Победа Нолика \n {game_map[0]}\n {game_map[1]}\n {game_map[2]}')
                restart_game()
                await message.answer('Игра начинается заново')
                await message.answer(f'Игру начинает {player}\n {game_map[0]} \n {game_map[1]} \n {game_map[2]}')
                return None
            if player == "x":
                player = "o"
            elif player == "o":
                player = "x"
            await message.answer(f'Теперь ход {player} \n {game_map[0]} \n {game_map[1]} \n {game_map[2]}')
        else:
            await message.answer('Извините это поле занято')


async def main():
    await ds.start_polling(bot)


asyncio.run(main())
