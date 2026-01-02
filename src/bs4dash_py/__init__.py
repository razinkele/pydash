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


# Server-side helpers for updating controlbar from Python
def show_controlbar(*args, **kwargs):
    return _lazy_import("show_controlbar", "server")(*args, **kwargs)


def hide_controlbar(*args, **kwargs):
    return _lazy_import("hide_controlbar", "server")(*args, **kwargs)


def toggle_controlbar(*args, **kwargs):
    return _lazy_import("toggle_controlbar", "server")(*args, **kwargs)


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
    # server helpers
    "show_controlbar",
    "hide_controlbar",
    "toggle_controlbar",
]
