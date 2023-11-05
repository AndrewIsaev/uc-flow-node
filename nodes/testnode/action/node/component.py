from uc_flow_nodes.component import Routes as NodeRoutes
from uc_flow_nodes.service import NodeService

from nodes.testnode.action.node.views import execute, info


class Service(NodeService):
    class Routes(NodeRoutes):
        Info = info.InfoView
        Execute = execute.View
