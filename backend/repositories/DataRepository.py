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

    @staticmethod
    def update_status_alle_lampen(status):
        sql = "UPDATE lampen SET status = %s"
        params = [status]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def get_power_usage():
        sql = "SELECT deviceid, date FROM history where deviceid = 4"
        solar = Database.get_rows(sql)
        sql = "SELECT deviceid, date FROM solar.History where deviceid = 5"
        car = Database.get_rows(sql)
        sql = "SELECT deviceid, date FROM solar.History where deviceid = 10"
        grid = Database.get_rows(sql)

        return {
            "solar": solar,
            "car": car,
            "grid": grid
        }

