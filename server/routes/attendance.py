from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse
from extensions import db
from models import AttendanceRecord
from datetime import datetime

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
        args = attendance_parser.parse_args()
        record = AttendanceRecord.query.get(record_id)
        if not record:
            return {"message": "Attendance record not found"}, 404

        record.clock_out_time = datetime.utcnow() if not args['clock_out_time'] else datetime.fromisoformat(args['clock_out_time'])
        # Calculate total hours worked if both clock in and out times are available
        if record.clock_in_time and record.clock_out_time:
            record.total_hours_worked = (record.clock_out_time - record.clock_in_time).total_seconds() / 3600  # Convert to hours

        db.session.commit()
        return {"message": "Clock-out recorded successfully"}, 200

class StartBreak(Resource):
    def put(self, record_id):
        args = attendance_parser.parse_args()
        record = AttendanceRecord.query.get(record_id)
        if not record:
            return {"message": "Attendance record not found"}, 404
        
        record.break_start_time = datetime.utcnow() if not args['break_start_time'] else datetime.fromisoformat(args['break_start_time'])
        db.session.commit()
        return {"message": "Break started successfully"}, 200

class EndBreak(Resource):
    def put(self, record_id):
        args = attendance_parser.parse_args()
        record = AttendanceRecord.query.get(record_id)
        if not record:
            return {"message": "Attendance record not found"}, 404
        
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

api.add_resource(ClockIn, '/clock-in')
api.add_resource(ClockOut, '/clock-out/<string:record_id>')
api.add_resource(StartBreak, '/start-break/<string:record_id>')
api.add_resource(EndBreak, '/end-break/<string:record_id>')
api.add_resource(GetAttendanceRecord, '/attendance/<string:employee_id>')
