import pyrogram
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup as rkm, InlineKeyboardMarkup as km, InlineKeyboardButton as btn
import sqlite3
import os
import asyncio
import requests
from pyromod import listen
import uuid

api_id= 22350456
api_hash = "163ea40f6a5f53be2109cb87b74bfc12" 

status = False

token = "5393921528:AAEHuoKKespj_VKnz1pJaolG0nza-CDyNZc"
admin = 5191376406

aws = Client(
    "delete",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=token
)

conn = sqlite3.connect('delete_db.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        session TEXT
    )
''')

conn.commit()

@aws.on_message(filters.command("start"))
async def start_command(aws, message):
    if message.from_user.id == admin:
        await message.reply_text(text=f'''Welcome, {message.from_user.first_name}! 🍻\nThis is the bot pin delete ⚚\nDev: @u4060''', reply_markup=rkm(
            [
                [f"ℹ️ Info"],
                ["▶️ Start Bot", "▶️ Start Account"],
                ["➕ Add User", "➖ Delete User"],
                ["➕ Add Account", "➖ Delete Account"],
                ["⏹️ Stop Bot"],
                ["➖ Delete All Accounts"]
            ]
        ))
    else:
        await aws.send_message(message.chat.id, f'''Welcome, {message.from_user.first_name}! 🍻\nThis is the checker bot by: @u4060 🐊!
