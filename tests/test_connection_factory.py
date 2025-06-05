import pytest
from utils.connection_factory import (
    generate_connection_string,
    get_builder,
    ODBCConnectionStringBuilder,
    JDBCConnectionStringBuilder,
    ADOConnectionStringBuilder,
)


def test_odbc_connection_string_mysql():
    # Test ODBC connection string generation for MySQL (per your config.yaml)
    conn_str = generate_connection_string("ODBC", "MySQL")
    # The driver name comes from driver_maps.odbc in config.yaml
    assert "Driver={MySQL ODBC 9.3 Unicode}" in conn_str
    assert "Server=test-db.vie.altova.com" in conn_str
    assert "Port=3320" in conn_str
    # Note: the builder uses db_name ("MySQL") as the Database= value
    assert "Database=DBDiff" in conn_str
    assert "UID=altova_user" in conn_str
    assert "PWD=user" in conn_str


def test_jdbc_connection_string_mysql():
    # Test JDBC connection string generation for MySQL (per your config.yaml)
    conn_str = generate_connection_string("JDBC", "MySQL")
    # According to the builder, it should be exactly: jdbc:<subprotocol>://<host>:<port>/<db_name>
    expected = "jdbc:mysql://localhost:3306/MySQL"
    assert conn_str == expected


def test_ado_connection_string_mysql():
    # Test ADO connection string generation for MySQL (per your config.yaml)
    conn_str = generate_connection_string("ADO", "MySQL")
    # The provider name comes from driver_maps.ado_provider in config.yaml
    assert "Provider=MySQL Provider" in conn_str
    assert "Data Source=localhost,3306" in conn_str
    # Uses db_name ("MySQL") as the Initial Catalog
    assert "Initial Catalog=MySQL" in conn_str
    assert "User Id=testuser" in conn_str
    assert "Password=testpass" in conn_str


def test_get_builder_types():
    # Ensure get_builder returns the proper builder subclasses
    assert isinstance(get_builder("ODBC"), ODBCConnectionStringBuilder)
    assert isinstance(get_builder("JDBC"), JDBCConnectionStringBuilder)
    assert isinstance(get_builder("ADO"), ADOConnectionStringBuilder)


def test_get_builder_invalid():
    # If an unsupported connection type is requested, we should get a ValueError
    with pytest.raises(ValueError):
        get_builder("INVALID_TYPE")
