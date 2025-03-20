# import datetime as dt
#
# notification_time = dt.time(hour=15, minute=30)
#
# async def check_and_send_notifications():
#     now = dt.datetime.now().time()
#     if now.hour == notification_time.hour and now.minute == notification_time.minute:
#         await bot.send_message(user_id, "SEND_NOTIFICATION")