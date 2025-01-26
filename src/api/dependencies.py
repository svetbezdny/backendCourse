from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(5, ge=1, le=20)]


PaginationDep = Annotated[PaginationParams, Depends()]
