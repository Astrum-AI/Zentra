from enum import Enum


class ButtonVariant(str, Enum):
    none = "none"
    primary = "primary"
    secondary = "secondary"
    destructive = "destructive"
    outline = "outline"
    ghost = "ghost"
    link = "link"


class ButtonIconPosition(str, Enum):
    start = "start"
    end = "end"
