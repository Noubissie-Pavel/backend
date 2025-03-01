import time

import serial

from app.models.operation import Operation
from app.schemas.operation import OperationSchema
from app.schemas.transaction import TransactionCreateSchema


def send_at_command(command):
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

    decoded_response = send_AT_command(f'AT+CUSD=1,"*126*1*{telephone_number}*{amount}#",15').decode(errors='ignore')


def get_ussd_operation_by_code(operation: Operation, transaction_data: TransactionCreateSchema):
    # send_at_command('AT+CUSD=2')
    send_at_command('AT+CMGD=0,4') ## delte all sms
    message = send_at_command('AT+CMGR=0')
    print("-------------------------------------------------------------------------------", message)
    # send_at_command('AT+CMGD=1,4')
    # decoded_om_response = (send_at_command(
    #     f'AT+CUSD=1,"{operation.ussd_code}*{transaction_data.amount}*{transaction_data.receiver_phone_number}#",15')
    #                        .decode(errors='ignore'))
    # print("-------------------------------------------------------------------------------", decoded_om_response)
    # om_code_pin = send_at_command('AT+CUSD=1,"2020",1').decode(errors='ignore')
    # print("-------------------------------------------------------------------------------", om_code_pin)
    # double_confirmation = send_at_command('AT+CUSD=1,"1",1').decode(errors='ignore')
    # print("-------------------------------------------------------------------------------", double_confirmation)

    return None


def testing_momo(operation: Operation, transaction_data: TransactionCreateSchema):
    operation_data = OperationSchema.model_validate(operation)
    return operation_data
