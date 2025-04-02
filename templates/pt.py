from datetime import datetime
from .base import LangContent


class PTLang(LangContent):
    @staticmethod
    def subject(name: str) -> str:
        return f"Lembrete de Pagamento - {name}"

    @staticmethod
    def body(
        name: str,
        payment_day: str = 2,
        items: list[str] = [],
        value: float = 0.0,
        pix_key: str = "",
    ) -> str:
        return f"""
            Olá {name}, hoje é o dia de fechamento da minha fatura.
            
            Você tem até o dia {payment_day}/{datetime.now().month + 1} para pagar o que me deve.
            
            Item(s) comprados com meu cartão: {",".join(items)}
            
            Valor total: {value}

            Minha chave pix para pagamento é: {pix_key}

            Se já realizou o pagamento, desconsidere essa mensagem.

            Esta é uma mensagem automática, não responda à este email.
            """
