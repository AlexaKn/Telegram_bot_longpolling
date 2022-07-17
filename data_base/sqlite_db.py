import sqlite3 as sq
from create_bot import dp, bot

def sql_start():
    global base,cur
    base = sq.connect('flowers_data.db')
    cur = base.cursor()
    if base:
        print('Data base connected!')
    base.execute('CREATE TABLE IF NOT EXISTS shop(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO shop VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_read(message):
    for ret in cur.execute('SELECT * FROM shop').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nDescription: {ret[2]}\nPrice {ret[-1]}')

async def sql_read2():
    return cur.execute('SELECT * FROM shop').fetchall()

async def sql_delete_command(data):
    cur.execute('DELETE FROM shop WHERE name == ?', (data))
    base.commit()