import logging
import datetime as dt
from abc import ABC, abstractmethod
from typing import Any, List

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


class IJob(ABC):

    @abstractmethod
    def id(self):
        pass


class SchedulerService:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
        self.scheduler.start()

    def add_job(
            self,
            func,
            trigger_time: dt.time,
            args: List[Any],
            job: IJob
    ):
        self.scheduler.add_job(
            func,
            CronTrigger(hour=trigger_time.hour, minute=trigger_time.minute),
            args=args,
            id=job.id(),
        )

    def _get_job(self, job: IJob):
        self.scheduler.get_job(job.id())

    def _remove_job(self, job: IJob):
        self.scheduler.remove_job(job.id())

    def remove_if_exists(self, jobs: List[IJob] | IJob):
        if isinstance(jobs, IJob):
            jobs = [jobs]
        for job in jobs:
            if self._get_job(job):
                self._remove_job(job)
