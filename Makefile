include .env
export $(shell sed 's/=.*//' .env)

MIGRATIONS_DIR = ./src/migrations

help:
	@echo "run – запустить приложение полностью"
	@echo "debug – поднять все зависимости, но не запускать executable – их вы можете запустить сами через IDE, терминал и т.д. – при таком запуске можно дебажиться"
	@echo "migrate – применить к базе данных миграции из папки /src/migrations"
	@echo "dump – вручную экспортировать базу данных. Необходимо казать путь к файлу экспорта: make dump file=/path/to/file/file.sql"
	@echo "load_dumped – вручную импортировать базу данных. Необходимо казать путь к файлу импорта: make load_dumped file=/path/to/file/file.sqli"

debug:
	docker compose up -d db

run:
	docker compose up -d db && docker compose up -d bot --build

down:
	docker compose down db bot

migrate:
	    @for sql_file in $$(ls -v $(MIGRATIONS_DIR)/*.sql); do \
        psql -U $(POSTGRES_USER) -d $(POSTGRES_DATABASE) -h localhost -p $(POSTGRES_PORT) -f $$sql_file; \
		done

dump:
	pg_dump -U $(POSTGRES_USER) -h localhost -p $(POSTGRES_PORT) -d $(POSTGRES_DATABASE) > $(file)

load_dumped:
	psql -U $(POSTGRES_USER) -h localhost -p $(POSTGRES_PORT) -d $(POSTGRES_DATABASE) -f $(file)
