from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.db.database import get_db
from app.schemas.attendance_schema import AttendanceCreate, AttendanceResponse
from app.services.attendance_service import AttendanceService
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.employee_repository import EmployeeRepository

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])


def get_attendance_service(db: Session = Depends(get_db)) -> AttendanceService:
    attendance_repo = AttendanceRepository(db)
    employee_repo = EmployeeRepository(db)
    return AttendanceService(attendance_repo, employee_repo)


@router.post(
    "/",
    response_model=AttendanceResponse,
    status_code=status.HTTP_201_CREATED
)
def mark_attendance(
    attendance: AttendanceCreate,
    service: AttendanceService = Depends(get_attendance_service)
):
    return service.mark_attendance(attendance)


@router.get(
    "/",
    response_model=List[AttendanceResponse]
)
def get_all_attendance(
    from_date: Optional[date] = Query(None, description="Filter attendance from this date (inclusive)"),
    to_date: Optional[date] = Query(None, description="Filter attendance to this date (inclusive)"),
    service: AttendanceService = Depends(get_attendance_service)
):
    return service.get_all_attendance(from_date, to_date)


@router.get(
    "/employee/{employee_id}",
    response_model=List[AttendanceResponse]
)
def get_attendance_by_employee(
    employee_id: str,
    service: AttendanceService = Depends(get_attendance_service)
):
    return service.get_attendance_by_employee(employee_id)
