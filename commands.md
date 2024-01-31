# All commands using project

Frontend

- Run tests:
  - `npx hardhat test`
- Install hardhat to local environment
  - `npm install --save-dev hardhat`
- Create sample project use hardhat
  - `npx hardhat init`
- Fix issue on file
  - `npx eslint --fix .`
- Review issue on file
  - `npm run lint`
- Check formatting for solidity file
  - `npx prettier --check "**/*.sol"`
- Modify formatting issue inside solidity file
  - `npx prettier --write "**/*.sol"`
- Run tests coverage
  - `npx hardhat coverage`

Backend

- Run tests with code coverage:
  - `poetry run coverage run -m pytest`
- Run tests:
  - `poetry run pytest`
- Run tests with coverage:
  - `poetry run pytest --cov`
- Run tests with output capturing disabled:
  - `poetry run pytest -s`
    - Disable output capturing when running tests, allowing the output from tests to be displayed on the console.
- Run specific file:
  - `poetry run pytest -k`
    - Allows you to select a specific file and run only that selected file when executing pytest.
- Run tests until failure:
  - `poetry run pytest -x`
    - Run tests until a failure occurs, then stop the tests when encountering a failed test function.
- Format code using Black:
  - `poetry run black .`
- Check code formatting is needed or not:
  - `poetry run black . --check`
- Sort imports using isort with Black profile:
  - `poetry run isort . --profile black`
- Check code style with Flake8:
  - `poetry run flake8 .`
- Check code bug:
  - `poetry run bandit .`
