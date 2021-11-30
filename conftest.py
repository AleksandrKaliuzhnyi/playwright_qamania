import json
import os.path
from pytest import fixture
from playwright.sync_api import Playwright, sync_playwright
from page_objects.application import App
import settings
import json


@fixture(scope='session')
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope='session')
def desktop_app(get_playwright, request):
    # conditions if use addoption
    # base_url = request.config.getoption('--base_url')
    # conditions if use getini
    # base_url = request.config.getini('base_url')
    # conditions if use addoption
    # conditions if use json config
    base_url = request.config.getoption('--base_url')
    app = App(get_playwright, base_url=base_url)
    # conditions if use settings.py
    # app = App(get_playwright,  base_url=settings.BASE_URL)
    app.goto('/')
    yield app
    app.close()


@fixture(scope='session')
def desktop_app_auth(desktop_app, request):
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    desktop_app.goto("/login")
    desktop_app.login(**config)
    yield desktop_app


def pytest_addoption(parser):
    # addoption
    parser.addoption('--base_url', action='store', default='http://127.0.0.1:8000')
    # addini
    # parser.addini('base_url', help='base url of site under test', default='http://127.0.0.1:8000')
    # json config
    parser.addoption('--secure', action='store', default='secure.json')


def load_config(file):
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(config_file) as cfg:
        return json.loads(cfg.read())
