from enum import Enum


class Action(str, Enum):
    authorization = "authorization"
    g_sheets = "g_sheets"


class Operation(str, Enum):
    create_table = "create_table"
    add_sheet = "add_sheet"
    write_to_cell = "write_to_cell"
    get_cell_value = "get_cell_value"
