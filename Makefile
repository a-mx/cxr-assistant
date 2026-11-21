.PHONY: run
VENV=.venv
PYTHON=$(VENV)\Scripts\python.exe
FLASK=$(PYTHON) -m flask --app "src.app:create_app(load_models=False)"

run:
	$(PYTHON) -m run

init: migrate-init migrate

migrate: migrate-create migrate-up

migrate-init:
	$(FLASK) db init

migrate-create:
	$(FLASK) db migrate -m "$(or $(MSG),auto migration)"

migrate-up:
	$(FLASK) db upgrade