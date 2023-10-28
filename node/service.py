from enum import Enum
from typing import List

import ujson
from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.service import NodeService
from uc_flow_nodes.views import execute, info
from uc_flow_schemas import flow
from uc_flow_schemas.flow import Defaults, DisplayOptions
from uc_flow_schemas.flow import NodeType as BaseNodeType
from uc_flow_schemas.flow import OptionValue, Property, RunState
from uc_http_requester.requester import Request


class Value(str, Enum):
    value_1 = "value_1"
    value_2 = "value_2"


class NodeType(flow.NodeType):
    id: str = "3a13c9d3-13f8-4a14-8607-4d633014448b"
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = "test_name"
    displayName: str = "TestNode"
    icon: str = '<svg><text x="8" y="50" font-size="50">🤖</text></svg>'
    description: str = "test description"
    properties: List[Property] = [
        Property(
            displayName="Текстовое поле",
            name="str_field",
            type=Property.Type.STRING,
            placeholder="Foo placeholder",
            description="Текстовое поле",
            required=True,
            default="Test data",
        ),
        Property(
            displayName="Числовое поле",
            name="int_field",
            type=Property.Type.NUMBER,
            placeholder="Foo placeholder",
            description="Числовое поле",
            required=True,
            default="Test data",
        ),
        Property(
            displayName="Число/Текст",
            name="is_return_str",
            type=Property.Type.BOOLEAN,
            placeholder="Foo placeholder",
            description="Выбор число или строка",
            required=True,
            default=True,
        ),
        Property(
            displayName="Переключатель",
            name="switcher",
            type=Property.Type.BOOLEAN,
            placeholder="switcher",
            description="switcher",
            required=True,
            default=False,
        ),
        Property(
            displayName="Значение 1",
            name="field_1",
            type=Property.Type.OPTIONS,
            noDataExpression=True,
            options=[
                OptionValue(
                    name="Значение 1",
                    value=Value.value_1,
                    description="",
                ),
                OptionValue(
                    name="Значение 2",
                    value=Value.value_2,
                    description="",
                ),
            ],
            displayOptions=DisplayOptions(
                show={
                    "switcher": [
                        True,
                    ],
                },
            ),
        ),
        Property(
            displayName="Значение 2",
            name="field_2",
            type=Property.Type.OPTIONS,
            noDataExpression=True,
            options=[
                OptionValue(
                    name="Значение 1",
                    value=Value.value_1,
                    description="",
                ),
                OptionValue(
                    name="Значение 2",
                    value=Value.value_2,
                    description="",
                ),
            ],
            displayOptions=DisplayOptions(
                show={
                    "switcher": [
                        True,
                    ],
                },
            ),
        ),
        Property(
            displayName="Поле для ввода почты",
            name="email_field",
            type=Property.Type.EMAIL,
            placeholder="email_field",
            description="Поле для ввода почты",
            required=True,
            displayOptions=DisplayOptions(
                show={
                    "switcher": [
                        True,
                    ],
                    "field_1": [
                        Value.value_1,
                    ],
                    "field_2": [
                        Value.value_1,
                    ],
                },
            ),
        ),
        Property(
            displayName="Поле для ввода даты и время",
            name="date_field",
            type=Property.Type.DATETIME,
            placeholder="date_field",
            description="Поле для ввода даты и время",
            required=True,
            displayOptions=DisplayOptions(
                show={
                    "switcher": [
                        True,
                    ],
                    "field_1": [
                        Value.value_2,
                    ],
                    "field_2": [
                        Value.value_2,
                    ],
                },
            ),
        ),
    ]


class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            int_str_field = int(json.node.data.properties["str_field"])
            result = json.node.data.properties["int_field"] + int_str_field
            is_return_str = json.node.data.properties["is_return_str"]
            await json.save_result(
                {"result": result if not is_return_str else str(result)}
            )
            json.state = RunState.complete
        except ValueError as e:
            self.log.warning(f"Error {e}")
            await json.save_error("Field must be numeric")
            json.state = RunState.error
        except Exception as e:
            self.log.warning(f"Error {e}")
            await json.save_error(str(e))
            json.state = RunState.error
        return json


class Service(NodeService):
    class Routes(NodeService.Routes):
        Info = InfoView
        Execute = ExecuteView
