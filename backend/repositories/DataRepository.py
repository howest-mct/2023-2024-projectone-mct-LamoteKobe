from .Database import Database
from datetime import datetime


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.method != 'GET' and request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens
    

    @staticmethod
    def write_ldr(oost, west):
        sql = 'insert into History (DeviceID, Date, Value) values (%s, %s, %s) '
        # Database.execute_sql(sql, params=[1, datetime.now(), oost])
        # Database.execute_sql(sql, params=[2, datetime.now(), west])


    @staticmethod
    def write_device_state(id, state):
        sql = 'insert into History (DeviceID, Date, Value) values (%s, %s, %s)'
        Database.execute_sql(sql, params=[id, datetime.now(), state])

  