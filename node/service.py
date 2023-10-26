import ujson
from typing import List, Tuple

from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.service import NodeService
from uc_flow_nodes.views import info, execute
from uc_flow_schemas import flow
from uc_flow_schemas.flow import Property, CredentialProtocol, RunState
from uc_http_requester.requester import Request


class NodeType(flow.NodeType):
    id: str = '1257d121-5853-4844-8d23-99685ecaede7'
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = 'test_name'
    displayName: str = 'TestNode'
    icon: str = '<svg><text x="8" y="50" font-size="50">🤖</text></svg>'
    description: str = 'test description'
    properties: List[Property] = [
        Property(
            displayName='Текстовое поле',
            name='str_field',
            type=Property.Type.STRING,
            placeholder='Foo placeholder',
            description='Текстовое поле',
            required=True,
            default='Test data',
        ),
        Property(
            displayName='Числовое поле',
            name='int_field',
            type=Property.Type.NUMBER,
            placeholder='Foo placeholder',
            description='Числовое поле',
            required=True,
            default='Test data',
        ),
        Property(
            displayName='Число/Текст',
            name='is_return_str',
            type=Property.Type.BOOLEAN,
            placeholder='Foo placeholder',
            description='Выбор число или строка',
            required=True,
            default=True,
        )  
    ]


class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            int_str_field = int(json.node.data.properties['str_field'])
            result = json.node.data.properties['int_field']+int_str_field
            is_return_str = json.node.data.properties['is_return_str']
            await json.save_result({
                "result": result if not is_return_str else str(result)
            })
            json.state = RunState.complete
        except ValueError as e:
            self.log.warning(f'Error {e}')
            await json.save_error("Field must be numeric")
            json.state = RunState.error
        except Exception as e:
            self.log.warning(f'Error {e}')
            await json.save_error(str(e))
            json.state = RunState.error
        return json


class Service(NodeService):
    class Routes(NodeService.Routes):
        Info = InfoView
        Execute = ExecuteView
