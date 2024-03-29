import re
from pydantic import Field, HttpUrl, ValidationInfo, field_validator
from pydantic_core import PydanticCustomError

from cli.templates.ui import (
    ButtonJSX,
    IconButtonJSX,
    CalendarJSX,
    CheckboxJSX,
    CollapsibleJSX,
    InputJSX,
    InputOTPJSX,
    LabelJSX,
)

from zentra.core import Component, Icon
from zentra.core.enums.ui import (
    ButtonSize,
    ButtonVariant,
    ButtonIconPosition,
    IconButtonSize,
    InputOTPPatterns,
    InputTypes,
)


def has_valid_pattern(*, pattern: str, value: str) -> bool:
    match = re.match(pattern, value)
    return bool(match)


class Button(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Button component focusing on text.

    Parameters:
    - `text` (`str`) - the text displayed inside the button
    - `url` (`str, optional`) - the URL the button links to. `None` by default. When `None` removes it from `Button`
    - `variant` (`str, optional`) - the style of the button. Valid options: `['default', 'secondary', 'destructive', 'outline', 'ghost', 'link']`. `default` by default
    - `size` (`str, optional`) - the size of the button. Valid options: `['default', 'sm', 'lg']`. `default` by default
    - `disabled` (`bool, optional`) - adds the disabled property, preventing it from being clicked. `False` by default
    """

    text: str = Field(min_length=1)
    url: HttpUrl = None
    variant: ButtonVariant = "default"
    size: ButtonSize = "default"
    disabled: bool = False

    def attr_str(self) -> str:
        return ButtonJSX.attributes(
            url=self.url, variant=self.variant, size=self.size, disabled=self.disabled
        )

    def content_str(self) -> str:
        return self.text


class IconButton(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Button component with a [Radix UI Icon](https://www.radix-ui.com/icons).

    Parameters:
    - `icon` (`Icon`) - the [Radix UI Icon](https://www.radix-ui.com/icons) to add inside the button
    - `icon_position` (`str, optional`) - the position of the icon inside the button. When set to `start`, icon appears before the text. When `end`, it appears after the text. `start` by default. Valid options: `['start', 'end']`
    - `text` (`str, optional`) - the text displayed inside the button. `None` by default. When `None` removes it from `Button`
    - `url` (`str, optional`) - the URL the button links to. `None` by default. When `None` removes it from `Button`
    - `variant` (`str, optional`) - the style of the button. Valid options: `['default', 'secondary', 'destructive', 'outline', 'ghost', 'link']`. `default` by default
    - `size` (`str, optional`) - the size of the button. Valid options: `['default', 'sm', 'lg', 'icon']`. `icon` by default
    - `disabled` (`bool, optional`) - adds the disabled property, preventing it from being clicked. `False` by default
    """

    icon: Icon
    icon_position: ButtonIconPosition = "start"
    text: str = None
    url: HttpUrl = Field(default=None)
    variant: ButtonVariant = "default"
    size: IconButtonSize = "icon"
    disabled: bool = False

    def attr_str(self) -> str:
        return IconButtonJSX.attributes(
            url=self.url, variant=self.variant, size=self.size, disabled=self.disabled
        )

    def content_str(self) -> str:
        return IconButtonJSX.main_content(
            text=self.text, icon=self.icon, icon_position=self.icon_position
        )


class Calendar(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Calendar component.

    Parameters:
    - `id` (`str`) - an identifier for the component. Prepended to `get` and `set` for the `useState()` hook. Must be `lowercase` or `camelCase` and up to a maximum of `15` characters

    Example:
    1. `id='monthly'` ->
        `const [monthlyDate, monthlySetDate] = useState(new Date());"`
    2. `id='yearlyCalendar'` ->
        `const [yearlyCalendarDate, yearlyCalendarSetDate] = useState(new Date());"`
    """

    id: str = Field(min_length=1, max_length=15)

    @field_validator("id")
    def validate_id(cls, id: str) -> str:
        if not has_valid_pattern(pattern=r"^[a-z]+(?:[A-Z][a-z]*)*$", value=id):
            raise PydanticCustomError(
                "string_pattern_mismatch",
                "must be lowercase or camelCase",
                dict(wrong_value=id, pattern="^[a-z]+(?:[A-Z][a-z]*)*$"),
            )
        return id

    def unique_logic_str(self) -> str:
        return CalendarJSX.unique_logic(id=self.id)

    def attr_str(self) -> str:
        return CalendarJSX.attributes(id=self.id)


class Checkbox(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Checkbox component.

    Parameters:
    - `id` (`str`) - an identifier for the component. Must be `lowercase` or `camelCase` and up to a maximum of `15` characters
    - `label` (`str`) - the text associated to the checkbox
    - `more_info` (`str, optional`) - additional information to add under the checkbox. `None` by default. When `None` removes it from `Checkbox`
    - `disabled` (`bool, optional`) - adds the disabled property, preventing it from being selected. `False` by default
    """

    id: str = Field(min_length=1, max_length=15)
    label: str = Field(min_length=1)
    more_info: str = None
    disabled: bool = False

    @field_validator("id")
    def validate_id(cls, id: str) -> str:
        if not has_valid_pattern(pattern=r"^[a-z]+(?:[A-Z][a-z]*)*$", value=id):
            raise PydanticCustomError(
                "string_pattern_mismatch",
                "must be lowercase or camelCase",
                dict(wrong_value=id, pattern="^[a-z]+(?:[A-Z][a-z]*)*$"),
            )
        return id

    def attr_str(self) -> str:
        return CheckboxJSX.attributes(id=self.id, disabled=self.disabled)

    def below_content_str(self) -> str:
        content = CheckboxJSX.main_content(id=self.id, label=self.label)

        if self.more_info:
            content += CheckboxJSX.more_info(info=self.more_info)

        content += "</div>"
        return content


class MultiCheckbox(Component):
    """
    A Zentra model for multiple [shadcn/ui](https://ui.shadcn.com/) Checkbox components.

    Parameters:
    - `items` (`list[Checkbox]`) - a list of Checkbox components. Requires a `minimum` of `2` items
    """

    items: list[Checkbox] = Field(min_length=2)

    # TODO: add logic specific to `Forms`


class Collapsible(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Collapsible component.

    Parameters:
    - `id` (`str`) - an identifier for the component. Prepended to `get` and `set` for the `useState()` hook. Must be `lowercase` or `camelCase` and up to a maximum of `15` characters
    - `title` (`str`) - the main heading of the collapsible
    - `items` (`list[str]`) - a list of strings representing the text to add into each collapsible block. Requires a `minimum` of `1` item
    """

    id: str = Field(min_length=1, max_length=15)
    title: str = Field(min_length=1)
    items: list[str] = Field(min_length=1)

    @field_validator("id")
    def validate_id(cls, id: str) -> str:
        if not has_valid_pattern(pattern=r"^[a-z]+(?:[A-Z][a-z]*)*$", value=id):
            raise PydanticCustomError(
                "string_pattern_mismatch",
                "must be lowercase or camelCase",
                dict(wrong_value=id, pattern="^[a-z]+(?:[A-Z][a-z]*)*$"),
            )
        return id

    def unique_logic_str(self) -> str:
        return CollapsibleJSX.unique_logic(id=self.id)

    def attr_str(self) -> str:
        return CollapsibleJSX.attributes(id=self.id)

    def content_str(self) -> str:
        title = CollapsibleJSX.title(self.title)
        items_str = CollapsibleJSX.items(self.items)
        return title + items_str


class Combobox(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Combobox component.

    Parameters:
    - `name` (`str`) - the name of the component
    """

    # TODO: come back once 'popover' and 'command' created


class DatePicker(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) DatePicker component.

    Parameters:
    - `name` (`str`) - the name of the component
    """

    # TODO: come back once 'popover' created


class Input(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Input component.

    Inputs are extremely versatile as expressed in the [HTML Input docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/url). We've limited the attributes to the basics for simplicity. Once components are generated, you can edit them in the respective `.tsx` files with additional attributes if needed.

    Parameters:
    - `id` (`str`) - an identifier for the component. Must be `lowercase` or `camelCase` and up to a maximum of `15` characters
    - `type` (`str`) - the type of input field. Options `['text', 'email', 'password', 'number', 'file', 'tel', 'search', 'url', 'color']`
    - `placeholder` (`str`) - the placeholder text for the input
    - `disabled` (`bool, optional`) - adds the disabled property, preventing it from being selected. `False` by default
    """

    id: str = Field(min_length=1, max_length=15)
    type: InputTypes
    placeholder: str
    disabled: bool = False

    @field_validator("id")
    def validate_id(cls, id: str) -> str:
        if not has_valid_pattern(pattern=r"^[a-z]+(?:[A-Z][a-z]*)*$", value=id):
            raise PydanticCustomError(
                "string_pattern_mismatch",
                "must be lowercase or camelCase",
                dict(wrong_value=id, pattern="^[a-z]+(?:[A-Z][a-z]*)*$"),
            )
        return id

    def attr_str(self) -> str:
        return InputJSX.attributes(
            id=self.id,
            type=self.type,
            placeholder=self.placeholder,
            disabled=self.disabled,
        )


class InputOTP(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) InputOTP component.

    Parameters:
    - `num_inputs` (`int`) - the length of the OTP. E.g., 6 = 6 input slots. Must be a minimum of `1`
    - `num_groups` (`int, optional`) - the number of slot groups. E.g., `InputOTP(num_inputs=6, num_groups=2)` -> 2 groups of 3 input slots. `1` by default
    - `pattern` (`str, optional`) - a regex pattern to limit the OTP input values. Options include: `['digits_only', 'chars_only', 'digits_n_chars_only']` ([official patterns](https://github.com/guilhermerodz/input-otp/blob/master/packages/input-otp/src/regexp.ts)) or a `custom` variant. `None` by default

    Examples:
    1. A basic OTP without a pattern.
    ```python
    input = InputOTP(num_inputs=6, num_groups=2)
    ```
    into ->
    ```jsx
    import { InputOTP, InputOTPGroup, InputOTPSlot, InputOTPSeparator } from '../ui/input-otp'

    <InputOTP maxLength={6}>
        <InputOTPGroup>
            <InputOTPSlot index={0} />
            <InputOTPSlot index={1} />
            <InputOTPSlot index={2} />
        </InputOTPGroup>
        <InputOTPSeparator />
        <InputOTPGroup>
            <InputOTPSlot index={3} />
            <InputOTPSlot index={4} />
            <InputOTPSlot index={5} />
        </InputOTPGroup>
    </InputOTP>
    ```

    2. A basic OTP with an official pattern and single group.
    ```python
    input = InputOTP(num_inputs=6, pattern='digits_only')
    ```
    into ->
    ```jsx
    import { InputOTP, InputOTPGroup, InputOTPSlot } from '../ui/input-otp'
    import { REGEXP_ONLY_DIGITS } from "input-otp"

    <InputOTP
        maxLength={6}
        pattern={REGEXP_ONLY_DIGITS}
    >
        <InputOTPGroup>
            <InputOTPSlot index={0} />
            <InputOTPSlot index={1} />
            <InputOTPSlot index={2} />
            <InputOTPSlot index={3} />
            <InputOTPSlot index={4} />
            <InputOTPSlot index={5} />
        </InputOTPGroup>
    </InputOTP>
    ```

    3. An OTP with a custom pattern and 3 groups.
    ```python
    input = InputOTP(num_inputs=6, num_groups=3, pattern=r"([\^$.|?*+()\[\]{}])")
    ```
    into ->
    ```jsx
    import { InputOTP, InputOTPGroup, InputOTPSlot, InputOTPSeparator } from '../ui/input-otp'

    <InputOTP
        maxLength={6}
        pattern="([\^$.|?*+()\[\]{}])"
    >
        <InputOTPGroup>
            <InputOTPSlot index={0} />
            <InputOTPSlot index={1} />
        </InputOTPGroup>
        <InputOTPSeparator />
        <InputOTPGroup>
            <InputOTPSlot index={2} />
            <InputOTPSlot index={3} />
        </InputOTPGroup>
        <InputOTPSeparator />
        <InputOTPGroup>
            <InputOTPSlot index={4} />
            <InputOTPSlot index={5} />
        </InputOTPGroup>
    </InputOTP>
    ```
    """

    num_inputs: int = Field(ge=1)
    num_groups: int = Field(default=1, ge=1)
    pattern: InputOTPPatterns | str = None

    @field_validator("num_groups")
    def validate_num_groups(num_groups: int, info: ValidationInfo) -> int:
        num_inputs = info.data.get("num_inputs")
        if num_groups > num_inputs:
            raise PydanticCustomError(
                "size_out_of_bounds",
                f"cannot have more groups ({num_groups}) than input slots ({num_inputs})\n",
                dict(wrong_value=num_groups, input_size=num_inputs),
            )
        return num_groups

    @field_validator("pattern")
    def validate_pattern(pattern: str) -> str:
        if pattern not in InputOTPPatterns:
            try:
                re.compile(pattern)
            except re.error:
                official_patterns = [pattern.value for pattern in InputOTPPatterns]
                raise PydanticCustomError(
                    "invalid_regex_pattern",
                    f"must be an official pattern option ({official_patterns}) or a valid regex string\n",
                    dict(wrong_value=pattern, official_patterns=official_patterns),
                )
        return pattern

    def attr_str(self) -> str:
        return InputOTPJSX.attributes(num_inputs=self.num_inputs, pattern=self.pattern)

    def content_str(self) -> str:
        return InputOTPJSX.main_content(
            num_inputs=self.num_inputs, num_groups=self.num_groups
        )

    def extra_imports_str(self) -> str | None:
        return InputOTPJSX.extra_imports(pattern=self.pattern)


class Label(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Label component.

    Parameters:
    - `id` (`str`) - an identifier for the component. Must be `lowercase` or `camelCase` and up to a maximum of `15` characters
    - `text` (`str`) - the descriptive text to put into the label
    """

    id: str = Field(min_length=1, max_length=15)
    text: str = Field(min_length=1)

    @field_validator("id")
    def validate_id(cls, id: str) -> str:
        if not has_valid_pattern(pattern=r"^[a-z]+(?:[A-Z][a-z]*)*$", value=id):
            raise PydanticCustomError(
                "string_pattern_mismatch",
                "must be lowercase or camelCase",
                dict(wrong_value=id, pattern="^[a-z]+(?:[A-Z][a-z]*)*$"),
            )
        return id

    def attr_str(self) -> str:
        return LabelJSX.attributes(id=self.id)

    def content_str(self) -> str:
        return LabelJSX.main_content(text=self.text)


class RadioGroup(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) RadioGroup component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class ScrollArea(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) ScrollArea component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Select(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Select component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Slider(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Slider component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Switch(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Switch component.

    Parameters:
    - `disabled` (`bool, optional`) - a flag for disabling the switch component. Default is `False`
    - `read_only` (`bool, optional`) - a flag for making the switch read only. Default is `False`. Indicates that the element is not editable, but is otherwise operable. More information on [Read only](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-readonly)
    """

    disabled: bool = False
    read_only: bool = False


class Tabs(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Tabs component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Textarea(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Textarea component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class Toggle(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Toggle component.

    Parameters:
    - `name` (`str`) - the name of the component
    """


class ToggleGroup(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) ToggleGroup component.

    Parameters:
    - `name` (`str`) - the name of the component
    """
