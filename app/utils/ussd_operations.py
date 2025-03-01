from app.models.operation import Operation
from app.schemas.operation import OperationSchema


def get_ussd_operation_by_code(operation_result: Operation):
    operation_data = OperationSchema.model_validate(operation_result).model_dump()

    print("--------------------------------------", operation_data)
    return None
