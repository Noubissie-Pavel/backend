from app.models.operation import Operation
from app.schemas.operation import OperationSchema
from app.schemas.transaction import TransactionCreateSchema


def get_ussd_operation_by_code(operation_result: Operation, transaction_data: TransactionCreateSchema):
    operation_data = OperationSchema.model_validate(operation_result)

    print("--------------------------------------", operation_data.ussd_code)
    print("--------------------------------------", transaction_data)
    return None
