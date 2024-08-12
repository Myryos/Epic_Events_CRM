from peewee import IntegerField, CharField, TimestampField
from .base import BaseModel
from datetime import datetime, timedelta
import bcrypt
import jwt
import os

from dotenv import load_dotenv


load_dotenv()


class Employee(BaseModel):
    MANAGER = 1
    SALESMAN = 2
    SUPPORT = 3

    ROLE_CHOICES = ((MANAGER, "Manager"), (SALESMAN, "Salesman"), (SUPPORT, "Support"))

    id = IntegerField(primary_key=True)
    full_name = CharField(max_length=64)
    email = CharField(max_length=128, unique=True)
    password = CharField(max_length=60)
    role = IntegerField(choices=ROLE_CHOICES)
    creation_time = TimestampField()
    update_time = TimestampField()
    salt = CharField(max_length=4)

    class Meta:
        table_name = "employee"

    def __str__(self):
        return self.full_name

    def to_dict(self):
        return {
            "Full Name": self.full_name,
            "Email": self.email,
            "Role": self.role,
            "Creation Time": self.creation_time,
            "Update Time": self.update_time,
        }

    def set_password(self, raw_password):
        self.salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(raw_password.encode("utf-8"), self.salt).decode(
            "utf-8"
        )

    def check_password(self, raw_password):
        return bcrypt.checkpw(
            raw_password.encode("utf-8"), self.password.encode("utf-8")
        )

    def save(self, *args, **kwargs):
        self.update_time = datetime.now()
        super().save(*args, **kwargs)

    def generate_jwt(self):
        payload = {
            "employee_id": self.id,
            "exp": datetime.now()
            + timedelta(seconds=int(os.getenv("JWT_EXP_DELTA_SECONDS"))),
        }

        token = jwt.encode(
            payload,
            os.getenv("JWT_SECRET_KEY"),
            algorithm=os.getenv("JWT_ALGORITHM"),
        )
        return token

    @staticmethod
    def decode_jwt(token):
        try:
            payload = jwt.decode(
                jwt=token,
                key=os.getenv("JWT_SECRET_KEY"),
                algorithms=[os.getenv("JWT_ALGORITHM")],
            )
            return payload.get("employee_id")
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
            return None
        except jwt.InvalidTokenError:
            print("Invalid token.")
            return None

    @staticmethod
    def set_token(token):
        os.environ["EMPLOYEE_TOKEN"] = token
        with open("token.txt", "w") as f:
            f.write(token)

    @staticmethod
    def load_token():
        try:
            with open("token.txt", "r") as f:
                token = f.read().strip()
                return token
        except FileNotFoundError:
            return None
