
import streamlit as st
import datetime
import telegram
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler

# Replace with your actual token
TOKEN = '6457623134:AAG8VmCJT4_gQ-UJYwmDyeg0hEisRCrKmbA'


# Define the sleep cycle calculator function
def calculate_sleep_times(desired_wake_time):
    """Calculates ideal bedtimes based on the desired wake time.

    Args:
        desired_wake_time: A datetime object representing the desired wake-up time.

    Returns:
        A list of datetime objects representing ideal bedtimes.
    """

    ideal_bedtimes = []
    for cycles in range(3, 7):  # 3 to 6 cycles (adjust as needed)
        ideal_bedtime = desired_wake_time - datetime.timedelta(minutes=cycles * 90)
        ideal_bedtimes.append(ideal_bedtime)
    return ideal_bedtimes


# Define the 'start' command handler
async def start(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the '/start' command."""
    user = update.effective_user
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"Hello {user.first_name}! I'm a sleep cycle calculator. Tell me when you want to wake up, and I'll suggest ideal bedtimes.")


# Define the 'wake' command handler
async def wake(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the '/wake' command to calculate ideal bedtimes."""
    print("Wake  up time")
    try:
        wake_time_str = update.message.text.split('/wake ')[1].strip()
        wake_time = datetime.datetime.strptime(wake_time_str, "%H:%M").time()  # Example format

        # Create a datetime object with today's date and the specified wake time
        desired_wake_time = datetime.datetime.combine(datetime.date.today(), wake_time)

        ideal_bedtimes = calculate_sleep_times(desired_wake_time)

        # Format the bedtimes for display
        bedtime_messages = [f"For {cycles} cycles, try going to bed around {bedtime.strftime('%H:%M')}."
                            for cycles, bedtime in enumerate(ideal_bedtimes, start=3)]

        # Send the results to the user
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="\n".join(bedtime_messages))

    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"Oops, something went wrong. Please enter your wake-up time in the format HH:MM (e.g., /wake 07:30).")


# Build the application
def streamlit_app():
    st.title("Simple Streamlit App")
    st.write("This app is connected to a Telegram bot!")
    message = st.text_input("Enter a message:")
    if st.button("Send to Bot"):
        # Send the message to the Telegram bot
        # (You'll need to implement your own logic here)
        st.write("Message sent to bot!")

if __name__ == '__main__':
    # Start the Telegram bot in a separate thread
    #loop = asyncio.get_event_loop()
    #bot_thread = Thread(target=lambda: loop.run_until_complete(run_telegram_bot()))
    #bot_thread.start()
    streamlit_app()
    application = ApplicationBuilder().token(TOKEN).build()

    # Add handlers for the commands
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('wake', wake))

    # Run the application
    application.run_polling()
