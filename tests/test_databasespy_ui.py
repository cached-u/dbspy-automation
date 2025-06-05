import sys
import pytest
from utils.databasespy import launch_database_spy, connect_to_database, connect_to_database_spy
from utils import common_classes as Constants

ControlTypes = Constants.control_types

# Parametrized test 
@pytest.mark.parametrize(
    "conn_type, db_name",
    [
        ("ODBC", "MySQL"),
        ("ODBC", "MySQL")
    ],
)
def test_connection_ui(conn_type, db_name):
    app, main = launch_database_spy()
    connect_to_database(connection_type=conn_type, db_name=db_name)
    wizard = main.child_window(
        title=Constants.ADD_DATA_SOURCE_WINDOW_TITLE,
        control_type=ControlTypes.WINDOW
    )
    #Checks if the connection wizard is gone
    assert not wizard.exists(timeout=10)
    app.kill()