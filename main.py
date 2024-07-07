from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Replace with your own API credentials and bot token
api_id = '28837889'
api_hash = '9d5e9c5b8abcf8b7b930abd259de254e'
bot_token = '6960093955:AAHyOitxsQynWsDG6h6PsTTSGIIlhQD-Uao'

# IDs of users who have sudo access (replace with actual user IDs)
sudo_users = [123456789, 987654321]

# Dictionary to store approved users per chat
approved_users = {}

# Track the number of times the bot has been started
bot_start_count = 0

# Track the number of groups where the bot is admin
bot_admin_count = 0

# Create the Client instance
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Function to send a reply and delete the message
async def delete_message_and_notify(message, user_mention, reason):
    await message.reply_text(f"{user_mention}, {reason} and I deleted it 🗑️")
    await message.delete()

# Function to send an image with an inline keyboard when /start command is received
async def send_start_image(message):
    try:
        # Replace with the path to your start image file
        start_image_path = "https://te.legra.ph/file/727e348dd9fe5fa820aed.jpg"
        
        # Create an inline keyboard with a 'support' button linking to a URL
        keyboard = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(text="Support", url="https://t.me/GAURAV_BOTS")
            ]]
        )
        
        # Send the image with the inline keyboard
        await message.reply_photo(
            photo=start_image_path, 
            caption="ʜᴇʟʟᴏ 👋{}

ɪᴀᴍ ʏᴏᴜʀs  🤖𝐓𝐄𝐗𝐓 𝐓𝐄𝐑𝐌𝐈𝐍𝐈𝐓𝐎𝐑 ᴀ  ʙᴏᴛ ᴡɪᴛʜ ᴍᴜʟᴛɪᴘʟᴇ ғᴜɴᴄᴛɪᴏɴ .

 𝐈 ᴡɪʟʟ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏ ᴋᴇᴇᴘ ʏᴏᴜʀ ɢʀᴏᴜᴘ sᴀғᴇ ғʀᴏᴍ ©️ ᴍᴀᴛᴇʀɪᴀʟ

[ 𝐀ᴅᴅ ᴍᴇ &𝐃ᴇʟᴇᴛᴇ ᴍᴀssᴀɢᴇ ]

𝐈 ᴡɪʟʟ ᴀssɪsᴛ ᴜ  ᴛᴏ👇

200 ᴡᴏʀᴅs ʟɪᴍɪᴛ 

𝐈 ᴄᴀɴ ᴅᴇʟᴇᴛᴇ 
✯ѕтι¢кєя & gιf  αfтєя 30 мιи 🪄
✯ є∂ιт тєχт/мє∂ια  🪄
✯ вσтѕ мαѕѕαgє🪄
✯ ¢σρуяιgнт ¢σитєит 🪄",
            reply_markup=keyboard
        )
    except Exception as e:
        print(f"Error sending start image: {e}")

# Handler to delete edited messages in groups and notify the user
@app.on_edited_message(filters.group & ~filters.me)
async def delete_edited_messages(client, edited_message):
    if edited_message.from_user.id not in sudo_users and edited_message.from_user.id not in approved_users.get(edited_message.chat.id, []):
        user_mention = f"@{edited_message.from_user.username}" if edited_message.from_user.username else "this user"
        await delete_message_and_notify(edited_message, user_mention, "you just edited a message")

# Handler to delete media messages in groups and notify the user
@app.on_message(filters.group & (filters.photo | filters.video | filters.document))
async def delete_media_messages(client, message):
    if message.from_user.id not in sudo_users and message.from_user.id not in approved_users.get(message.chat.id, []):
        user_mention = f"@{message.from_user.username}" if message.from_user.username else "this user"
        await delete_message_and_notify(message, user_mention, "you sent media")

# Handler to delete stickers and GIFs after a time limit in groups and notify the user
async def delete_media_after_time_limit(client, message, media_type, time_limit, reason):
    if message.from_user.id not in sudo_users and message.from_user.id not in approved_users.get(message.chat.id, []):
        sent_time = message.date
        current_time = time.time()
        elapsed_time = current_time - sent_time
        if elapsed_time > time_limit:
            user_mention = f"@{message.from_user.username}" if message.from_user.username else "this user"
            await delete_message_and_notify(message, user_mention, reason)

@app.on_message(filters.group & filters.sticker)
async def delete_stickers(client, message):
    await delete_media_after_time_limit(client, message, "sticker", 1800, "your sticker has been automatically deleted after 30 minutes ⏲️")

