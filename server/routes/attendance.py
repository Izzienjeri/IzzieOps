from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse
from extensions import db
from models import AttendanceRecord
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

attendance_bp = Blueprint('attendance', __name__)
api = Api(attendance_bp)

# Attendance Parser
attendance_parser = reqparse.RequestParser()
attendance_parser.add_argument('employee_id', type=str, required=True, help="Employee ID is required")
attendance_parser.add_argument('clock_in_time', type=str)  # ISO format
attendance_parser.add_argument('clock_out_time', type=str)  # ISO format
attendance_parser.add_argument('break_start_time', type=str)  # ISO format
attendance_parser.add_argument('break_end_time', type=str)  # ISO format

class ClockIn(Resource):
    def post(self):
        args = attendance_parser.parse_args()
        record = AttendanceRecord(
            employee_id=args['employee_id'],
            clock_in_time=datetime.utcnow() if not args['clock_in_time'] else datetime.fromisoformat(args['clock_in_time'])
        )
        db.session.add(record)
        db.session.commit()
        return {"message": "Clock-in recorded successfully"}, 201

class ClockOut(Resource):
    def put(self, record_id):
        # Parse arguments
        args = attendance_parser.parse_args()
        
        # Retrieve the attendance record using the provided record_id
        record = AttendanceRecord.query.get(record_id)
        if not record:
            return {"message": "Attendance record not found"}, 404
        
        # Check if the employee_id matches the record
        if record.employee_id != args['employee_id']:
            return {"message": "Unauthorized: Employee ID does not match the record"}, 403
        
        # Set clock_out_time
        record.clock_out_time = datetime.utcnow() if not args['clock_out_time'] else datetime.fromisoformat(args['clock_out_time'])

        # Calculate total hours worked
        if record.clock_in_time and record.clock_out_time:
            total_hours = (record.clock_out_time - record.clock_in_time).total_seconds() / 3600  # Convert to hours
            
            if record.break_start_time and record.break_end_time:
                break_duration = (record.break_end_time - record.break_start_time).total_seconds() / 3600
                total_hours -= break_duration  # Subtract break duration from total hours

            record.total_hours_worked = total_hours
        
        # Commit changes to the database
        db.session.commit()
        return {"message": "Clock-out recorded successfully"}, 200



class StartBreak(Resource):
    def put(self, record_id):
        args = attendance_parser.parse_args()
        record = AttendanceRecord.query.get(record_id)
        if not record:
            return {"message": "Attendance record not found"}, 404
        
        if record.break_start_time and not record.break_end_time:
            return {"message": "Break is already in progress"}, 400
        
        record.break_start_time = datetime.utcnow() if not args['break_start_time'] else datetime.fromisoformat(args['break_start_time'])
        db.session.commit()
        return {"message": "Break started successfully"}, 200


class EndBreak(Resource):
    def put(self, record_id):
        args = attendance_parser.parse_args()
        record = AttendanceRecord.query.get(record_id)
        if not record:
            return {"message": "Attendance record not found"}, 404
        
        if not record.break_start_time:
            return {"message": "No break has been started"}, 400
        
        if record.break_end_time:
            return {"message": "Break has already ended"}, 400
        
        record.break_end_time = datetime.utcnow() if not args['break_end_time'] else datetime.fromisoformat(args['break_end_time'])
        db.session.commit()
        return {"message": "Break ended successfully"}, 200

class GetAttendanceRecord(Resource):
    def get(self, employee_id):
        records = AttendanceRecord.query.filter_by(employee_id=employee_id).all()
        if not records:
            return {"message": "No attendance records found for this employee"}, 404
        
        attendance_data = [{
            "id": record.id,
            "clock_in_time": record.clock_in_time,
            "clock_out_time": record.clock_out_time,
            "break_start_time": record.break_start_time,
            "break_end_time": record.break_end_time,
            "total_hours_worked": record.total_hours_worked
        } for record in records]
        
        return jsonify(attendance_data)

class AttendanceSummary(Resource):
    def get(self, employee_id, time_period):
        now = datetime.utcnow()
        start_date, end_date = None, None
        
        if time_period == "daily":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif time_period == "weekly":
            start_date = now - timedelta(days=now.weekday())  # Monday of the current week
            end_date = start_date + timedelta(days=6)  # Sunday of the current week
        elif time_period == "monthly":
            start_date = now.replace(day=1)  # First day of the month
            end_date = (start_date + relativedelta(months=1)) - timedelta(days=1)  # Last day of the month

        records = AttendanceRecord.query.filter(
            AttendanceRecord.employee_id == employee_id,
            AttendanceRecord.clock_in_time >= start_date,
            AttendanceRecord.clock_out_time <= end_date
        ).all()

        total_hours = sum(record.total_hours_worked for record in records if record.total_hours_worked)

        return jsonify({
            "employee_id": employee_id,
            "time_period": time_period,
            "total_hours": total_hours
        })    

api.add_resource(ClockIn, '/clock-in')
api.add_resource(ClockOut, '/clock-out/<string:record_id>')
api.add_resource(StartBreak, '/start-break/<string:record_id>')
api.add_resource(EndBreak, '/end-break/<string:record_id>')
api.add_resource(GetAttendanceRecord, '/attendance/<string:employee_id>')
api.add_resource(AttendanceSummary, '/attendance-summary/<string:employee_id>/<string:time_period>')

