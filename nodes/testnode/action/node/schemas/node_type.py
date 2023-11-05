from typing import List

from uc_flow_schemas import flow
from uc_flow_schemas.flow import DisplayOptions, OptionValue, Property

from nodes.testnode.action.node.schemas.enums import Action, Operation


class NodeType(flow.NodeType):
    id: str = "d1f7c623-0da3-4283-b242-df7217de2bcb"
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = "g_sheet"
    displayName: str = "GoogleSheetNode"
    icon: str = '<svg><text x="8" y="50" font-size="50">🤖</text></svg>'
    description: str = "test description"
    properties: List[Property] = [
        Property(
            displayName="Выберите действие",
            name="action",
            type=Property.Type.OPTIONS,
            noDataExpression=True,
            options=[
                OptionValue(
                    name="Авторизация",
                    value=Action.authorization,
                    description="Авторизация",
                ),
                OptionValue(
                    name="Google Sheets",
                    value=Action.g_sheets,
                    description="Google Sheets API",
                ),
            ],
        ),
        Property(
            displayName="Auth Data",
            name="auth_data",
            type=Property.Type.JSON,
            noDataExpression=True,
            displayOptions=DisplayOptions(
                show={
                    "action": [
                        Action.authorization,
                    ],
                },
            ),
        ),
        Property(
            displayName="Google Sheets actions",
            name="g_sheet_action",
            type=Property.Type.OPTIONS,
            noDataExpression=True,
            displayOptions=DisplayOptions(
                show={
                    "action": [
                        Action.g_sheets,
                    ],
                },
            ),
            options=[
                OptionValue(
                    name="Create table",
                    value=Operation.create_table,
                    description="Create table",
                ),
                OptionValue(
                    name="Add sheet to table",
                    value=Operation.add_sheet,
                    description="Add sheet to table",
                ),
                OptionValue(
                    name="Write to cell",
                    value=Operation.write_to_cell,
                    description="Write to cell",
                ),
                OptionValue(
                    name="Get cell value",
                    value=Operation.get_cell_value,
                    description="Get cell value",
                ),
            ],
        ),
        Property(
            displayName="Access token",
            name="access_token",
            type=Property.Type.STRING,
            noDataExpression=True,
            displayOptions=DisplayOptions(
                show={
                    "action": [
                        Action.g_sheets,
                    ],
                },
            ),
        ),
        Property(
            displayName="Table Name",
            name="table_name",
            type=Property.Type.STRING,
            noDataExpression=True,
            displayOptions=DisplayOptions(
                show={
                    "action": [
                        Action.g_sheets,
                    ],
                    "g_sheet_action": [
                        Operation.create_table,
                    ],
                },
            ),
        ),
        Property(
            displayName="Spreadsheet Id",
            name="spreadsheet_id",
            type=Property.Type.STRING,
            noDataExpression=True,
            displayOptions=DisplayOptions(
                show={
                    "action": [
                        Action.g_sheets,
                    ],
                    "g_sheet_action": [
                        Operation.add_sheet,
                        Operation.get_cell_value,
                        Operation.write_to_cell,
                    ],
                },
            ),
        ),
        Property(
            displayName="Sheet name",
            name="sheet_name",
            type=Property.Type.STRING,
            noDataExpression=True,
            displayOptions=DisplayOptions(
                show={
                    "action": [
                        Action.g_sheets,
                    ],
                    "g_sheet_action": [
                        Operation.add_sheet,
                        Operation.get_cell_value,
                        Operation.write_to_cell,
                    ],
                },
            ),
        ),
        Property(
            displayName="Range",
            name="range",
            type=Property.Type.STRING,
            noDataExpression=True,
            displayOptions=DisplayOptions(
                show={
                    "action": [
                        Action.g_sheets,
                    ],
                    "g_sheet_action": [
                        Operation.get_cell_value,
                        Operation.write_to_cell,
                    ],
                },
            ),
        ),
        Property(
            displayName="Value",
            name="user_value",
            type=Property.Type.JSON,
            noDataExpression=True,
            displayOptions=DisplayOptions(
                show={
                    "action": [
                        Action.g_sheets,
                    ],
                    "g_sheet_action": [
                        Operation.write_to_cell,
                    ],
                },
            ),
        ),
    ]
