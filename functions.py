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
    db.commit()
    cur.close()


def add_file(file_id, access_hash, file_reference, uploader, file_type=None):
    cur = db.cursor()
    if file_type is None:
        query = 'insert into files (file_id,access_hash , file_reference , uploader ) values (? , ? , ? , ?) '
        cur.execute(query, (file_id, access_hash, file_reference, uploader))
    else:
        query = 'insert into files (file_id,access_hash , file_reference , type , uploader ) values (? ,?, ? ,?, ?) '
        cur.execute(query, (file_id, access_hash, file_reference, file_type, uploader))

    rowid = cur.lastrowid
    db.commit()
    cur.close()

    return rowid


def delete_file(rowid):
    cur = db.cursor()
    query = "DELETE FROM files WHERE rowid =?  "
    cur.execute(query, (rowid,))
    db.commit()
    cur.close()


def get_user_files(user: MyUser):
    cur = db.cursor()
    query = "select * from files where uploader = ?"
    cur.execute(query, (user.chat_id,))
    result = cur.fetchall()

    if len(result) == 0:
        return None
    else:
        return result


def get_file(file_id):
    cur = db.cursor()
    query = "select * from files where rowid = ?"
    cur.execute(query, (file_id,))
    result = cur.fetchone()

    if result is None:
        return None

    else:
        return result


def set_file_type(file_id, file_type):
    cur = db.cursor()
    query = "UPDATE files SET type = ? WHERE file_id=?"
    cur.execute(query, (file_type, file_id))
    db.commit()
    cur.close()


def get_file_uploader(rowid):
    cur = db.cursor()
    query = "select uploader from files where rowid = ?"
    cur.execute(query, (rowid,))
    result = cur.fetchone()

    if result is not None:
        return result[0]


def change_file_status(file_rowid, status: int):
    cur = db.cursor()
    query = "UPDATE files SET status = ? WHERE rowid=?"
    cur.execute(query, (status, file_rowid))
    db.commit()
    cur.close()


def get_file_status(file_rowid):
    cur = db.cursor()
    query = "select status from files where rowid = ?"
    cur.execute(query, (file_rowid,))
    result = cur.fetchone()
    cur.close()
    if result is None:
        return None

    else:
        return result
