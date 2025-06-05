# utils/databasespy.py

from pywinauto.application import Application
from utils import connection_factory as ConnectionFactory
from utils import common_classes as Constants
from utils.config import Config

ControlTypes = Constants.control_types
ConnectionTypes = Constants.connection_types
CommonErrors = Constants.errors
connection_type_map = Constants.connection_types_map.MAP

# TODO add error handling


def launch_database_spy():
    """
    Launches DatabaseSpy and returns (app, main_window).
    Reads exe_path and timeout from config.yaml.
    """
    exe_path = Config.get_global("exe_path")
    launch_timeout = Config.get_global("launch_timeout", 15)
    visible_timeout = Config.get_global("visible_timeout", 5)
    try:
        app = Application(backend="uia").start(
            exe_path, timeout=launch_timeout)
        main_window = app.window(title_re=Constants.APP_TITLE_RE)
        main_window.wait("visible", timeout=visible_timeout)
        return app, main_window
    except Exception as e:
        print(e)
        raise e


def connect_to_database_spy():
    """
    Attempts to attach to a running Altova DatabaseSpy window.
    Returns (app, main_window) if successful, or (None, None) otherwise.
    """
    connection_timeout = Config.get_global("connection_timeout", 5)
    try:
        app = Application(backend="uia").connect(
            title_re=Constants.APP_TITLE_RE, timeout=connection_timeout
        )
        main_window = app.window(title_re=Constants.APP_TITLE_RE)
        main_window.wait("visible", timeout=connection_timeout)
        return app, main_window
    except Exception as e:
        print(e)
        return None, None


def close_connection_wizard(main_window):
    """
    Closes the connection wizard.
    Reads timeout from config.yaml.
    """
    visible_timeout = Config.get_global("visible_timeout", 5)
    try:
        dlg = main_window.child_window(
            title=Constants.ADD_DATA_SOURCE_WINDOW_TITLE,
            control_type=ControlTypes.WINDOW
        )
        dlg.wait("visible", timeout=visible_timeout)
        close_btn = dlg.child_window(
            title=Constants.ADD_DATA_SOURCE_CLOSE_BUTTON_TITLE,
            auto_id=Constants.ADD_DATA_SOURCE_CLOSE_BUTTON_AUTO_ID,
            control_type=ControlTypes.BUTTON
        )
        close_btn.wait("visible", timeout=visible_timeout)
        close_btn.click_input()
    except Exception as e:
        print(e)
        pass


def open_new_project():
    """
    Ensures a DatabaseSpy instance is running (attaches if already open,
    launches otherwise), then opens a new project.
    Reads exe_path and timeout from config.yaml if not provided.
    """
    visible_timeout = Config.get_global("visible_timeout", 5)

    app, main_window = connect_to_database_spy()
    if main_window is None:
        app, main_window = launch_database_spy()

    main_window.set_focus()

    close_connection_wizard(main_window)

    # Click 'File' in the menu bar
    menu_bar = main_window.child_window(
        title=Constants.MENU_BAR_PANE_TITLE,
        auto_id=Constants.MENU_BAR_PANE_AUTO_ID,
        control_type=ControlTypes.PANE
    )
    file_item = menu_bar.child_window(
        title=Constants.FILE_MENU_ITEM_TITLE,
        control_type=ControlTypes.MENU_ITEM
    )
    file_item.wait("visible", timeout=visible_timeout)
    file_item.click_input()

    # Wait for File menu popup
    file_popup = main_window.child_window(
        title="File", control_type=ControlTypes.MENU
    )
    file_popup.wait("visible", timeout=visible_timeout)
    file_popup.set_focus()

    # Click 'New'
    file_toolbar = file_popup.child_window(
        auto_id="1", control_type=ControlTypes.TOOLBAR
    )
    new_item = file_toolbar.child_window(
        title="New", control_type=ControlTypes.MENU_ITEM
    )
    new_item.wait("visible", timeout=visible_timeout)
    new_item.click_input()

    # Wait for New submenu
    new_popup = main_window.child_window(
        title="New", control_type=ControlTypes.MENU
    )
    new_popup.wait("visible", timeout=visible_timeout)

    # Click 'New Project'
    new_toolbar = new_popup.child_window(
        auto_id="1", control_type=ControlTypes.TOOLBAR
    )
    new_project_item = new_toolbar.child_window(
        title="New Project\tStrg+Umschalt+N",
        control_type=ControlTypes.MENU_ITEM
    )
    new_project_item.wait("visible", timeout=visible_timeout)
    new_project_item.click_input()

    print("opened a new project")


