from sqlite3 import IntegrityError
from database import db
from telethon.types import User
from errors import ErrorCode
from reports import Report, ErrorReport, ReportCode
from models import MyUser, Step


def get_user(user: User):
    cur = db.cursor()
    query = "select * from users where chat_id = ?"
    cur.execute(query, (user.id,))
    result = cur.fetchone()
    cur.close()
    if result is None:
        return None

    else:
        user = MyUser(chat_id=result[0], name=result[1], step=result[2])
        return user


def sign_user(user: User):
    cur = db.cursor()
    query = "insert into users (chat_id , name ) values (? , ?) "

    try:
        cur.execute(query, (user.id, user.first_name))
        cur.close()
        db.commit()
        report = Report(status_code=ReportCode.SUCCESS)
        return report

    except IntegrityError as error:
        cur.close()

        if error.sqlite_errorcode == ErrorCode.SQLITE_CONSTRAINT_UNIQUE:
            report = ErrorReport(status_code=ReportCode.UNSUCCESSFUL, error_code=ErrorCode.SQLITE_CONSTRAINT_UNIQUE)
            return report


def change_step(user: MyUser, step):
    cur = db.cursor()
    query = "UPDATE users SET step = ? WHERE chat_id=?"
    cur.execute(query, (step, user.chat_id))
