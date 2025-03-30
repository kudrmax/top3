from enum import Enum
from typing import Any

from aiogram.fsm.context import FSMContext

from src.models.daily_plan import DailyPlanCreate
from src.models.user import User


class PropertyName(str, Enum):
    PLAN = 'plan'
    COUNT = 'count'
    DATE = 'date'


class CreateDailyPlanStateService:
    PLAN_CREATE = 'plan_create'

    @classmethod
    async def get_daily_plan_from_state(cls, user: User, state: FSMContext) -> DailyPlanCreate:
        data = await state.get_data()
        plan_create: DailyPlanCreate = data.get(cls.PLAN_CREATE)
        if plan_create is None:
            return DailyPlanCreate()
        return plan_create

    @classmethod
    async def add_daily_plan_to_state(cls, state: FSMContext, plan_create: DailyPlanCreate) -> None:
        await state.update_data({cls.PLAN_CREATE: plan_create})

    @classmethod
    async def add_data_to_state(cls, user: User, state: FSMContext, obj: Any, property_name: PropertyName):
        plan_create = await cls.get_daily_plan_from_state(user, state)
        match property_name.value:
            case PropertyName.PLAN:
                plan_create.plan = obj
            case PropertyName.COUNT:
                plan_create.count = obj
            case PropertyName.DATE:
                plan_create.date = obj
        await cls.add_daily_plan_to_state(state, plan_create)
