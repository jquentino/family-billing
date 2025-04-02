from typing import Protocol


class LangContent(Protocol):
    @staticmethod
    def subject(name: str) -> str: ...

    @staticmethod
    def body(
        name: str,
        payment_day: int,
        items: list[str],
        value: float,
        pix_key: str,
    ) -> str: ...
