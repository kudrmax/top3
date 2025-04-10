from aiogram.fsm.state import StatesGroup, State


class CreateState(StatesGroup):
    waiting_for_plan = State()
    waiting_for_count = State()
    waiting_for_date = State()


class CompleteState(StatesGroup):
    waiting_for_number = State()


class UpdateState(StatesGroup):
    waiting_for_text = State()
    waiting_for_number = State()
