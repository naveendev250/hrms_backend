from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.models.attendance import Attendance
from app.schemas.attendance_schema import AttendanceCreate


class AttendanceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, attendance: AttendanceCreate) -> Attendance:
        db_attendance = Attendance(
            employee_id=attendance.employee_id,
            date=attendance.date,
            status=attendance.status
        )
        self.db.add(db_attendance)
        self.db.commit()
        self.db.refresh(db_attendance)
        return db_attendance

    def get_by_id(self, attendance_id: int) -> Optional[Attendance]:
        return self.db.query(Attendance).filter(Attendance.id == attendance_id).first()

    def get_by_employee_id(self, employee_id: str) -> List[Attendance]:
        return self.db.query(Attendance).filter(
            Attendance.employee_id == employee_id
        ).order_by(Attendance.date.desc()).all()

    def get_all(self, from_date: Optional[date] = None, to_date: Optional[date] = None) -> List[Attendance]:
        query = self.db.query(Attendance)
        
        if from_date:
            query = query.filter(Attendance.date >= from_date)
        if to_date:
            query = query.filter(Attendance.date <= to_date)
        
        return query.order_by(Attendance.date.desc()).all()

    def get_by_employee_and_date(self, employee_id: str, attendance_date: date) -> Optional[Attendance]:
        return self.db.query(Attendance).filter(
            Attendance.employee_id == employee_id,
            Attendance.date == attendance_date
        ).first()

    def exists_for_date(self, employee_id: str, attendance_date: date) -> bool:
        return self.db.query(Attendance).filter(
            Attendance.employee_id == employee_id,
            Attendance.date == attendance_date
        ).count() > 0
