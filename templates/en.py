from datetime import datetime
from .base import LangContent


class ENLang(LangContent):
    @staticmethod
    def subject(name: str) -> str:
        return f"Payment Reminder - {name}"

    @staticmethod
    def body(
        name: str,
        payment_day: str = 2,
        items: list[str] = [],
        value: float = 0.0,
        pix_key: str = "",
    ) -> str:
        return f"""
            Hello {name}, today is the closing day of my bill.
            
            You have until the day {payment_day}/{datetime.now().month + 1} to pay what you owe me.
            
            Item(s) purchased with my card: {",".join(items)}
            
            Total amount: {value}

            My pix key for payment is: {pix_key}

            If you have already made the payment, please disregard this message.

            This is an automated message, do not reply to this email.
            """
