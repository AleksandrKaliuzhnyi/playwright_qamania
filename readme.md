#Project
about...

## Install guide

## Allure report
allure serve .\report\ --port 3060


## Pytest
pytest -m smoke
pytest -m smoke --maxfail=1
pytest -n smoke -n 2 - run tests in several treads