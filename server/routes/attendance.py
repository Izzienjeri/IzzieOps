from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from extensions import db
from models import Employee, Attendance, Break, ActivityLog  # Assume these models exist
from serializer import AttendanceSchema, BreakSchema, ActivityLogSchema  # Assume these serializers exist
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)
api = Api(attendance_bp)

# Create request parsers for the various operations
clock_in_parser = reqparse.RequestParser()
clock_in_parser.add_argument('employee_id', type=str, required=True, help='Employee ID is required')

clock_out_parser = reqparse.RequestParser()
clock_out_parser.add_argument('employee_id', type=str, required=True, help='Employee ID is required')

start_break_parser = reqparse.RequestParser()
start_break_parser.add_argument('employee_id', type=str, required=True, help='Employee ID is required')

end_break_parser = reqparse.RequestParser()
end_break_parser.add_argument('employee_id', type=str, required=True, help='Employee ID is required')

retrieve_timesheet_parser = reqparse.RequestParser()
retrieve_timesheet_parser.add_argument('employee_id', type=str, required=True, help='Employee ID is required')


class ClockIn(Resource):
    def post(self):
        args = clock_in_parser.parse_args()
        employee_id = args['employee_id']
        current_time = datetime.utcnow()

        # Check if employee is already clocked in
        attendance = Attendance.query.filter_by(employee_id=employee_id, clock_out_time=None).first()
        if attendance:
            return {'message': 'Employee is already clocked in.'}, 400

        # Create a new attendance record
        new_attendance = Attendance(employee_id=employee_id, clock_in_time=current_time)
        db.session.add(new_attendance)
        db.session.commit()

        return {'message': 'Clock-in successful.', 'clock_in_time': current_time}, 201


class ClockOut(Resource):
    def post(self):
        args = clock_out_parser.parse_args()
        employee_id = args['employee_id']
        current_time = datetime.utcnow()

        # Check for existing clock-in record
        attendance = Attendance.query.filter_by(employee_id=employee_id, clock_out_time=None).first()
        if not attendance:
            return {'message': 'Employee is not clocked in.'}, 400

        # Update attendance record with clock-out time
        attendance.clock_out_time = current_time
        db.session.commit()

        total_hours = (attendance.clock_out_time - attendance.clock_in_time).total_seconds() / 3600
        return {'message': 'Clock-out successful.', 'total_hours': total_hours}, 200


class StartBreak(Resource):
    def post(self):
        args = start_break_parser.parse_args()
        employee_id = args['employee_id']
        current_time = datetime.utcnow()

        # Validate that the employee is clocked in
        attendance = Attendance.query.filter_by(employee_id=employee_id, clock_out_time=None).first()
        if not attendance:
            return {'message': 'Employee is not clocked in.'}, 400

        # Log the start of the break
        new_break = Break(employee_id=employee_id, break_start_time=current_time, attendance_id=attendance.id)
        db.session.add(new_break)
        db.session.commit()

        return {'message': 'Break started.', 'break_start_time': current_time}, 201


class EndBreak(Resource):
    def post(self):
        args = end_break_parser.parse_args()
        employee_id = args['employee_id']
        current_time = datetime.utcnow()

        # Validate that the employee is on a break
        break_record = Break.query.filter_by(employee_id=employee_id, break_end_time=None).first()
        if not break_record:
            return {'message': 'Employee is not on a break.'}, 400

        # Update the break record with the end time
        break_record.break_end_time = current_time
        db.session.commit()

        duration = (break_record.break_end_time - break_record.break_start_time).total_seconds() / 60  # Duration in minutes
        return {'message': 'Break ended.', 'duration': duration}, 200


class RetrieveTimesheet(Resource):
    def get(self):
        args = retrieve_timesheet_parser.parse_args()
        employee_id = args['employee_id']

        # Fetch attendance records
        attendance_records = Attendance.query.filter_by(employee_id=employee_id).all()
        attendance_schema = AttendanceSchema(many=True)
        return attendance_schema.dump(attendance_records), 200


# Add resources to the API
api.add_resource(ClockIn, '/api/attendance/clock-in')
api.add_resource(ClockOut, '/api/attendance/clock-out')
api.add_resource(StartBreak, '/api/attendance/start-break')
api.add_resource(EndBreak, '/api/attendance/end-break')
api.add_resource(RetrieveTimesheet, '/api/attendance/timesheet')

