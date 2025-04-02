from .en import ENLang
from .pt import PTLang
from .base import LangContent

content_generators: dict[str, LangContent] = {"en": ENLang, "pt": PTLang}
