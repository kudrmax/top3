import os
from typing import Tuple, Any

from pydantic import PostgresDsn

from src.settings.env_vars import PostgresEnvVarsNames


class PostgresConnection:
    docker_host = 'db'
    docker_port = 5432
    not_docker_host = 'localhost'

    def get_url(self):
        return str(PostgresDsn.build(
            scheme="postgresql",
            username=self._get_username(),
            password=self._get_password(),
            host=self._get_host(),
            port=self._get_port(),
            path=self._get_database(),
        ))

    def _get_username(self) -> str:
        return self.__get_env_var(PostgresEnvVarsNames.user)

    def _get_password(self) -> str:
        return self.__get_env_var(PostgresEnvVarsNames.password)

    def _get_database(self) -> str:
        return self.__get_env_var(PostgresEnvVarsNames.database)

    def _get_host(self) -> str:
        host, _ = self.__get_host_and_port()
        return host

    def _get_port(self) -> int:
        _, port = self.__get_host_and_port()
        return port

    def __get_host_and_port(self) -> Tuple[str, int]:
        if bool(os.getenv(PostgresEnvVarsNames.run_with_docker)):
            return self.docker_host, self.docker_port
        return self.not_docker_host, int(self.__get_env_var(PostgresEnvVarsNames.port))

    @staticmethod
    def __get_env_var(env_var_name: str) -> Any:
        return os.getenv(env_var_name)
