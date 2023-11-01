from enum import Enum
from typing import List
import json as js

import ujson
from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.views import execute

from uc_flow_schemas.flow import RunState
from uc_http_requester.requester import Request
from nodes.testnode.action.node.provider.testnode import Authorization, Customer

from nodes.testnode.action.node.schemas.enums import Action


class View(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            action = json.node.data.properties["action"]
            match action:
                case Action.authorization:
                    # url = f"https://{crm_host}/v2api/auth/login"
                    auth: Authorization = Authorization(
                        host=json.node.data.properties["crm_host"],
                        email=json.node.data.properties["email"],
                        api_key=json.node.data.properties["api_key"],
                        office_id=json.node.data.properties["office_id"]
                    )

                    data = auth.get_request()
                    result = await data.execute()

                    token = result.json().get("token")
                    await json.save_result({
                        "result": {
                            "token": token,
                            "host": auth.host,
                            "office_id": auth.office_id
                        }
                    })
                    json.state = RunState.complete
                case Action.api:

                    auth_data = json.node.data.properties["auth_data"]
                    filters = json.node.data.properties["parameters"]

                    customer: Customer = Customer(
                        **auth_data,
                        params=filters,
                    )

                    data = customer.get_request()
                    result = await data.execute()

                    await json.save_result({
                        "result": result.json(),
                    })
                    json.state = RunState.complete
        except Exception as e:
            self.log.warning(f"Error {e}")
            await json.save_error(str(e))
            json.state = RunState.error
        return json
