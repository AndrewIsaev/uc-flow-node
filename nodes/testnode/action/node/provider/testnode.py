import json as js
import time
from typing import Any
from urllib.parse import urljoin

import jwt
from pydantic import BaseModel
from uc_http_requester.requester import Request

BASE_URL: str = "https://sheets.googleapis.com/v4/spreadsheets"


class Authorization(BaseModel):
    email: str
    url: str = "https://oauth2.googleapis.com/token"
    grant_type: str = "urn:ietf:params:oauth:grant-type:jwt-bearer"
    private_key_id: str
    private_key: str

    def get_url(self) -> str:
        base_url: str = f"https://{self.host}"
        path_url: str = "/".join([self.api, self.path])
        return urljoin(base_url, path_url)

    def get_jwt_token(self):
        iat: float = time.time()
        exp: float = iat + 3600
        payload: dict[str, Any] = {
            "iss": self.email,
            "sub": self.email,
            "scope": "https://www.googleapis.com/auth/spreadsheets",
            "aud": "https://accounts.google.com/o/oauth2/token",
            "iat": iat,
            "exp": exp,
        }
        additional_headers: dict[str, str] = {"kid": self.private_key_id}
        signed_jwt: str = jwt.encode(
            payload, self.private_key, headers=additional_headers, algorithm="RS256"
        )

        return signed_jwt

    def _get_request_params(self) -> dict:
        a: str = self.get_jwt_token()
        res: dict[str, str] = {"grant_type": self.grant_type, "assertion": a}
        return res

    def get_request(self) -> Request:
        return Request(
            url=self.url,
            method=Request.Method.post,
            json=js.dumps(self._get_request_params()),
        )


class Table(BaseModel):
    access_token: str
    sheet_name: str

    def _get_request_params(self) -> dict:
        res: dict[str, dict[str, str]] = {"properties": {"title": self.sheet_name}}
        return res

    def create_table(self) -> Request:
        params: dict = self._get_request_params()
        return Request(
            url=BASE_URL,
            method=Request.Method.post,
            json=js.dumps(params),
            headers={"Authorization": f"Bearer {self.access_token}"},
        )


class Sheet(BaseModel):
    access_token: str
    table_id: str
    sheet_name: str
    query_params: str = "batchUpdate"

    def get_url(self) -> str:
        base_url: str = ("/").join([BASE_URL, self.table_id])
        return (":").join([base_url, self.query_params])

    def _get_request_params(self) -> dict:
        res: dict[str, list[dict[str, dict[str, dict[str, str]]]]] = {
            "requests": [{"addSheet": {"properties": {"title": self.sheet_name}}}]
        }
        return res

    def create_sheet(self) -> Request:
        params: dict = self._get_request_params()
        return Request(
            url=self.get_url(),
            method=Request.Method.post,
            json=js.dumps(params),
            headers={"Authorization": f"Bearer {self.access_token}"},
        )


class Value(BaseModel):
    table_id: str
    access_token: str
    sheet_name: str
    range: str
    value: dict | None
    path: str = "values"
    value_input_option: str = "valueInputOption=USER_ENTERED"

    def get_url(self, method) -> str | None:
        base_url: str = ("/").join([BASE_URL, self.table_id, self.path])
        url: str = ("/").join([base_url, ("!").join([self.sheet_name, self.range])])
        if method == "get":
            return url
        if method == "put":
            return ("?").join([url, self.value_input_option])

    def get_values(self) -> Request:
        return Request(
            url=self.get_url("get"),
            method=Request.Method.get,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

    def _get_request_params(self) -> dict:
        res: dict[str, Any] = {
            "range": f"{self.sheet_name}!{self.range}",
            "majorDimension": "ROWS",
            "values": self.value["values"],
        }
        return res

    def add_values(self) -> Request:
        params: dict = self._get_request_params()
        return Request(
            url=self.get_url("put"),
            method=Request.Method.put,
            json=js.dumps(params),
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
