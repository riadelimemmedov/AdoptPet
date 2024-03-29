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
- Run specific file:
  - `poetry run pytest -k`
- Run tests until failure:
  - `poetry run pytest -x`
- Run tests paralel:
  - `poetry run pytest -n auto`
- Format code using Black:
  - `poetry run black .`
- Generate html for covering tests:
  - `poetry run pytest --cov=./ --cov-report=html`
- Check code formatting is needed or not:
  - `poetry run black . --check`
- Sor t imports using isort with Black profile:
  - `poetry run isort . --profile black`
- Check code style with Flake8:
  - `poetry run flake8 .`
- Check code bug:
  - `poetry run bandit .`
- Run all the tests in the apps.users.tests module:
  - `poetry run manage.py test apps.users.tests`
- Run all the tests found within the 'apps' package:
  - `poetry run manage.py test apps`
- Run just one test case class:
  - `poetry run manage.py test apps.users.tests.UsersManagersTests`
- Run just one test method:
  - `poetry run manage.py test apps.users.tests.UsersManagersTests.test_create_user`
- Return migration data without creating the migration file,like mock migration file.Migration not affect to database:
- `poetry run manage.py makemigrations --dry-run --verbosity 3`
- Run pre commit hooks
- `poetry run pre-commit run --all-files`
- Generate api schema
- `poetry run manage.py spectacular --file schema.yml`
- Configure waitress
- `poetry run waitress-serve --listen=*:8000 config.wsgi:application`
- Stress test using Apache Benchmark
- `ab -n 400 -c 10 http://127.0.0.1:8000/pets/`
