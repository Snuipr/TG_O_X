import random
import asyncio
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message


def checker_map(map):
    count = 0
    s = []
    game_list = [map[i] for i in range(3)]
    y_list = []
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


def restart_game():
    global game_map
    global player
    game_map = [["#", "#", "#"], ["#", "#", "#"], ["#", "#", "#"]]
    player = random.choice(['x', 'o'])


player: str = None
game_map = [["#", "#", "#"],
            ["#", "#", "#"],
            ["#", "#", "#"]]
kb1 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='0'), KeyboardButton(text='1'), KeyboardButton(text='2')],
                                    [KeyboardButton(text='3'), KeyboardButton(text='4'), KeyboardButton(text='5')],
                                    [KeyboardButton(text='6'), KeyboardButton(text='7'), KeyboardButton(text='8')],
                                    [KeyboardButton(text='Начать заново')]],
                          resize_keyboard=True)

bot = Bot(token='7639555111:AAFAvfiO18kgl23zHzwHKn38tWac9frIJcw')
ds = Dispatcher()


@ds.message()
async def start(message: Message):
    global game_map
    global player
    if message.text == "/start":
        restart_game()
        await message.answer(f'Игру начинает {player} \n {game_map[0]} \n {game_map[1]} \n {game_map[2]}',
                             reply_markup=kb1)
    if str(message.text) == 'Начать заново':
        restart_game()
        await message.answer('Игра начинается заново')
        await message.answer(f'Игру начинает {player}\n {game_map[0]} \n {game_map[1]} \n {game_map[2]}')
        return None
    if message.text.isdigit():
        if game_map[int(message.text) // 3][int(message.text) % 3] == '#':
            game_map[int(message.text) // 3][int(message.text) % 3] = player
            k = game_map[0].count('#') + game_map[1].count('#') + game_map[2].count('#')
            if k == 0:
                await message.answer(f'Ничья \n {game_map[0]}\n {game_map[1]}\n {game_map[2]}')
                restart_game()
                await message.answer('Игра начинается заново')
                await message.answer(f'Игру начинает {player}\n {game_map[0]} \n {game_map[1]} \n {game_map[2]}')
                return None
            if checker_map(game_map) == 1:
                await message.answer(f'Победа Крестика \n {game_map[0]}\n {game_map[1]}\n {game_map[2]}')
                restart_game()
                await message.answer('Игра начинается заново')
                await message.answer(f'Игру начинает {player}\n {game_map[0]} \n {game_map[1]} \n {game_map[2]}')
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