from typing import List
from fastapi import HTTPException, status
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee_schema import EmployeeCreate, EmployeeResponse


class EmployeeService:
    def __init__(self, repository: EmployeeRepository):
        self.repository = repository

    def create_employee(self, employee: EmployeeCreate) -> EmployeeResponse:
        if self.repository.exists_by_id(employee.employee_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Employee with ID '{employee.employee_id}' already exists"
            )

        if self.repository.exists_by_email(employee.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Employee with email '{employee.email}' already exists"
            )

        db_employee = self.repository.create(employee)
        return EmployeeResponse.model_validate(db_employee)

    def get_all_employees(self) -> List[EmployeeResponse]:
        employees = self.repository.get_all()
        return [EmployeeResponse.model_validate(emp) for emp in employees]

    def get_employee_by_id(self, employee_id: str) -> EmployeeResponse:
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID '{employee_id}' not found"
            )
        return EmployeeResponse.model_validate(employee)

    def delete_employee(self, employee_id: str) -> dict:
        if not self.repository.exists_by_id(employee_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID '{employee_id}' not found"
            )

        self.repository.delete(employee_id)
        return {"message": f"Employee '{employee_id}' deleted successfully"}
