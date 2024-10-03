from marshmallow import Schema, fields, post_load
from models import Employee, Document, Task, Attendance, LeaveRequest, Payroll

class EmployeeSchema(Schema):
    id = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    position = fields.Str(required=True)
    manager_id = fields.Str(allow_none=True)
    documents = fields.List(fields.Nested('DocumentSchema'), dump_only=True)
    tasks = fields.List(fields.Nested('TaskSchema'), dump_only=True)
    leave_requests = fields.List(fields.Nested('LeaveRequestSchema'), dump_only=True)

    @post_load
    def create_employee(self, data, **kwargs):
        return Employee(**data)

class DocumentSchema(Schema):
    id = fields.Str(required=True)
    employee_id = fields.Str(required=True)
    document_type = fields.Str(required=True)
    file_path = fields.Str(required=True)

    @post_load
    def create_document(self, data, **kwargs):
        return Document(**data)

class TaskSchema(Schema):
    id = fields.Str(required=True)
    employee_id = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    status = fields.Str(required=True)
    due_date = fields.Date(required=True)

    @post_load
    def create_task(self, data, **kwargs):
        return Task(**data)

class AttendanceSchema(Schema):
    id = fields.Str(required=True)
    employee_id = fields.Str(required=True)
    clock_in_time = fields.DateTime(required=True)
    clock_out_time = fields.DateTime(allow_none=True)
    status = fields.Str(required=True)

    @post_load
    def create_attendance(self, data, **kwargs):
        return Attendance(**data)

class LeaveRequestSchema(Schema):
    id = fields.Str(required=True)
    employee_id = fields.Str(required=True)
    leave_type = fields.Str(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    status = fields.Str(required=True)

    @post_load
    def create_leave_request(self, data, **kwargs):
        return LeaveRequest(**data)

class PayrollSchema(Schema):
    id = fields.Str(required=True)
    employee_id = fields.Str(required=True)
    salary = fields.Float(required=True)
    pay_date = fields.Date(required=True)
    pay_period_start = fields.Date(required=True)
    pay_period_end = fields.Date(required=True)

    @post_load
    def create_payroll(self, data, **kwargs):
        return Payroll(**data)

employee_schema = EmployeeSchema()
document_schema = DocumentSchema()
task_schema = TaskSchema()
attendance_schema = AttendanceSchema()
leave_request_schema = LeaveRequestSchema()
payroll_schema = PayrollSchema()

employees_schema = EmployeeSchema(many=True)
documents_schema = DocumentSchema(many=True)
tasks_schema = TaskSchema(many=True)
attendances_schema = AttendanceSchema(many=True)
leave_requests_schema = LeaveRequestSchema(many=True)
payrolls_schema = PayrollSchema(many=True)
