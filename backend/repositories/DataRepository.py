from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.method != 'GET' and request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_status_lampen():
        sql = "SELECT * from lampen"
        return Database.get_rows(sql)

    @staticmethod
    def read_status_lamp_by_id(id):
        sql = "SELECT * from lampen WHERE id = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def update_status_lamp(id, status):
        sql = "UPDATE lampen SET status = %s WHERE id = %s"
        params = [status, id]
        return Database.execute_sql(sql, params)

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