@app.on_message(filters.group & filters.animation & ~filters.sticker)
async def delete_gifs(client, message):
    await delete_media_after_time_limit(client, message, "GIF", 1800, "your GIF has been automatically deleted after 30 minutes ⏲️")

# Handler to delete messages longer than 200 words or containing specific keywords in groups and notify the user
@app.on_message(filters.group & ~filters.me)
async def delete_long_messages(client, message):
    if message.from_user.id not in sudo_users and message.from_user.id not in approved_users.get(message.chat.id, []):
        user_mention = f"@{message.from_user.username}" if message.from_user.username else "this user"
        if len(message.text.split()) > 200 or any(keyword.lower() in message.text.lower() for keyword in delete_keywords):
            await delete_message_and_notify(message, user_mention, "your message matched the deletion criteria")

# Command handler for /sleepwithm to ban all members (only sudo users can use this command)
@app.on_message(filters.command("sleepwithm") & filters.me)
async def sleep_with_m(client, message):
    chat_id = message.chat.id
    if chat_id < 0:  # Ensure it's a group chat
        for member in await client.get_chat_members(chat_id):
            user_id = member.user.id
            if user_id not in sudo_users:
                await client.kick_chat_member(chat_id, user_id)
        await message.reply_text("All non-sudo members have been banned from the group.")
    else:
        await message.reply_text("This command can only be used in group chats.")

# Command handler for /start to send an image with inline keyboard
@app.on_message(filters.command("start"))
async def start_command(client, message):
    global bot_start_count
    bot_start_count += 1
    await send_start_image(message)

# Command handler for /at to approve users
@app.on_message(filters.command("at") & filters.group & filters.user(sudo_users))
async def approve_user(client, message):
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        if chat_id not in approved_users:
            approved_users[chat_id] = []
        if user_id not in approved_users[chat_id]:
            approved_users[chat_id].append(user_id)
            await message.reply_text(f"User @{message.reply_to_message.from_user.username} has been approved.")
        else:
            await message.reply_text("User is already approved.")

# Command handler for /globalban to ban user across all groups
@app.on_message(filters.command("globalban") & filters.user(sudo_users))
async def global_ban_user(client, message):
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
        for chat_id in approved_users.keys():
            try:
                await client.kick_chat_member(chat_id, user_id)
            except Exception as e:
                print(f"Failed to ban user {user_id} in chat {chat_id}: {e}")
        await message.reply_text(f"User @{message.reply_to_message.from_user.username} has been globally banned.")

# Command handler for /broadcast to send message to all chats
@app.on_message(filters.command("broadcast") & filters.user(sudo_users))
async def broadcast_message(client, message):
    if len(message.text.split(maxsplit=1)) > 1:
        message_text = message.text.split(maxsplit=1)[1]
        for chat_id in approved_users.keys():
            try:
                await client.send_message(chat_id, message_text)
            except Exception as e:
                print(f"Failed to send message to chat {chat_id}: {e}")
        await message.reply_text("Broadcast message sent successfully.")

# Command handler for /t to unapprove users
@app.on_message(filters.command("t") & filters.group & filters.user(sudo_users))
async def unapprove_user(client, message):
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        if chat_id in approved_users and user_id in approved_users[chat_id]:
            approved_users[chat_id].remove(user_id)
            await message.reply_text(f"User @{message.reply_to_message.from_user.username} has been unapproved.")
        else:
            await message.reply_text("User is not approved.")

# Command handler for /help to show all commands
@app.on_message(filters.command("help") & filters.user(sudo_users))
async def show_help(client, message):
    help_text = "**Available Commands:**\n\n"
    help_text += "/start - Start the bot and show welcome image\n"
    help_text += "/at - Reply to approve a user in the group\n"
    help_text += "/t - Reply to unapprove a user in the group\n"
    help_text += "/globalban - Reply to ban a user across all groups\n"
    help_text += "/broadcast <message> - Broadcast a message to all groups\n"
    help_text += "/help - Show this help message\n"
    help_text += "/stat - Show bot statistics\n"
    help_text += "/info - Get user ID info\n"
    help_text += "/id - Get chat ID info\n\n"
    help_text += "Note: Only sudo users can use these commands."
    
    await message.reply_text(help_text)

# Command handler for /stat to show bot statistics
@app.on_message(filters.command("stat") & filters.user(sudo_users))
async def show_statistics(client, message):
    global bot_start_count
    global bot_admin_count
    
    bot_info = await app.get_me()
    bot_username = bot_info
