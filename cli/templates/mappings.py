from pydantic_core import Url
from cli.conf.types import MappingDict
from cli.templates.ui.attributes import (
    alt_attribute,
    calendar_attributes,
    collapsible_attributes,
    input_otp_attributes,
    param_attr,
    nextjs_link_attributes,
    size_attribute,
    slider_attributes,
    src_attribute,
    str_attr,
    toggle_attributes,
)
from cli.templates.ui.content import (
    alert_content,
    avatar_content,
    checkbox_content,
    collapsible_content,
    input_otp_content,
    radio_group_content,
    scroll_area_content,
    select_content,
    text_alert_dialog_content,
    text_content,
    tooltip_content,
)
from cli.templates.ui.imports import (
    alert_imports,
    collapsible_imports,
    image_imports,
    input_opt_imports,
    radio_group_imports,
    slider_imports,
    static_img_imports,
)
from cli.templates.ui.logic import calendar_logic, collapsible_logic

from pydantic import BaseModel


# Components made up of other Zentra models using a 'content' or 'items' attribute
PARENT_COMPONENTS = [
    "Button",
    "ScrollArea",
    "Toggle",
    "ToggleGroup",
    "Tooltip",
]

# Dictionary of components with containers around them
# (classname, attributes)
COMPONENTS_TO_WRAP = {
    "Checkbox": 'className="flex items-top space-x-2"',
}


# Components that have a "use client" import at the top of their file
USE_CLIENT_COMPONENTS = [
    "Calendar",
    "Checkbox",
    "Collapsible",
    "Image",
]

# Components that have "useState"
USE_STATE_COMPONENTS = [
    "Calendar",
    "Collapsible",
]


COMPONENT_ATTR_MAPPING = {
    "Calendar": lambda comp: calendar_attributes(comp),
    "Collapsible": lambda comp: collapsible_attributes(comp),
    "InputOTP": lambda comp: input_otp_attributes(comp),
    "Link": lambda comp: nextjs_link_attributes(comp),
    "Slider": lambda comp: slider_attributes(comp),
    "Toggle": lambda comp: toggle_attributes(comp),
}


COMMON_ATTR_MAPPING = {
    "id": lambda value: str_attr("id", value),
    "url": lambda _: "asChild",
    "href": lambda value: str_attr("href", value)
    if isinstance(value, (str, Url))
    else None,
    "name": lambda value: str_attr("htmlFor", value),
    "type": lambda value: str_attr("type", value),
    "placeholder": lambda value: str_attr("placeholder", value),
    "variant": lambda value: str_attr("variant", value) if value != "default" else None,
    "size": lambda value: size_attribute(value),
    "disabled": lambda value: "disabled" if value else None,
    "apiEndpoint": lambda value: str_attr("apiEndpoint", value),
    "num_inputs": lambda value: param_attr("maxLength", value),
    "key": lambda key: param_attr("key", key),
    "target": lambda value: str_attr("target", value),
    "styles": lambda value: str_attr("className", value),
    "src": lambda value: src_attribute(value),
    "alt": lambda alt: alt_attribute(alt),
    "width": lambda width: param_attr("width", width),
    "height": lambda height: param_attr("height", height),
    "checked": lambda checked: param_attr("checked", checked),
    "pressed": lambda pressed: param_attr("pressed", pressed),
    "color": lambda value: str_attr("color", value),
    "stroke_width": lambda value: param_attr("strokeWidth", value),
    "min": lambda value: param_attr("min", value),
    "max": lambda value: param_attr("max", value),
    "step": lambda value: param_attr("step", value),
    "orientation": lambda value: str_attr("orientation", value),
    "default_value": lambda value: str_attr("defaultValue", value),
}


ADDITIONAL_IMPORTS_MAPPING = {
    "Collapsible": lambda _: collapsible_imports(),
    "InputOTP": lambda comp: input_opt_imports(comp),
    "RadioGroup": lambda _: radio_group_imports(),
    "StaticImage": lambda img: static_img_imports(img),
    "Image": lambda comp: image_imports(comp),
    "Avatar": lambda comp: image_imports(comp),
    "Slider": lambda _: slider_imports(),
    "Alert": lambda comp: alert_imports(comp),
}


COMPONENT_CONTENT_MAPPING = {
    "Checkbox": lambda cb: checkbox_content(cb),
    "Collapsible": lambda comp: collapsible_content(comp),
    "RadioGroup": lambda rg: radio_group_content(rg),
    "ScrollArea": lambda sa: scroll_area_content(sa),
    "Select": lambda select: select_content(select),
    "Alert": lambda alert: alert_content(alert),
    "TextAlertDialog": lambda ad: text_alert_dialog_content(ad),
    "Tooltip": lambda tt: tooltip_content(tt),
    "Avatar": lambda avatar: avatar_content(avatar),
    "InputOTP": lambda otp: input_otp_content(otp),
}


COMMON_CONTENT_MAPPING = {
    "text": lambda value: text_content(value),
}


COMMON_LOGIC_MAPPING = {
    "Calendar": lambda comp: calendar_logic(comp),
    "Collapsible": lambda comp: collapsible_logic(comp),
}


class JSXMappings(BaseModel):
    """A storage container for JSX mappings."""

    common_attrs: MappingDict
    component_attrs: MappingDict
    common_content: MappingDict
    component_content: MappingDict
    common_logic: MappingDict
    additional_imports: MappingDict
    wrappers: dict[str, str]
    use_client_map: list[str]
    use_state_map: list[str]
    parent_components: list[str]


MAPPING_DICT = {
    "common_attrs": COMMON_ATTR_MAPPING,
    "component_attrs": COMPONENT_ATTR_MAPPING,
    "common_content": COMMON_CONTENT_MAPPING,
    "component_content": COMPONENT_CONTENT_MAPPING,
    "common_logic": COMMON_LOGIC_MAPPING,
    "additional_imports": ADDITIONAL_IMPORTS_MAPPING,
    "wrappers": COMPONENTS_TO_WRAP,
    "use_client_map": USE_CLIENT_COMPONENTS,
    "use_state_map": USE_STATE_COMPONENTS,
    "parent_components": PARENT_COMPONENTS,
}

JSX_MAPPINGS = JSXMappings(**MAPPING_DICT)
