from pydantic import BaseModel


class CredentialResponse(BaseModel):
    credential: str
    select_by: str
