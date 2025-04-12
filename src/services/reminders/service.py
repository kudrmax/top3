import datetime as dt
import logging

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from src.models.reminders.reminder_settings import ReminderSettingUpsert, ReminderSetting
from src.models.user import User
from src.services.plans.service import daily_plans_service
from src.services.scheduler.service import IJob, SchedulerService
from src.storage.postgres.repositories.reminder_serttings.repository import ReminderSettingRepository


class PlanReminderJob(IJob):
    def __init__(self, tg_id: int, time: dt.time):
        self.tg_id = tg_id
        self.time = time

    def id(self):
        return f"plan_reminder_{self.tg_id}_{self.time.hour}_{self.time.minute}"


class ReminderService(SchedulerService):
    def __init__(
            self,
            reminder_repository: ReminderSettingRepository,
            bot: Bot
    ):
        super().__init__()

        self.logger = logging.getLogger(self.__class__.__name__)

        self.reminder_repository = reminder_repository
        self.bot = bot

        self.init_schedule()

    def init_schedule(self):
        for reminder_setting in self.reminder_repository.get_all():
            if reminder_setting:
                user = User(reminder_setting.tg_id)
                self.schedule_reminders(user, None, reminder_setting)
            else:
                pass  # TODO add logging

    def _clear_schedule(self, user: User, reminder_settings: ReminderSetting | None) -> None:
        if not reminder_settings:
            return

        times = reminder_settings.get_times()
        jobs = [PlanReminderJob(user.tg_id, time) for time in times]

        self.remove_if_exists(jobs)

    def _add_creation_reminder_job(self, user: User, time: dt.time):
        self.add_job(
            func=self.send_creation_reminder,
            trigger_time=time,
            args=[user],
            job=PlanReminderJob(user.tg_id, time),
        )

    def _add_plan_reminder_job(self, user: User, time: dt.time):
        self.add_job(
            func=self.send_plan_reminder,
            trigger_time=time,
            args=[user],
            job=PlanReminderJob(user.tg_id, time),
        )

    def schedule_reminders(
            self,
            user: User,
            old_reminder_settings: ReminderSetting | None,
            new_reminder_settings: ReminderSetting
    ) -> None:
        if old_reminder_settings:
            self._clear_schedule(user, old_reminder_settings)

        time = new_reminder_settings.creation_reminder_time
        if time:
            self._add_creation_reminder_job(user, time)

        times = new_reminder_settings.reminder_times
        if times is not None and len(times) > 0:
            for time in times:
                self._add_plan_reminder_job(user, time)

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
