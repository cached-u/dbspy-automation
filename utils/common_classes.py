# === Application Window Titles ===
APP_TITLE_RE = r".*Altova DatabaseSpy.*"

# === “Add a Data Source” Dialog ===
ADD_DATA_SOURCE_WINDOW_TITLE = "Add a Data Source"
ADD_DATA_SOURCE_CLOSE_BUTTON_TITLE = "Close"
ADD_DATA_SOURCE_CLOSE_BUTTON_AUTO_ID = "2"

# === Menu Bar ===
MENU_BAR_PANE_TITLE = "Menu Bar"
MENU_BAR_PANE_AUTO_ID = "59398"

# === “File” Menu ===
FILE_MENU_ITEM_TITLE = "File"
FILE_MENU_WINDOW_TITLE = "File"
FILE_TOOLBAR_AUTO_ID = "1"

# === “New” Submenu under File ===
NEW_MENU_ITEM_TITLE = "New"
NEW_POPUP_WINDOW_TITLE = "New"
NEW_TOOLBAR_AUTO_ID = "1"
NEW_PROJECT_MENU_ITEM_TITLE = "New Project\tStrg+Umschalt+N"

# === “Create a Database Connection…” Menu Item ===
CONNECTION_WIZARD_WINDOW_NAME = "Create a Database Connection...\tStrg+Q"

# === Mapped Errors ===
class errors:
    APP_LAUNCH_ERROR = "Error launching the application"
    APP_CONNECT_ERROR = "Error connecting to the application"
    TIMEOUT = "TimeoutError"
    ELEMENT_NOT_FOUND = "Could not find element"

# === Control Types ===
class control_types:
    WINDOW = "Window"
    BUTTON = "Button"
    PANE = "Pane"
    MENU = "Menu"
    MENU_ITEM = "MenuItem"
    TOOLBAR = "ToolBar"
    TEXT = "Text"
    EDIT = "Edit"

# === DB Connection Types ===
class connection_types:
    TEST = "TEST"
    JDBC = "JDBC"
    ODBC = "ODBC"
    ADO = "ADO"
    NATIVE = "NATIVE"

class connection_types_map:
    MAP = {
        "TEST": "ODBC Connections",
        "ODBC": "ODBC Connections",
        "JDBC": "JDBC Connections",
        "ADO": "ADO Connections"
    }