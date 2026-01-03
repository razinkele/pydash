"""bs4dash_py - minimal MVP package"""

__version__ = "0.0.1"

# Lazy import helpers to avoid requiring backend packages at import time (useful for tests)
import importlib


def _lazy_import(name, module="layout"):
    mod = importlib.import_module(f"{__name__}.{module}")
    return getattr(mod, name)


# Dash-based helpers (default MVP)
def dashboard_page(*args, **kwargs):
    return _lazy_import("dashboard_page", "layout")(*args, **kwargs)


def navbar(*args, **kwargs):
    return _lazy_import("navbar", "layout")(*args, **kwargs)


def sidebar(*args, **kwargs):
    return _lazy_import("sidebar", "layout")(*args, **kwargs)


def box(*args, **kwargs):
    return _lazy_import("box", "layout")(*args, **kwargs)


# Shiny-for-Python helpers
def dashboard_page_shiny(*args, **kwargs):
    return _lazy_import("dashboard_page_shiny", "shiny_layout")(*args, **kwargs)


def navbar_shiny(*args, **kwargs):
    return _lazy_import("navbar_shiny", "shiny_layout")(*args, **kwargs)


def sidebar_shiny(*args, **kwargs):
    return _lazy_import("sidebar_shiny", "shiny_layout")(*args, **kwargs)


def box_shiny(*args, **kwargs):
    return _lazy_import("box_shiny", "shiny_layout")(*args, **kwargs)


def body_shiny(*args, **kwargs):
    return _lazy_import("body_shiny", "shiny_layout")(*args, **kwargs)


def footer_shiny(*args, **kwargs):
    return _lazy_import("footer_shiny", "shiny_layout")(*args, **kwargs)


def dashboard_brand_shiny(*args, **kwargs):
    return _lazy_import("dashboard_brand_shiny", "shiny_layout")(*args, **kwargs)


def controlbar_shiny(*args, **kwargs):
    return _lazy_import("controlbar_shiny", "shiny_layout")(*args, **kwargs)


# convenience helpers
def value_box_shiny(*args, **kwargs):
    return _lazy_import("value_box_shiny", "shiny_layout")(*args, **kwargs)


def info_box_shiny(*args, **kwargs):
    return _lazy_import("info_box_shiny", "shiny_layout")(*args, **kwargs)


def tabs_shiny(*args, **kwargs):
    return _lazy_import("tabs_shiny", "shiny_layout")(*args, **kwargs)


def tab_item_shiny(*args, **kwargs):
    return _lazy_import("tab_item_shiny", "shiny_layout")(*args, **kwargs)


def menu_item_shiny(*args, **kwargs):
    return _lazy_import("menu_item_shiny", "shiny_layout")(*args, **kwargs)


def menu_group_shiny(*args, **kwargs):
    return _lazy_import("menu_group_shiny", "shiny_layout")(*args, **kwargs)


def navbar_item_shiny(*args, **kwargs):
    return _lazy_import("navbar_item_shiny", "shiny_layout")(*args, **kwargs)


def navbar_user_menu_shiny(*args, **kwargs):
    return _lazy_import("navbar_user_menu_shiny", "shiny_layout")(*args, **kwargs)


def breadcrumb_shiny(*args, **kwargs):
    return _lazy_import("breadcrumb_shiny", "shiny_layout")(*args, **kwargs)


def sidebar_header_shiny(*args, **kwargs):
    return _lazy_import("sidebar_header_shiny", "shiny_layout")(*args, **kwargs)


def sidebar_divider_shiny(*args, **kwargs):
    return _lazy_import("sidebar_divider_shiny", "shiny_layout")(*args, **kwargs)


# Server-side helpers for updating controlbar from Python
def show_controlbar(*args, **kwargs):
    return _lazy_import("show_controlbar", "server")(*args, **kwargs)


def hide_controlbar(*args, **kwargs):
    return _lazy_import("hide_controlbar", "server")(*args, **kwargs)


def toggle_controlbar(*args, **kwargs):
    return _lazy_import("toggle_controlbar", "server")(*args, **kwargs)


def update_sidebar_badges(*args, **kwargs):
    return _lazy_import("update_sidebar_badges", "server")(*args, **kwargs)


def update_sidebar_active(*args, **kwargs):
    return _lazy_import("update_sidebar_active", "server")(*args, **kwargs)


def update_navbar_items(*args, **kwargs):
    return _lazy_import("update_navbar_items", "server")(*args, **kwargs)


def update_tab_content(*args, **kwargs):
    return _lazy_import("update_tab_content", "server")(*args, **kwargs)


__all__ = [
    "dashboard_page",
    "navbar",
    "sidebar",
    "box",
    "dashboard_page_shiny",
    "navbar_shiny",
    "sidebar_shiny",
    "box_shiny",
    "body_shiny",
    "footer_shiny",
    "dashboard_brand_shiny",
    "controlbar_shiny",
    "value_box_shiny",
    "info_box_shiny",
    "tabs_shiny",
    "tab_item_shiny",
    "menu_item_shiny",
    "menu_group_shiny",
    "navbar_item_shiny",
    "breadcrumb_shiny",
    "sidebar_header_shiny",
    "sidebar_divider_shiny",
    # server helpers
    "show_controlbar",
    "hide_controlbar",
    "toggle_controlbar",
    "update_sidebar",
    "update_navbar_tabs",
    "update_sidebar_badges",
    "update_sidebar_active",
    "update_navbar_items",
    "update_tab_content",
]
