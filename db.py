import sqlite3 as sq
from aiogram import types, F, Router
from aiogram import html

async def db_start():
    global db, cur

    db = sq.connect('dinners.db')
    cur = db.cursor()

    if db:
        cur.execute("DELETE FROM dinners")
        cur.execute("CREATE TABLE IF NOT EXISTS dinners(user_id TEXT PRIMARY KEY, name TEXT, dinner TEXT, lanch TEXT, starttime TEXT)")
        db.commit()

    if not db:
        cur.execute("CREATE TABLE IF NOT EXISTS dinners(user_id TEXT PRIMARY KEY, name TEXT, dinner TEXT, lanch TEXT, starttime TEXT)")
    db.commit()
    



async def create_dinner(user_id, name, dinner, lanch, starttime):
    user = cur.execute("SELECT * FROM dinners WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO dinners VALUES(?,?,?,?,?)",(user_id, name, dinner, lanch, starttime))
        cur.execute("UPDATE dinners SET name = '{}', dinner = '{}', lanch = '{}', starttime= '{}' WHERE user_id == '{}'".format(name, dinner, lanch, starttime, user_id))
        db.commit()
    else:
        cur.execute("UPDATE dinners SET dinner = '{}', lanch = '{}', starttime= '{}' WHERE user_id == '{}'".format(dinner, lanch, starttime, user_id))
        db.commit()


async def create_lanch(user_id, name, dinner, lanch, starttime):
    user = cur.execute("SELECT * FROM dinners WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO dinners VALUES(?,?,?,?,?)",(user_id, name, dinner, lanch, starttime))
        cur.execute("UPDATE dinners SET name = '{}', dinner = '{}', lanch = '{}', starttime= '{}' WHERE user_id == '{}'".format(name, dinner, lanch, starttime, user_id))
        db.commit()
    else:
        cur.execute("UPDATE dinners SET dinner = '{}', lanch = '{}', starttime= '{}' WHERE user_id == '{}'".format(dinner, lanch, starttime, user_id))
        db.commit()

async def delete_din_lanch(user_id):
    user = cur.execute("SELECT 1 FROM dinners WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if user:
        cur.execute("DELETE FROM dinners WHERE user_id == '{key}'".format(key=user_id)).fetchone()
        db.commit()

def on_dinner_lanch():
    user_din=cur.execute("SELECT name, starttime FROM dinners  WHERE dinner == 1").fetchall()
    user_lanch=cur.execute("SELECT name, starttime FROM dinners WHERE lanch == 1").fetchall()
    text = ''
    text_din = 'никого'
    text_lanch = 'никого'
    if user_din:
        text_din = ''
        for row in user_din:            
            text_din += f"{row[0]} c {row[1]}\n"
            if user_lanch:
                text_lanch = ''
                for row in user_lanch:                
                    text_lanch += f"{row[0]} c {row[1]}\n"
            text = f"{html.bold('На обеде:')}\n{text_din}\n{html.bold('На перерыве:')}\n{text_lanch}"
        return text
          
    elif user_lanch:
        text_lanch = ''
        for row in user_lanch:            
            text_lanch += f"{row[0]} c {row[1]}\n"
            if user_din:
                for row in user_din:
                    text_din = ''
                    text_din += f"{row[0]} c {row[1]}\n"
            text = f"{html.bold('На обеде:')}\n{text_din}\n\n{html.bold('На перерыве:')}\n{text_lanch}"
        return text
    
    else:
        text = f"{html.bold('На обеде:')}\n{text_din}\n\n{html.bold('На перерыве:')}\n{text_lanch}"
        return text

