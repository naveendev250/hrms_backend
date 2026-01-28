from typing import List, Optional
from datetime import date
from fastapi import HTTPException, status
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.attendance_schema import AttendanceCreate, AttendanceResponse


class AttendanceService:
    def __init__(self, attendance_repo: AttendanceRepository, employee_repo: EmployeeRepository):
        self.attendance_repo = attendance_repo
        self.employee_repo = employee_repo

    def mark_attendance(self, attendance: AttendanceCreate) -> AttendanceResponse:
        if not self.employee_repo.exists_by_id(attendance.employee_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID '{attendance.employee_id}' not found"
            )

        if self.attendance_repo.exists_for_date(attendance.employee_id, attendance.date):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Attendance already marked for employee '{attendance.employee_id}' on {attendance.date}"
            )

        db_attendance = self.attendance_repo.create(attendance)
        return AttendanceResponse.model_validate(db_attendance)

    def get_all_attendance(self, from_date: Optional[date] = None, to_date: Optional[date] = None) -> List[AttendanceResponse]:
        attendance_records = self.attendance_repo.get_all(from_date, to_date)
        return [AttendanceResponse.model_validate(att) for att in attendance_records]

    def get_attendance_by_employee(self, employee_id: str) -> List[AttendanceResponse]:
        if not self.employee_repo.exists_by_id(employee_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID '{employee_id}' not found"
            )

        attendance_records = self.attendance_repo.get_by_employee_id(employee_id)
        return [AttendanceResponse.model_validate(att) for att in attendance_records]
