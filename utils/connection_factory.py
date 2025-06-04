from typing import Dict
from utils.config import Config

class ConnectionStringBuilder:
    def build(self, db_name: str, db_version: str) -> str:
        raise NotImplementedError()

class ODBCConnectionStringBuilder(ConnectionStringBuilder):
    def build(self, db_name: str, db_version: str) -> str:
        db_conf = Config.get_database_config(db_name)
        host = db_conf.get("host", "localhost")
        port = db_conf.get("port", None) or 5432
        user = db_conf.get("user", "")
        password = db_conf.get("password", "")
        driver_map = Config.get_driver_map()
        driver = driver_map.get(db_name)

        return (
            f"Driver={{{driver}}};"
            f"Server={host};Port={port};"
            f"Database={db_name};"
            f"UID={user};PWD={password};"
        )

class JDBCConnectionStringBuilder(ConnectionStringBuilder):
    def build(self, db_name: str, db_version: str) -> str:
        db_conf = Config.get_database_config(db_name)
        host = db_conf.get("host", "localhost")
        port = db_conf.get("port", None) or 5432
        subprotocol_map = Config.get_jdbc_subprotocol_map()
        subprotocol = subprotocol_map.get(db_name)

        return f"jdbc:{subprotocol}://{host}:{port}/{db_name}"

class ADOConnectionStringBuilder(ConnectionStringBuilder):
    def build(self, db_name: str, db_version: str) -> str:
        db_conf = Config.get_database_config(db_name)
        host = db_conf.get("host", "localhost")
        port = db_conf.get("port", None) or 1433
        user = db_conf.get("user", "")
        password = db_conf.get("password", "")
        provider_map = Config.get_ado_provider_map()
        provider = provider_map.get(db_name)

        return (
            f"Provider={provider};"
            f"Data Source={host},{port};"
            f"Initial Catalog={db_name};"
            f"User Id={user};Password={password};"
        )

_BUILDER_REGISTRY: Dict[str, ConnectionStringBuilder] = {
    "ODBC": ODBCConnectionStringBuilder(),
    "JDBC": JDBCConnectionStringBuilder(),
    "ADO": ADOConnectionStringBuilder(),
}

def get_builder(connection_type: str) -> ConnectionStringBuilder:
    key = connection_type.upper()
    if key not in _BUILDER_REGISTRY:
        raise ValueError(f"Unsupported connection type: {connection_type}")
    return _BUILDER_REGISTRY[key]

def generate_connection_string(connection_type: str, db_name: str, db_version: str = "") -> str:
    builder = get_builder(connection_type)
    return builder.build(db_name, db_version)
