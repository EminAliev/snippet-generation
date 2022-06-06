from pydantic import BaseModel


class InputUrl(BaseModel):
    url: str


class InputFile(BaseModel):
    file: str