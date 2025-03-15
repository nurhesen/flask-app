from pydantic import BaseModel, constr, validator


class PostBase(BaseModel):
    text: constr(max_length=1024)


class PostCreate(PostBase):
    @validator('text')
    def check_text_size(cls, v):
        if len(v.encode('utf-8')) > 1 * 1024 * 1024:
            raise ValueError("Payload exceeds maximum size of 1 MB")
        return v


class PostOut(PostBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes=True
