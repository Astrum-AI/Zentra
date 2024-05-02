import re

from pydantic import HttpUrl
from zentra.core.enums.ui import InputOTPPatterns
from zentra.nextjs import Link, StaticImage, Url
from zentra.ui.control import Slider, Toggle


def str_attr(name: str, value: str) -> str:
    """A helper function for creating string attribute strings, such as `color="red"`."""
    return f'{name}="{value}"'


def param_attr(name: str, value: int | str, backticks: bool = False) -> str:
    """A helper function for creating parameter attribute strings, such as `size={48}`, `checked={false}`, or ```alt={`I have a {param} here`}```."""
    if backticks:
        return f"{name}={{`{value}`}}"

    return f"{name}={{{value}}}"


def query_attr(values: dict[str, str | dict[str, str]]) -> str:
    """A helper function for creating query attribute strings, such as:
    ```jsx
    {
        pathname: "/dashboard",
        query: {
            name: "test", second: "test2"
        },
    }
    ```
    Returned as a compressed string like so:
    `{ pathname: "/dashboard", query: { name: "test", second: "test2" }, }`.

    Values are wrapped in `{ }` automatically.

    Example usage:
    ```python
    query_attr(values=)
    ```
    """

    def query_items(values: dict[str, str]) -> list[str]:
        query_list = ["{", "}"]
        for name, vals in values.items():
            query_list.insert(-1, f'{name}: "{vals}",')
        return query_list

    query_list = []
    for name, vals in values.items():
        if isinstance(vals, str):
            query_list.append(f'{name}: "{vals}",')
        else:
            queries = " ".join(query_items(vals))
            query_list.append(f"{name}: {queries},")

    return " ".join(["{"] + query_list + ["}"])


def size_attribute(value: str | int, attr_name: str = "size") -> str:
    """Returns a string for the `size` attribute based on its given value."""
    if isinstance(value, str) and value != "default":
        return str_attr(attr_name, value)

    elif isinstance(value, int):
        return param_attr(attr_name, value)


def src_attribute(value: str | HttpUrl | StaticImage, attr_name: str = "src") -> str:
    """Returns a string for the `src` attribute based on its given value."""
    if isinstance(value, str):
        if value.startswith("http"):
            return str_attr(attr_name, value)
        elif value.startswith("$"):
            return param_attr(attr_name, value[1:])

    else:
        return param_attr(attr_name, value.name)


def alt_attribute(alt: str, attr_name: str = "alt") -> str:
    """Returns a string for the `alt` attribute based on its given value."""
    values = alt.split(" ")
    param_str = False

    new_alt = []
    for word in values:
        if word and word.startswith("$"):
            word = "{" + word[1:] + "}"
            param_str = True
        new_alt.append(word)

    if param_str:
        return param_attr(attr_name, " ".join(new_alt), backticks=True)

    return str_attr(attr_name, " ".join(new_alt))


def calendar_attributes(name: str) -> list[str]:
    """Returns a list of strings for the Calendar attributes based on a given name value."""
    return [
        str_attr("mode", "single"),
        param_attr("selected", f"{name}Date"),
        param_attr("onSelect", f"{name}SetDate"),
        str_attr("className", "rounded-md border"),
    ]


def collapsible_attributes(name: str) -> list[str]:
    """Returns a list of strings for the Collapsible attributes based on a given name value."""
    return [
        param_attr("open", f"{name}IsOpen"),
        param_attr("onOpenChange", f"{name}SetIsOpen"),
        str_attr("className", "w-[350px] space-y-2"),
    ]


def input_otp_attributes(pattern: str) -> list[str] | None:
    """Returns a list of strings for the InputOTP attributes based on a given pattern value."""
    if pattern:
        return [
            param_attr("pattern", InputOTPPatterns(pattern).name)
            if pattern in InputOTPPatterns
            else str_attr("pattern", re.compile(pattern).pattern)
        ]

    return None


def nextjs_link_attributes(link: Link) -> list[str]:
    """Returns a list of strings for the Link attributes based on its given values."""
    attributes = []

    if isinstance(link.href, Url):
        queries = {
            "pathname": link.href.pathname,
            "query": link.href.query,
        }
        attributes.append(param_attr("href", query_attr(queries)))

    if link.replace:
        attributes.append("replace")

    if not link.scroll:
        attributes.append(param_attr("scroll", str(link.scroll).lower()))

    if link.prefetch is not None:
        attributes.append(param_attr("prefetch", str(link.prefetch).lower()))

    return attributes


def slider_attributes(slider: Slider) -> list[str]:
    """Returns a list of strings for the Slider attributes based on its given values."""
    attrs = [
        param_attr("defaultValue", f"[{slider.value}]"),
        param_attr("min", slider.min),
        param_attr("max", slider.max),
        param_attr("step", slider.step),
        param_attr("className", f'cn("w-[{str(slider.bar_size)}%]", className)'),
        str_attr("orientation", slider.orientation),
    ]

    if slider.name:
        attrs.insert(0, str_attr("htmlFor", slider.name))

    return attrs


def toggle_attributes(toggle: Toggle) -> list[str]:
    """Returns a list of strings for the Toggle attributes based on its given values."""
    return [
        str_attr(
            "aria-label",
            f'Toggle{f' {toggle.style}' if toggle.style != "default" else ''}',
        )
    ]
