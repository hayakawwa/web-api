from typing import Annotated

from fastapi import Depends

from repositories.base.unit_of_work import UnitOfWork

UOWDep = Annotated[UnitOfWork, Depends(UnitOfWork)]
