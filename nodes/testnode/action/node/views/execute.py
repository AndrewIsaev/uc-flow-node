from enum import Enum
from typing import List
import json as js

import ujson
from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.views import execute

from uc_flow_schemas.flow import RunState
from uc_http_requester.requester import Request
from nodes.testnode.action.node.provider.testnode import Authorization, Table

from nodes.testnode.action.node.schemas.enums import Action, Operation


class View(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            action = json.node.data.properties["action"]
            match action:
                case Action.authorization:
                    auth: Authorization = Authorization(
                        # url=json.node.data.properties["auth_data"]["auth_uri"],
                        private_key_id=json.node.data.properties["auth_data"]["private_key_id"],
                        private_key=json.node.data.properties["auth_data"]["private_key"],
                        email=json.node.data.properties["auth_data"]["client_email"],
                    )

                    data = auth.get_request()
                    result = await data.execute()

                    token = result.json().get("access_token")
                    await json.save_result({
                        "result": {
                            "access_token": token,
                        }
                    })
                    json.state = RunState.complete
                case Action.g_sheets:
                    api_action = json.node.data.properties["g_sheet_action"]
                    match api_action:
                        case Operation.create_table:
                            table_name = json.node.data.properties["table_name"]
                            access_token = json.node.data.properties["access_token"]
                            table: Table = Table(
                                access_token=access_token,
                                title=table_name,
                            )

                    data = table.create_table()
                    result = await data.execute()

                    await json.save_result(
                        {
                            "result": {
                                "spreadsheetId": result.json().get("spreadsheetId"),
                                    }
                        }
                    )
                    json.state = RunState.complete
        except Exception as e:
            self.log.warning(f"Error {e}")
            await json.save_error(str(e))
            json.state = RunState.error
        return json