''', reply_to_message_id=message.message_id, reply_markup=km(
            inline_keyboard=[[btn(text="- Mr Aws ", url="https://t.me/EnginnerManAcc")]]
        ))

@aws.on_message(filters.text)
async def checker(aws, message):
    if message.from_user.id == admin:
        pass
    else:
        await aws.send_message(message.chat.id, f'''Sorry, you are not subscribed to use this bot. 🚫\nContact the bot dev for access.\nBy: [Aws ](https://t.me/EnginnerManAcc) 🐊''', reply_to_message_id=message.message_id, reply_markup=km(
            inline_keyboard=[[btn(text="- Aws ", url="https://t.me/EnginnerManAcc")]]
        ))
        return

    if message.text == 'ℹ️ Info':
	    try:
	        userre = open('user.txt', 'r').read().splitlines()
	        users = []
	        for userr in userre:
	            users.append(userr)
	        num_accounts = cursor.execute('SELECT COUNT(*) FROM sessions').fetchone()[0]
	        sessions_info = cursor.execute('SELECT id, session FROM sessions').fetchall()
	        sessions_text = "\n\n".join([f"ID: {session[0]}, Session: {session[1]}" for session in sessions_info])
	        users_text = "\n".join([f"USER: @{user}" for user in users])
	        open("sessions.txt", "w").write(sessions_text)
	        open("users.txt", "w").write(users_text)
	        files = ["users.txt", "sessions.txt"]
	        for i in files:
		        await aws.send_document(message.chat.id, i)
		        os.remove(i)
	        await aws.send_message(message.chat.id, "- Sessions and users Files .")
	        await aws.send_message(message.chat.id, text=f"ℹ️ Users: \n{users_text}\nℹ️ Accounts: {num_accounts}\nℹ️ Bot by: [Aws ](https://t.me/EnginnerManAcc)", disable_web_page_preview=True)
	    except Exception as e:
	        print(e)
	        await message.reply_text(text=f"ℹ️ User: None\nℹ️ Accounts: {num_accounts}\nℹ️ Bot by: [Aws ](https://t.me/EnginnerManAcc)", disable_web_page_preview=True)

    if message.text == "➕ Add User":
        try:
            os.remove("user.txt")
        except:
            pass
        user_input = await aws.ask(message.chat.id, f"➕ Send username to add:")
        username = user_input.text
        with open('user.txt', 'w') as user_file:
            user_file.write(str(username))
        await message.reply_text(f"➕ Username added: {username}")

    if message.text == "➖ Delete User":
        try:
            os.remove("user.txt")
        except:
            pass
        await message.reply_text(f"➖ Username deleted.")

    if message.text == '➖ Delete All Accounts':
        await message.reply_text("➖ Send /deleteall to delete all added accounts.")

    if message.text == '/deleteall':
        cursor.execute('DELETE FROM sessions')
        conn.commit()
        await message.reply_text("➖ All accounts deleted.")

    if message.text == "➕ Add Account":
	    user_input = await aws.ask(message.chat.id, f"➕ Send session to add:")
	    session = user_input.text
	    session_id = str(uuid.uuid4())  
	    session_chars_count = sum(c.isalnum() for c in session)
	    if session_chars_count <= 50:
	        await message.reply_text("➖ This is not a valid Pyrogram session. Please provide a valid session string.", reply_markup=km(
	            inline_keyboard=[[btn(text="- delete ", url="https://t.me/EnginnerManAcc")]]
	        ))
	        return
	    session_exists = cursor.execute('SELECT session FROM sessions WHERE session = ?', (session,)).fetchone()
	    if session_exists:
	        await message.reply_text("➖ This session already exists.", reply_markup=km(
	            inline_keyboard=[[btn(text="- Aws ", url="https://t.me/EnginnerManAcc")]]
	        ))
	    else:
	        cursor.execute('INSERT INTO sessions (id, session) VALUES (?, ?)', (session_id, session))  
	        conn.commit()
	        await message.reply_text(f"➕ Session account added with ID: {session_id}")


    if message.text == '⏹️ Stop Bot':
        await message.reply_text("⏹️ Stopping the checker bot...", reply_markup=km(
            inline_keyboard=[[btn(text="- Aws ", url="https://t.me/EnginnerManAcc")]]
        ))
        try:
            status = True
        except:
            pass

    if message.text == '▶️ Start Bot':
        try:
            os.remove('mode.txt')
        except:
            pass
        await message.reply_text("▶️ Started pinning users ⚚")
        sessions = cursor.execute('SELECT session FROM sessions').fetchall()
        clicks = 0
        status = True
        while status:
            for session in sessions:
                clicks += 1
                try:
                    api = Client("name_session", session_string=session[0], api_id=api_id, api_hash=api_hash)
                    await api.start()
                    username = open('user.txt', 'r').read().splitlines()
                    for username in username:
	                    try:
	                    	peer = await api.resolve_peer(username)
	                    	await api.invoke(await pyrogram.raw.functions.messages.get_peer_dialogs.GetPeerDialogs(peers=[peer]))
	                    except:
	                    	try:
	                    		t = await api.create_channel("- delete Checker")
	                    	except:
	                    		t = await api.create_group("- delete Checker")
	                    	finally:
	                    		t = await api.set_username(username)
	                    	await api.set_chat_username(t.id, username)
	                    	await api.update_profile(
	                            first_name="- delete Checker",
	                            bio="🐊 The delete checker account! ↬ by @u4060 🔥"
	                        )
	                    	me = await api.get_me()
	                    	phone = me.phone_number[:-2] + "*****"
	                    	await aws.send_video(message.chat.id, "https://t.me/u4060/148", caption=f"""
• 𝐖𝐞 𝐀𝐫𝐞 𝐊𝐢𝐧𝐠𝐬 𝐀𝐥𝐰𝐚𝐲𝐬 #𝟏
• 𝐔𝐬𝐞𝐫 ➞ : [ {username} ]
• 𝐂𝐏𝐒 ➞ : [ {clicks} ]
• 𝐓𝐢𝐦𝐞 𝐃𝐚𝐭𝐞 ➞ : [ 0 : 45 : 29 ]
• 𝐓𝐲𝐩𝐞 ➞ : [ 𝐀𝐜𝐜𝐨𝐮𝐧𝐭 ]
• 𝐊𝐢𝐧𝐠 ➞ : [ @u4060 ]
	""")
	                    	status = False
	                    	file = open("user.txt", "r").read()
	                    	new = file.replace(username, "")
	                    	file = open("user.txt", "w")
	                    	file.write(new)
	                    	continue
	                    	return
                except Exception as e:
                    error = f"{e}".replace("Telegram says: ", "").replace(
                        """ is required (caused by "account.UpdateUsername")""", " ").replace('420', '').replace(
                        """- The username is already in use by someone else (caused by "account.UpdateUsername")""",
                        "").replace(
                        "_WAIT_X", "").replace("seconds", "s").replace("400", '')
                    await message.reply_text(
                        f'''⤷ Clicks  ❲ {clicks} ❳\n⤷ Error with ↣ @{username}\n⌯ The error: \n\n{error}''')
                    if "401 USER_DEACTIVATED_BAN" in str(e) or "401 USER_DEACTIVATED" in str(e):
                        cursor.execute('DELETE FROM sessions WHERE session = ?', (session[0],))
                        conn.commit()
                        await aws.send_message(message.chat.id, f"⤷ Session is banned or not found, deleted.")
                        pass

aws.run()
