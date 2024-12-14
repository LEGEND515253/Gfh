import random
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from datetime import datetime, timedelta
from telegram.constants import ParseMode

# Your bot token here
BOT_TOKEN = "7406747605:AAGsaexpkhrKRJhRKR9hrKfK1eF3uvcF5nc"
ADMIN_ID = 1441704343  # Replace with your Telegram User ID

# Store giveaway participants and log
participants = []
winner_log = []

# Giveaway settings
max_entries = 500  # Maximum number of participants
prize = "DDOS FILE"  # Default prize
giveaway_end_time = datetime.now() + timedelta(hours=1)  # Set giveaway duration to 1 hour
welcome_message = "🎉 Welcome to the Giveaway Bot! 🎉"

# Command: /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        welcome_message + "\n"
        "Commands:\n"
        "1️⃣ /JOINGIVEAWAY - Join the giveaway.\n"
        "2️⃣ /pick_winner - Pick a random winner (Admin only).\n"
        "3️⃣ /participants - Show the list of participants (Admin only).\n"
        "4️⃣ /setprize <prize> - Set the giveaway prize (Admin only).\n"
        "5️⃣ /timeleft - Show time remaining for the giveaway.\n"
        "6️⃣ /history - Show the winner history (Admin only)."
    )

# Command: /JOINGIVEAWAY
async def join_giveaway(update: Update, context: CallbackContext):
    if len(participants) >= max_entries:
        await update.message.reply_text("🚫 Sorry, the giveaway has reached the maximum number of participants!")
        return

    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name

    if user_id in [participant["id"] for participant in participants]:
        await update.message.reply_text("✅ You are already in the giveaway!")
    else:
        participants.append({"id": user_id, "name": username})
        await update.message.reply_text(f"🎟️ {username} has joined the giveaway!")

# Command: /pick_winner
async def pick_winner(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized to pick a winner!")
        return

    if not participants:
        await update.message.reply_text("🚫 No participants in the giveaway yet!")
        return

    winner = random.choice(participants)
    winner_id = winner['id']
    winner_name = winner['name']
    winner_log.append(winner_name)

    # The file link you want to send to the winner
    file_link = "https://t.me/+YhFGirPumqthZjVl"  # Replace with the actual file link

    # Notify the winner in the group
    await update.message.reply_text(f"🏆 Congratulations {winner_name}! You have won the giveaway. Please contact the admin @LEGENDXOPL.")
    
    # Send the file link to the winner via DM
    await context.bot.send_message(
        chat_id=winner_id,
        text=f"🎉 Congratulations {winner_name}! You won the giveaway. Please contact the admin @LEGENDXOPL for further instructions.\n\nHere is your file link: {file_link}"
    )

# Command: /participants
async def participants_list(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized to view the participant list!")
        return

    if not participants:
        await update.message.reply_text("🚫 No participants in the giveaway yet!")
        return

    participant_names = [participant["name"] for participant in participants]
    participant_list = "\n".join(participant_names)
    await update.message.reply_text(f"👥 List of participants:\n{participant_list}")

# Command: /setprize
async def set_prize(update: Update, context: CallbackContext):
    global prize
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized to set the prize!")
        return
    prize = " ".join(context.args) if context.args else "Gift Card"
    await update.message.reply_text(f"🎁 The prize for this giveaway has been set to: {prize}")

# Command: /timeleft
async def time_left(update: Update, context: CallbackContext):
    time_remaining = giveaway_end_time - datetime.now()
    if time_remaining.total_seconds() > 0:
        await update.message.reply_text(f"⏳ Time left for the giveaway: {str(time_remaining).split('.')[0]}")
    else:
        await update.message.reply_text("⏳ The giveaway has ended!")

# Command: /history
async def history(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized to view the history!")
        return

    if not winner_log:
        await update.message.reply_text("🚫 No winners yet!")
        return

    winner_history = "\n".join(winner_log)
    await update.message.reply_text(f"📝 Giveaway Winner History:\n{winner_history}")

# Command: /leave
async def leave_giveaway(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    participant_to_remove = next((participant for participant in participants if participant["id"] == user_id), None)

    if participant_to_remove:
        participants.remove(participant_to_remove)
        await update.message.reply_text(f"🚫 {update.effective_user.username or update.effective_user.first_name} has left the giveaway.")
    else:
        await update.message.reply_text("❌ You are not in the giveaway!")

# Main function
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("JOINGIVEAWAY", join_giveaway))
    application.add_handler(CommandHandler("pick_winner", pick_winner))
    application.add_handler(CommandHandler("participants", participants_list))
    application.add_handler(CommandHandler("setprize", set_prize))
    application.add_handler(CommandHandler("timeleft", time_left))
    application.add_handler(CommandHandler("history", history))
    application.add_handler(CommandHandler("leave", leave_giveaway))

    print("🤖 Giveaway Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
