import logging
import re


class IgnoreHandledUpdatesFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        """Отключаем сообщения, содержащие "Update id=... is handled"""
        return not re.search(r"Update id=\d+ is handled", record.getMessage())


def setup_logger():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logging.getLogger("aiogram").setLevel(logging.DEBUG)

    logger = logging.getLogger('aiogram.event')
    logger.addFilter(IgnoreHandledUpdatesFilter())
