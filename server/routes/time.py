# server/routes/time.py

from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse
from extensions import db
from models import AttendanceRecord, Timesheet, Employee
from datetime import datetime

time_bp = Blueprint('time', __name__)
api = Api(time_bp)

# Clock-in and Clock-out Parser
attendance_parser = reqparse.RequestParser()
attendance_parser.add_argument('employee_id', type=str, required=True, help="Employee ID is required")

# Timesheet Parser
timesheet_parser = reqparse.RequestParser()
timesheet_parser.add_argument('employee_id', type=str, required=True, help="Employee ID is required")
timesheet_parser.add_argument('week_start_date', type=str, required=True, help="Week start date is required")
timesheet_parser.add_argument('week_end_date', type=str, required=True, help="Week end date is required")

class ClockIn(Resource):
    def post(self):
        args = attendance_parser.parse_args()
        employee = Employee.query.get(args['employee_id'])
        
        if not employee:
            return {"message": "Employee not found"}, 404

        # Check if already clocked in today
        today = datetime.utcnow().date()
        attendance_record = AttendanceRecord.query.filter_by(employee_id=employee.id, date=today).first()
        
        if attendance_record and attendance_record.clock_out_time is None:
            return {"message": "Already clocked in today"}, 400

        # Create new attendance record
        attendance = AttendanceRecord(
            employee_id=employee.id,
            clock_in_time=datetime.utcnow(),
            date=today
        )
        db.session.add(attendance)
        db.session.commit()
        
        return {"message": "Clock-in successful"}, 201

class ClockOut(Resource):
    def put(self, attendance_id):
        attendance_record = AttendanceRecord.query.get(attendance_id)
        
        if not attendance_record or attendance_record.clock_out_time is not None:
            return {"message": "Attendance record not found or already clocked out"}, 404

        # Record clock-out time and calculate hours worked
        attendance_record.clock_out_time = datetime.utcnow()
        time_worked = (attendance_record.clock_out_time - attendance_record.clock_in_time).total_seconds() / 3600
        attendance_record.total_hours_worked = time_worked
        db.session.commit()
        
        return {"message": "Clock-out successful", "hours_worked": time_worked}, 200

class SubmitTimesheet(Resource):
    def post(self):
        args = timesheet_parser.parse_args()
        employee = Employee.query.get(args['employee_id'])
        
        if not employee:
            return {"message": "Employee not found"}, 404

        # Create timesheet record
        timesheet = Timesheet(
            employee_id=employee.id,
            week_start_date=datetime.strptime(args['week_start_date'], '%Y-%m-%d').date(),
            week_end_date=datetime.strptime(args['week_end_date'], '%Y-%m-%d').date(),
            total_hours=0.0  
        )
        db.session.add(timesheet)
        db.session.commit()

        return {"message": "Timesheet submitted successfully"}, 201

class GetAttendanceRecords(Resource):
    def get(self, employee_id):
        attendance_records = AttendanceRecord.query.filter_by(employee_id=employee_id).all()
        if not attendance_records:
            return {"message": "No attendance records found"}, 404

        records = [{
            "date": record.date,
            "clock_in_time": record.clock_in_time,
            "clock_out_time": record.clock_out_time,
            "total_hours_worked": record.total_hours_worked
        } for record in attendance_records]

        return {"attendance_records": records}, 200

class GetTimesheets(Resource):
    def get(self, employee_id):
        timesheets = Timesheet.query.filter_by(employee_id=employee_id).all()
        if not timesheets:
            return {"message": "No timesheets found"}, 404

        sheets = [{
            "week_start_date": timesheet.week_start_date,
            "week_end_date": timesheet.week_end_date,
            "total_hours": timesheet.total_hours,
            "approved": timesheet.approved
        } for timesheet in timesheets]

        return {"timesheets": sheets}, 200

api.add_resource(ClockIn, '/clock-in')
api.add_resource(ClockOut, '/clock-out/<string:attendance_id>')
api.add_resource(SubmitTimesheet, '/submit-timesheet')
api.add_resource(GetAttendanceRecords, '/<string:employee_id>/attendance-records')
api.add_resource(GetTimesheets, '/<string:employee_id>/timesheets')
