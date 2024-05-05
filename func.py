import re
import sqlite3
import datetime
import time
import urllib

def check_internet_connection():
    try:
        urllib.request.urlopen('http://www.google.com', timeout=1)
        return True
    except Exception as err:
        print(f"ошибка проверки интернета {err}")
        return False

def check_date_format(date_text: str) -> bool:
    try:
        if datetime.datetime.strptime(date_text or "", "%d.%m"):
            print("it's a date")
            return True
        else:
            print("it's not a date")
            return False
    except Exception as e:
        print(e)
        return False


def check_time_format(time_text: str) -> bool:
    try:
        if re.match(r'[0-5]{1}[0-9]{1}.[0-5]{1}[0-9]{1}', time_text):
            print("time")
            return True
        else:
            print("not time")
            return False
    except Exception as e:
        print(e)
        return False

def add_reminde_database(user_id: str,
                         reminde_text: str,
                         date_text: str,
                         time_text: str,
                         ) -> bool:
    """

    :param reminde_text: текст напоминания
    :param date_text: текст даты
    :param time_text: текст времени
    :return:
    """
    try:
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        dt_check = time.strptime(date_text, '%d.%m')
        dt_check = time.strftime('%d.%m', dt_check)
        tm_check = time.strptime(time_text, '%H.%M')
        tm_check = time.strftime('%H.%M', tm_check)


        cur.execute(f"""INSERT INTO users(user_id,reminde_text,reminde_date,reminde_time,done)
                    VALUES("{user_id}","{reminde_text}","{dt_check}","{tm_check}","TRUE");""")
        con.commit()
        return True
    except Exception as e:
        print(e)
        return False

def remember(bot):
    while(True):
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        now = datetime.datetime.now()
        today = datetime.datetime.today()
        todayD = today.strftime("%d.%m")
        current_time = now.strftime("%H.%M")
        cur.execute(f"SELECT id,user_id,reminde_text FROM users WHERE done='TRUE' AND reminde_date='{todayD}' AND reminde_time='{current_time}';")
        one_result = cur.fetchall()
        if len(one_result) > 0:
            print(one_result)
            bot.send_message(one_result[0][1], one_result[0][2])
            sql_delete_query = (f"""DELETE from users WHERE id = {one_result[0][0]}""")
            cur.execute(sql_delete_query)
            conn.commit()
        time.sleep(1)
