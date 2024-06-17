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
    
    # update device state in db
    @staticmethod
    def write_appliance(id, state):
        sql = 'insert into DeviceHistory (DeviceID, Date, Value) values (%s, %s, %s)'
        return Database.execute_sql(sql, params=[id, datetime.now(), state])

    # get power usage history
    @staticmethod
    def get_power_usage(scale):       

        sql_constant = "SELECT constant FROM Device WHERE DeviceID = %s;"

        sql_hour = """
                WITH RECURSIVE intervals AS (
                    SELECT 
                        NOW() - INTERVAL 1 HOUR AS start_interval, 
                        DATE_ADD(NOW() - INTERVAL 1 HOUR, INTERVAL 10 MINUTE) AS end_interval
                    UNION ALL
                    SELECT 
                        start_interval + INTERVAL 10 MINUTE, 
                        end_interval + INTERVAL 10 MINUTE
                    FROM intervals
                    WHERE start_interval + INTERVAL 10 MINUTE < NOW()
                )
                SELECT
                    date_format(date_add(intervals.start_interval, INTERVAL 10 MINUTE), "%H:%i") AS time,
                    COUNT(DeviceHistory.historyid) AS count
                FROM
                    intervals
                LEFT JOIN
                    DeviceHistory
                ON
                    DeviceHistory.date >= intervals.start_interval 
                    AND DeviceHistory.date < intervals.end_interval
                    AND DeviceHistory.deviceid = %s
                GROUP BY
                    intervals.start_interval
                ORDER BY
                    intervals.start_interval asc;
            """
        sql_day = """
                WITH RECURSIVE intervals AS (
                    SELECT 
                        NOW() - INTERVAL 1 DAY AS start_interval, 
                        DATE_ADD(NOW() - INTERVAL 1 DAY, INTERVAL 1 HOUR) AS end_interval
                    UNION ALL
                    SELECT 
                        start_interval + INTERVAL 1 HOUR, 
                        end_interval + INTERVAL 1 HOUR
                    FROM intervals
                    WHERE start_interval + INTERVAL 1 HOUR < NOW()
                )
                SELECT
                    date_format(date_add(intervals.start_interval, INTERVAL 1 HOUR), "%H:%i") AS time,
                    COUNT(DeviceHistory.historyid) AS count
                FROM
                    intervals
                LEFT JOIN
                    DeviceHistory
                ON
                    DeviceHistory.date >= intervals.start_interval 
                    AND DeviceHistory.date < intervals.end_interval
                    AND DeviceHistory.deviceid = %s
                GROUP BY
                    intervals.start_interval
                ORDER BY
                    intervals.start_interval asc;
            """
        sql_week = """
                WITH RECURSIVE intervals AS (
                    SELECT 
                        NOW() - INTERVAL 7 DAY AS start_interval, 
                        DATE_ADD(NOW() - INTERVAL 7 DAY, INTERVAL 1 DAY) AS end_interval
                    UNION ALL
                    SELECT 
                        start_interval + INTERVAL 1 DAY, 
                        end_interval + INTERVAL 1 DAY
                    FROM intervals
                    WHERE start_interval + INTERVAL 1 DAY < NOW()
                )
                SELECT
                    date_format(date_add(intervals.start_interval, INTERVAL 1 day), "%d/%m") AS time,
                    COUNT(DeviceHistory.historyid) AS count
                FROM
                    intervals
                LEFT JOIN
                    DeviceHistory
                ON
                    DeviceHistory.date >= intervals.start_interval 
                    AND DeviceHistory.date < intervals.end_interval
                    AND DeviceHistory.deviceid = %s
                GROUP BY
                    intervals.start_interval
                ORDER BY
                    intervals.start_interval asc;
            """
        
        if scale == 1:
            solar = {"constant": Database.get_one_row(sql_constant, params=[4]), "values": Database.get_rows(sql_hour, params=[4])}
            eco = {"constant": Database.get_one_row(sql_constant, params=[5]), "values": Database.get_rows(sql_hour, params=[5])}
            house = {"constant": Database.get_one_row(sql_constant, params=[6]), "values": Database.get_rows(sql_hour, params=[6])}
        elif scale == 2:
            solar = {"constant": Database.get_one_row(sql_constant, params=[4]), "values": Database.get_rows(sql_day, params=[4])}
            eco = {"constant": Database.get_one_row(sql_constant, params=[5]), "values": Database.get_rows(sql_day, params=[5])}
            house = {"constant": Database.get_one_row(sql_constant, params=[6]), "values": Database.get_rows(sql_day, params=[6])}
        elif scale == 3:
            solar = {"constant": Database.get_one_row(sql_constant, params=[4]), "values": Database.get_rows(sql_week, params=[4])}
            eco = {"constant": Database.get_one_row(sql_constant, params=[5]), "values": Database.get_rows(sql_week, params=[5])}
            house = {"constant": Database.get_one_row(sql_constant, params=[6]), "values": Database.get_rows(sql_week, params=[6])}
        else:
            return 0
        
        return {"solar": solar, "eco": eco, "house": house}
    
    # write pulses from energymeter to db
    @staticmethod
    def write_pulse(pin):
        if pin == 5:
            id = 5
            name = "eco"
        elif pin == 6:
            id = 4
            name = "solar"
        elif pin == 1:
            id = 6
            name = "house"

        sql = "insert into DeviceHistory (DeviceID, Date) values (%s, %s)"
        Database.execute_sql(sql, params=[id, datetime.now()])
        return name

    @staticmethod
    def get_appliances():
        sql = 'SELECT Value FROM DeviceHistory where deviceid = 9 order by date desc limit 1;'
        oven = Database.get_one_row(sql)
        sql = 'SELECT Value FROM DeviceHistory where deviceid = 8 order by date desc limit 1;'
        ac = Database.get_one_row(sql)
        sql = 'SELECT Value FROM DeviceHistory where deviceid = 7 order by date desc limit 1;'
        wash = Database.get_one_row(sql)

        try:
            return {
            "data":[{"id": 9, "value": oven["Value"]}, {"id": 8, "value": ac["Value"]}, {"id": 7, "value": wash["Value"]}]
            }
        except Exception as ex:
            print(ex)
            return 

        

