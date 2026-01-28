from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.employee import Employee
from app.schemas.employee_schema import EmployeeCreate


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, employee: EmployeeCreate) -> Employee:
        db_employee = Employee(
            employee_id=employee.employee_id,
            full_name=employee.full_name,
            email=employee.email,
            department=employee.department
        )
        self.db.add(db_employee)
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    def get_by_id(self, employee_id: str) -> Optional[Employee]:
        return self.db.query(Employee).filter(Employee.employee_id == employee_id).first()

    def get_by_email(self, email: str) -> Optional[Employee]:
        return self.db.query(Employee).filter(Employee.email == email).first()

    def get_all(self) -> List[Employee]:
        return self.db.query(Employee).all()

    def delete(self, employee_id: str) -> bool:
        employee = self.get_by_id(employee_id)
        if employee:
            self.db.delete(employee)
            self.db.commit()
            return True
        return False

    def exists_by_id(self, employee_id: str) -> bool:
        return self.db.query(Employee).filter(Employee.employee_id == employee_id).count() > 0

    def exists_by_email(self, email: str) -> bool:
        return self.db.query(Employee).filter(Employee.email == email).count() > 0