def open_connection_wizard():
    """
    Ensures a DatabaseSpy instance is running (attaches if already open,
    launches otherwise), then opens the connection wizard.
    """
    visible_timeout = Config.get_global("visible_timeout", 15)
    try:
        app, main_window = connect_to_database_spy()
        if main_window is None:
            app, main_window = launch_database_spy()

        main_window.set_focus()

        close_connection_wizard(main_window)

        # Click 'File' in the menu bar
        menu_bar = main_window.child_window(
            title="Menu Bar", auto_id="59398", control_type=ControlTypes.PANE
        )
        file_item = menu_bar.child_window(
            title="File", control_type=ControlTypes.MENU_ITEM
        )
        file_item.wait("visible", timeout=visible_timeout)
        file_item.click_input()

        file_popup = main_window.child_window(
            title="File", control_type=ControlTypes.MENU
        )
        file_popup.wait("visible", timeout=visible_timeout)
        file_popup.set_focus()

        # Opens connection wizard
        file_toolbar = file_popup.child_window(
            auto_id="1", control_type=ControlTypes.TOOLBAR
        )
        conn_item = file_toolbar.child_window(
            title=Constants.CONNECTION_WIZARD_WINDOW_NAME,
            control_type=ControlTypes.MENU_ITEM
        )
        conn_item.wait("visible", timeout=visible_timeout)
        conn_item.click_input()

        connection_wizard = main_window.child_window(
            title=Constants.ADD_DATA_SOURCE_WINDOW_TITLE,
            control_type=ControlTypes.WINDOW
        )

        print("Opened connection wizard.")

        return main_window, connection_wizard
    except Exception as e:
        print(e)
        raise e


def connect_to_database(
    connection_type="ODBC",
    db_name="MySQL",
    db_version=""
):
    """
    Ensures a DatabaseSpy instance is running (attaches if already open,
    launches otherwise), then opens the connection wizard and connects to the specified db.
    Reads timeout from config.yaml if not provided.
    """
    visible_timeout = Config.get_global("visible_timeout", 5)

    main_window, connection_wizard = open_connection_wizard()

    # Select the right connection given the connection_type
    connection_toolbar = connection_wizard.child_window(
        auto_id="1163", control_type=ControlTypes.TOOLBAR
    )
    selected_connection_window = connection_toolbar.child_window(
        title=connection_type_map[connection_type],
        control_type=ControlTypes.BUTTON
    )
    selected_connection_window.wait("visible", timeout=visible_timeout)
    selected_connection_window.click_input()

    # Generate connection string given connection_type, db_name and db_version
    connection_string = ConnectionFactory.generate_connection_string(
        connection_type=connection_type,
        db_name=db_name,
        db_version=db_version
    )

    # Select "build a connection string" and paste generated connection string
    connection_text_field = connection_wizard.child_window(
        auto_id="1286", control_type=ControlTypes.EDIT
    )
    connect_button = connection_wizard.child_window(
        title="Connect", auto_id="1613", control_type=ControlTypes.BUTTON
    )
    connection_text_field.click_input()
    connection_text_field.set_text(connection_string)
    connect_button.click_input()

    # Verify success and eventually throw error


# def generate_connection_string(connection_type, db_name, db_version):
#     """
#     Generates a connection string given type (ODBC, JDBC ecc...), name (MariaDB, PostgreSQL ecc..) and version
#     """
#     try:
#         print('connection string generation')
#         # connection_factory
#         default_connection_string = "TEST CONNECTION STRING"
#         return default_connection_string

#     except Exception as e:
#         raise e
