from uc_flow_nodes.component import NodeComponent, Routes as NodeRoutes
from nodes.testnode.action.node.views import info, execute
from uc_flow_nodes.service import NodeService


class Service(NodeService):
    class Routes(NodeRoutes):
        Info = info.InfoView
        Execute = execute.View
