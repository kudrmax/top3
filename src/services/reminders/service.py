import datetime as dt
import logging

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from src.models.reminders.reminder_settings import ReminderSettingUpsert, ReminderSetting
from src.models.user import User
from src.services.plans.service import daily_plans_service
from src.storage.postgres.repositories.reminder_serttings.repository import ReminderSettingRepository


class Job:
    tg_id: int
    time: dt.time

    def __init__(self, tg_id: int, time: dt.time):
        self.tg_id = tg_id
        self.time = time

    def to_slug(self):
        return f"reminder_{self.tg_id}_{self.time.hour}_{self.time.minute}"


class ReminderService:
    def __init__(
            self,
            reminder_repository: ReminderSettingRepository,
            bot: Bot
    ):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.reminder_repository = reminder_repository
        self.bot = bot
        self.scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
        self.scheduler.start()
        self.init_schedule()

    def init_schedule(self):
        reminder_settings_list = self.reminder_repository.get_all()
        for reminder_setting in reminder_settings_list:
            if reminder_setting:
                user = User(reminder_setting.tg_id)
                self.schedule_reminders(user, None, reminder_setting)

    def schedule_reminders(
            self,
            user: User,
            old_reminder_settings: ReminderSetting | None,
            new_reminder_settings: ReminderSetting
    ) -> None:
        self._clear_schedule(user, old_reminder_settings)

        time = new_reminder_settings.creation_reminder_time
        if time:
            hour = time.hour
            minute = time.minute
            self.scheduler.add_job(
                self.send_creation_reminder,
                CronTrigger(hour=hour, minute=minute),
                args=[user],
                id=Job(user.tg_id, time).to_slug(),
            )

        times = new_reminder_settings.reminder_times
        if times is not None and len(times) > 0:
            for time in times:
                hour = time.hour
                minute = time.minute
                self.scheduler.add_job(
                    self.send_plan_reminder,
                    CronTrigger(hour=hour, minute=minute),
                    args=[user],
                    id=Job(user.tg_id, time).to_slug(),
                )

    async def send_creation_reminder(self, user: User) -> None:
        await self.bot.send_message(
            user.tg_id,
            "Напоминание: вы ещё не создали задачи на сегодня!"
        )

    async def send_plan_reminder(self, user: User) -> None:
        curren_plan = daily_plans_service.get_current(user)
        if curren_plan:
            plan = curren_plan.plan
            await self.bot.send_message(
                user.tg_id,
                f"Фокусируйтесь на главном. Ваши задачи:\n\n{plan}"
            )
        else:
            await self.send_creation_reminder(user)

    def update_user_settings(self, user: User, reminder_settings: ReminderSettingUpsert) -> None:
        old_reminder_settings = self.reminder_repository.get(user)

        self.reminder_repository.upsert(user, reminder_settings)

        new_reminder_settings = ReminderSetting(user.tg_id).init_from_upsert_model(reminder_settings)
        self.schedule_reminders(
            user,
            old_reminder_settings,
            new_reminder_settings
        )

    def _clear_schedule(self, user: User, reminder_settings: ReminderSetting | None) -> None:
        if not reminder_settings:
            return

        times = []

        time = reminder_settings.creation_reminder_time
        if time is not None:
            times.append(time)

        times = reminder_settings.reminder_times
        if times is not None and len(times) > 0:
            for time in times:
                times.remove(time)

        job_slugs = [Job(user.tg_id, time).to_slug() for time in times]

        for job_slug in job_slugs:
            if self.scheduler.get_job(job_slug):
                self.scheduler.remove_job(job_slug)
