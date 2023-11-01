from abc import abstractmethod
from typing import Any
from urllib.parse import urljoin
from pydantic import BaseModel
from uc_http_requester.requester import Request
from uc_flow_nodes.views import execute
import json as js

class AbstractModel(BaseModel):
    host: str
    office_id: int
    api: str = "v2api"
    path: str
    
    @abstractmethod
    def get_url(self):
        pass
    
    @abstractmethod
    def _get_request_params(self):
        pass
    
    @abstractmethod
    def get_request(self):
        pass
    
class Authorization(AbstractModel):
    email: str
    api_key: str
    path: str = "auth/login"
    
    def get_url(self) -> str:
        base_url = f"https://{self.host}"
        path_url = ("/").join([self.api, self.path])
        return urljoin(base_url, path_url)
    
    def _get_request_params(self)->dict:
        res ={
            "email":self.email,
            "api_key":self.api_key
        }
        return res
    
    def get_request(self)->Request:
        return Request(
                            url=self.get_url(),
                            method=Request.Method.post,
                            json=js.dumps(self._get_request_params()),
                        )
    
class Customer(AbstractModel):
    token: str
    path: str = "customer/index"
    params: dict = {}

    def get_url(self) -> str:
        base_url = f"https://{self.host}"
        path_url = ("/").join([self.api, str(self.office_id), self.path])
        return urljoin(base_url, path_url)
    
    def _get_request_params(self)->dict:
        res: dict = {}
        for value in self.params.values():
            res.update(value[0]) if value else ...
        return res

    
    def get_request(self)->Request:
        params = self._get_request_params()
        return Request(
                            url=self.get_url(),
                            method=Request.Method.post,
                            json=js.dumps(params),
                            headers={"X-ALFACRM-TOKEN":self.token}
                        )
        


