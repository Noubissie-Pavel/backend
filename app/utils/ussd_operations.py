import time

import serial

from app.models.operation import Operation
from app.schemas.operation import OperationSchema
from app.schemas.transaction import TransactionCreateSchema


def send_AT_command(command):
    if isinstance(command, str):
        command = command.encode()

    port = serial.Serial(
        port='/dev/ttyUSB2',
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=2,
        xonxoff=False,
        rtscts=False,
        dsrdtr=False,
        write_timeout=2,
        inter_byte_timeout=None,
        exclusive=False
    )

    port.write(command + b'\r')
    time.sleep(2)

    response = port.read(1024)
    port.close()

    if isinstance(response, bytes):
        return response
    return response


def get_ussd_operation_by_code(operation_result: Operation, transaction_data: TransactionCreateSchema):
    result = send_AT_command("AT")
    print(result)
    operation_data = OperationSchema.model_validate(operation_result)

    print("--------------------------------------", operation_data.ussd_code)
    print("--------------------------------------", transaction_data)
    return None
