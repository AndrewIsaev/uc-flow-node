import json as js
import time
from abc import abstractmethod
from typing import Any
from urllib.parse import urljoin

import jwt
from pydantic import BaseModel
from uc_flow_nodes.views import execute
from uc_http_requester.requester import Request


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


class Authorization(BaseModel):
    email: str
    url: str = "https://oauth2.googleapis.com/token"
    grant_type: str = "urn:ietf:params:oauth:grant-type:jwt-bearer"
    private_key_id: str
    private_key: str

    def get_url(self) -> str:
        base_url = f"https://{self.host}"
        path_url = ("/").join([self.api, self.path])
        return urljoin(base_url, path_url)

    def get_jwt_token(self):
        iat = time.time()
        exp = iat + 3600
        payload = {
            "iss": self.email,
            "sub": self.email,
            "scope": "https://www.googleapis.com/auth/spreadsheets",
            "aud": "https://accounts.google.com/o/oauth2/token",
            "iat": iat,
            "exp": exp,
        }
        additional_headers = {"kid": self.private_key_id}
        signed_jwt = jwt.encode(
            payload, self.private_key, headers=additional_headers, algorithm="RS256"
        )

        return signed_jwt

    def _get_request_params(self) -> dict:
        a = self.get_jwt_token()
        res = {"grant_type": self.grant_type, "assertion": a}
        return res

    def get_request(self) -> Request:
        return Request(
            url=self.url,
            method=Request.Method.post,
            json=js.dumps(self._get_request_params()),
        )


class Table(BaseModel):
    access_token: str
    title: str
    url: str = "https://sheets.googleapis.com/v4/spreadsheets"

    def get_url(self) -> str:
        base_url = f"https://{self.host}"
        path_url = ("/").join([self.api, str(self.office_id), self.path])
        return urljoin(base_url, path_url)

    def _get_request_params(self) -> dict:
        res = {"properties": {"title": self.title}}
        return res

    def create_table(self) -> Request:
        params = self._get_request_params()
        return Request(
            url=self.url,
            method=Request.Method.post,
            json=js.dumps(params),
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
