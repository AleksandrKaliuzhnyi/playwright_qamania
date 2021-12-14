import logging
import json
import os.path
from pytest import fixture
from playwright.sync_api import Playwright, sync_playwright
from page_objects.application import App
from settings import *
import json
from helpers.web_service import WebService
from helpers.db import DataBase


@fixture(autouse=True, scope='session')
def preconditions():
    logging.info('Preconditions started')
    yield
    logging.info('Postconditions started')


@fixture(scope='session')
def get_web_service(request):
    base_url = request.config.getoption('--base_url')
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    web = WebService(base_url)
    web.login(**config['users']['UserRole1'])
    yield web
    web.close()


@fixture(scope='session')
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope='session', params=['chromium']) # 'firefox', 'webkit'], ids=['chromium', 'firefox', 'webkit'])
def get_browser(get_playwright, request):
    browser = request.param
    headless = request.config.getini('headless')
    if headless == 'True':
        headless = True
    else:
        headless = False

    if browser == 'chromium':
        yield get_playwright.chromium.launch(headless=headless)
    elif browser == 'firefox':
        yield get_playwright.firefox.launch(headless=headless)
    elif browser == 'webkit':
        yield get_playwright.webkit.launch(headless=headless)
    else:
        assert False, 'browser type unknown'


@fixture(scope='session')
def desktop_app(get_browser, request):
    # conditions if use addoption
    # base_url = request.config.getoption('--base_url')
    # conditions if use getini
    # base_url = request.config.getini('base_url')
    # conditions if use addoption
    # conditions if use json config
    base_url = request.config.getoption('--base_url')
    app = App(get_browser, base_url=base_url, **BROWSER_OPTIONS)
    # conditions if use settings.py
    # app = App(get_playwright,  base_url=settings.BASE_URL)
    app.goto('/')
    yield app
    app.close()


@fixture(scope='session')
def get_db(request):
    path = request.config.getini('db_path')
    db = DataBase(path)
    yield db
    db.close()


@fixture(scope='session')
def desktop_app_auth(desktop_app, request):
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    desktop_app.goto("/login")
    desktop_app.login(**config['users']['UserRole1'])
    yield desktop_app


@fixture(scope='session')
def desktop_app_bob(get_browser, request):
    base_url = request.config.getini('base_url')
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    app = App(get_browser, base_url=base_url, **BROWSER_OPTIONS)
    app.goto('/login')
    app.login(**config['users']['UserRole2'])
    yield app
    app.close()


@fixture(scope='session', params=['iPhone 11', 'Pixel 2'], ids=['iPhone 11', 'Pixel 2'])
def mobile_app(get_playwright, get_browser, request):
    # conditions if use addoption
    # base_url = request.config.getoption('--base_url')
    # conditions if use getini
    # base_url = request.config.getini('base_url')
    # conditions if use addoption
    # conditions if use json config
    base_url = request.config.getoption('--base_url')
    device = request.config.param
    device_config = get_playwright.devices.get(device)
    if device_config is not None:
        device_config.update(BROWSER_OPTIONS)
    else:
        device_config = BROWSER_OPTIONS
    app = App(get_browser, base_url=base_url, **device_config)
    # conditions if use settings.py
    # app = App(get_playwright,  base_url=settings.BASE_URL)
    app.goto('/')
    yield app
    app.close()


@fixture(scope='session')
def mobile_app_auth(mobile_app, request):
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    mobile_app.goto("/login")
    mobile_app.login(**config['users']['UserRole1'])
    yield mobile_app


def pytest_addoption(parser):
    # addoption
    parser.addoption('--base_url', action='store', default='http://127.0.0.1:8000')
    # addini
    parser.addini('base_url', help='base url of site under test', default='http://127.0.0.1:8000')
    # json config
    parser.addoption('--secure', action='store', default='secure.json')
    parser.addoption('--device', action='store', default='')
    parser.addoption('--browser', action='store', default='chromium')
    parser.addini('db_path', help='path to sql db file', default='E:\\Python\\TestMe\\db.sqlite3')
    parser.addini('headless', help='run tests in headless mode', default='False')


def load_config(file):
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(config_file) as cfg:
        return json.loads(cfg.read())
