from aiogram.utils.markdown import html_decoration as hd


def spoiler(text: str) -> str:
    return hd.spoiler(text)


def b(text: str) -> str:
    return hd.bold(text)


def i(text: str) -> str:
    return hd.italic(text)


def link(text: str, url: str) -> str:
    return hd.link(text, url)
