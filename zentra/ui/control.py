from zentra.core import Component, Icon
from zentra.core.enums.ui import ButtonVariant, ButtonIconPosition


class Button(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Button component.

    Parameters:
    - name (str) - the name of the component.
    - text (str, optional) - the text displayed inside the button. Hidden by default.
    - url (str, optional) - the URL the button links to. Hidden by default.
    - variant (str, optional) - the style of the button. Valid options: `['none', 'primary', 'secondary', 'destructive', 'outline', 'ghost', 'link']`. `none` by default.
    - icon (Icon, optional) - the [Radix UI Icon](https://www.radix-ui.com/icons) to add inside the button. Hidden by default.
    - icon_position (str, optional) - the position of the icon inside the button. When set to `start`, icon appears before the text. When `end`, it appears after the text. `start` by default. Valid options: `['start', 'end']`.
    - icon_only (bool, optional) - converts the button to an icon only button. Ignores text parameter. `False` by default.
    - disabled (bool, optional) - adds the disabled property, preventing it from being clicked. `False` by default.
    """

    text: str = None
    url: str = None
    variant: ButtonVariant = "none"
    icon: Icon = None
    icon_position: ButtonIconPosition = "start"
    icon_only: bool = False
    disabled: bool = False


class Calendar(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Calendar component."""


class Checkbox(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Checkbox component."""


class Collapsible(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Collapsible component."""


class Combobox(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Combobox component."""


class DatePicker(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) DatePicker component."""


class Input(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Input component."""

    label: str
    placeholder: str
    read_only: bool = False


class Label(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Label component."""


class RadioGroup(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) RadioGroup component."""


class ScrollArea(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) ScrollArea component."""


class Select(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Select component."""


class Slider(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Slider component."""


class Switch(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Switch component."""


class Tabs(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Tabs component."""


class Textarea(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Textarea component."""


class Toggle(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Toggle component."""


class ToggleGroup(Component):
    """A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) ToggleGroup component."""
