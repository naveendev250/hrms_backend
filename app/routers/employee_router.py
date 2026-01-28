from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.employee_schema import EmployeeCreate, EmployeeResponse
from app.services.employee_service import EmployeeService
from app.repositories.employee_repository import EmployeeRepository

router = APIRouter(prefix="/api/employees", tags=["Employees"])


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    repository = EmployeeRepository(db)
    return EmployeeService(repository)


@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_employee(
    employee: EmployeeCreate,
    service: EmployeeService = Depends(get_employee_service)
):
    return service.create_employee(employee)


@router.get(
    "/",
    response_model=List[EmployeeResponse]
)
def get_all_employees(
    service: EmployeeService = Depends(get_employee_service)
):
    return service.get_all_employees()


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee(
    employee_id: str,
    service: EmployeeService = Depends(get_employee_service)
):
    return service.get_employee_by_id(employee_id)


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_200_OK
)
def delete_employee(
    employee_id: str,
    service: EmployeeService = Depends(get_employee_service)
):
    return service.delete_employee(employee_id)
