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
    def get_power_usage(scale):            

        sql_hour = """
                WITH RECURSIVE intervals AS (
                    SELECT 
                        NOW() - INTERVAL 1 HOUR AS start_interval, 
                        DATE_ADD(NOW() - INTERVAL 10 MINUTE, INTERVAL 10 MINUTE) AS end_interval
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
                    AND DeviceHistory.deviceid = 5
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
                    AND DeviceHistory.deviceid = 5
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
                    AND DeviceHistory.deviceid = 5
                GROUP BY
                    intervals.start_interval
                ORDER BY
                    intervals.start_interval asc;
            """
        
        if scale == 1:
            return Database.get_rows(sql_hour)
        elif scale == 2:
            return Database.get_rows(sql_day)
        elif scale == 3:
            return Database.get_rows(sql_week)
        else:
            return 0
    

    @staticmethod
    def write_pulse(pin):
        if pin == 5:
            id = 5
        elif pin == 6:
            id = 4
        sql = "insert into History (DeviceID, Date) values (%s, %s)"
        Database.execute_sql(sql, params=[id, datetime.now()])

