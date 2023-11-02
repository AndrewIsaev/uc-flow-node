from typing import List

from uc_flow_schemas import flow
from uc_flow_schemas.flow import Defaults, DisplayOptions
from uc_flow_schemas.flow import NodeType as BaseNodeType
from uc_flow_schemas.flow import OptionValue, Property

from nodes.testnode.action.node.schemas.enums import (
    Action,
    Operation,
    Parameters,
    Resource,
)


class NodeType(flow.NodeType):
    id: str = "75f37521-7c4d-4acc-90bd-bd3ac3883096"
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
                # OptionValue(
                #     name="Write to cell",
                #     value=Operation.write_to_cell,
                #     description="Write to cell",
                # ),
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
    ]
