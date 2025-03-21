from enum import Enum

from src.bot.functions.style import b


class Texts(str, Enum):
    not_implemented = "🚧 Данная функция пока не реализована"
    plan_is_not_created = "Вы еще не выбрали задачи. Сначала создайте их"
    there_id_not_completed_plan = "У вас есть незакрытые планы. Сначала закройте их"
    plan_was_created = "✅ Задачи добавлены"
    need_plan = (
        f"Введите топ-3 {b('самые важные задачи')} в порядке приоритета."
        "\n\n"
        "Вы можете ввести и большее количество задач, "
        "но говорят (хз кто, но не суть), "
        "что оптимальное число главных задач на день равно трем."
        "\n\n"
        "Пример:\n"
        "1. Самая главная задача\n"
        "2. Главная, но поменьше\n"
        "3. Тоже главная, но еще поменьше\n"
    )
    report_bug_to_max = (
        "Бот пока в разработке, так что могут быть баги."
        "\n\n"
        "Напишите пожалуйста о баге @kudrmax (можно голосовым)"
    )
