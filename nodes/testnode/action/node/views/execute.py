from enum import Enum
from typing import Any, List



from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.views import execute

from uc_flow_schemas.flow import RunState
from uc_http_requester.requester import Request, Response
from nodes.testnode.action.node.provider.testnode import Authorization, Sheet, Table, Value

from nodes.testnode.action.node.schemas.enums import Action, Operation


class View(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            action = json.node.data.properties["action"]
            match action:
                case Action.authorization:
                    auth: Authorization = Authorization(
                        private_key_id=json.node.data.properties["auth_data"]["private_key_id"],
                        private_key=json.node.data.properties["auth_data"]["private_key"],
                        email=json.node.data.properties["auth_data"]["client_email"],
                    )

                    data: Request = auth.get_request()
                    result: Response = await data.execute()

                    token:str = result.json().get("access_token")
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
                            table_name:str = json.node.data.properties["table_name"]
                            access_token:str = json.node.data.properties["access_token"]
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
                            
                        case Operation.add_sheet:
                            spreadsheet_id:str = json.node.data.properties["spreadsheet_id"]
                            sheet_name:str = json.node.data.properties["sheet_name"]
                            access_token = json.node.data.properties["access_token"]
                            
                            sheet = Sheet(
                                access_token=access_token,
                                table_id=spreadsheet_id,
                                sheet_name=sheet_name,
                            )
                            
                            data = sheet.create_sheet()
                            result = await data.execute()
                            
                            await json.save_result(
                                {
                                    "result": result.json(),
                                }
                            )
                            json.state = RunState.complete
                        case Operation.get_cell_value:
                            params:dict[str, Any] = {
                            "table_id": json.node.data.properties["spreadsheet_id"],
                            "sheet_name": json.node.data.properties["sheet_name"],
                            "access_token":json.node.data.properties["access_token"],
                            "range":json.node.data.properties["range"],
                            }
                            value:Value = Value(
                                **params
                            )
                            data = value.get_values()
                            result = await data.execute()
                            
                            await json.save_result(
                                {
                                    "result": result.json(),
                                }
                            )
                            json.state = RunState.complete
                            
                        case Operation.write_to_cell:
                            params:dict[str, Any] = {
                            "table_id": json.node.data.properties["spreadsheet_id"],
                            "sheet_name": json.node.data.properties["sheet_name"],
                            "access_token":json.node.data.properties["access_token"],
                            "range":json.node.data.properties["range"],
                            "value":json.node.data.properties["user_value"]
                            }
                            value:Value = Value(
                                **params
                            )
                            data = value.add_values()
                            result = await data.execute()
                            
                            await json.save_result(
                                {
                                    "result": result.json(),
                                }
                            )
                            json.state = RunState.complete
                            
        except Exception as e:
            self.log.warning(f"Error {e}")
            await json.save_error(str(e))
            json.state = RunState.error
        return json
