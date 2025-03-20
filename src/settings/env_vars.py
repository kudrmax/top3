from enum import Enum


class PostgresEnvVarsNames(str, Enum):
    run_with_docker = 'RUN_WITH_DOCKER'
    user = 'POSTGRES_USER'
    password = 'POSTGRES_PASSWORD'
    database = 'POSTGRES_DATABASE'
    port = 'POSTGRES_PORT'