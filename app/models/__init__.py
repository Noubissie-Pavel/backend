from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models import agency
from app.models import company
from app.models import operation
from app.models import sim_cart
from app.models import telecom_operator
from app.models import transaction
from app.models import user
from app.models import ussd
