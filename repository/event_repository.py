import pandas as pd
from sqlalchemy import create_engine
from util.singleton import singleton

@singleton
class EventRepository:
    def __init__(self):
        self.database = "gather_test"
        self.host = "localhost"
        self.user = "db_user"
        self.password = "db_pass"
        self.port = "5433"
        self.connection_string = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    def getMusicalEventRatesUser(self, user_id):
        engine = create_engine(self.connection_string)
        query = """
                SELECT eb.category,
                    (CASE WHEN price IS NULL THEN true ELSE false END) as price,
                    EXTRACT(HOUR FROM start_date)                                             as start_date,
                    EXTRACT(HOUR FROM end_date)                                               as end_date,
                    eb.private,
                    er.rate
                FROM event_rate er
                        INNER JOIN event_musical eb ON er.event_type = eb.event_type AND er.event_id = eb.id
                WHERE user_id in (:user_id)
                ORDER BY random();
                """
        data_frame = pd.read_sql(query, engine, params={"user_id": user_id})
        return data_frame

    def getSportEventRatesUser(self, user_id):
        engine = create_engine(self.connection_string)
        query = """
                SELECT eb.category,
                    (CASE WHEN price IS NULL THEN true ELSE false END) as price,
                    EXTRACT(HOUR FROM start_date)                                             as start_date,
                    EXTRACT(HOUR FROM end_date)                                               as end_date,
                    eb.private,
                    er.rate
                FROM event_rate er
                        INNER JOIN event_sport eb ON er.event_type = eb.event_type AND er.event_id = eb.id
                WHERE user_id in (:user_id)
                ORDER BY random();
                """
        data_frame = pd.read_sql(query, engine, params={"user_id": user_id})
        return data_frame
    def getNatureEventRatesUser(self, user_id):
        engine = create_engine(self.connection_string)
        query = """
                SELECT eb.category,
                    (CASE WHEN price IS NULL THEN true ELSE false END) as price,
                    EXTRACT(HOUR FROM start_date)                                             as start_date,
                    EXTRACT(HOUR FROM end_date)                                               as end_date,
                    eb.private,
                    er.rate
                FROM event_rate er
                        INNER JOIN event_nature eb ON er.event_type = eb.event_type AND er.event_id = eb.id
                WHERE user_id in (:user_id)
                ORDER BY random();
                """
        data_frame = pd.read_sql(query, engine, params={"user_id": user_id})
        return data_frame
    def getStagePlayEventRatesUser(self, user_id):
        engine = create_engine(self.connection_string)
        query = """
                SELECT eb.category,
                    (CASE WHEN price IS NULL THEN true ELSE false END) as price,
                    EXTRACT(HOUR FROM start_date)                                             as start_date,
                    EXTRACT(HOUR FROM end_date)                                               as end_date,
                    eb.private,
                    er.rate
                FROM event_rate er
                        INNER JOIN event_stage_play eb ON er.event_type = eb.event_type AND er.event_id = eb.id
                WHERE user_id in (:user_id)
                ORDER BY random();
                """
        data_frame = pd.read_sql(query, engine, params={"user_id": user_id})
        return data_frame

    def getMusicalEventRates(self):
        engine = create_engine(self.connection_string)
        query = """
                SELECT eb.category,
                    (CASE WHEN price IS NULL THEN true ELSE false END) as price,
                    EXTRACT(HOUR FROM start_date)                                             as start_date,
                    EXTRACT(HOUR FROM end_date)                                               as end_date,
                    eb.private,
                    er.rate
                FROM event_rate er
                        INNER JOIN event_musical eb ON er.event_type = eb.event_type AND er.event_id = eb.id
                ORDER BY random()
                LIMIT 1500;
                """
        data_frame = pd.read_sql(query, engine)
        return data_frame
    def getSportEventRates(self):
        engine = create_engine(self.connection_string)
        query = """
                SELECT eb.category,
                    (CASE WHEN price IS NULL THEN true ELSE false END) as price,
                    EXTRACT(HOUR FROM start_date)                                             as start_date,
                    EXTRACT(HOUR FROM end_date)                                               as end_date,
                    eb.private,
                    er.rate
                FROM event_rate er
                        INNER JOIN event_sport eb ON er.event_type = eb.event_type AND er.event_id = eb.id
                ORDER BY random()
                LIMIT 1500;
                """
        data_frame = pd.read_sql(query, engine)
        return data_frame
    def getNatureEventRates(self):
        engine = create_engine(self.connection_string)
        query = """
                SELECT eb.category,
                    (CASE WHEN price IS NULL THEN true ELSE false END) as price,
                    EXTRACT(HOUR FROM start_date)                                             as start_date,
                    EXTRACT(HOUR FROM end_date)                                               as end_date,
                    eb.private,
                    er.rate
                FROM event_rate er
                        INNER JOIN event_nature eb ON er.event_type = eb.event_type AND er.event_id = eb.id
                ORDER BY random()
                LIMIT 1500;
                """
        data_frame = pd.read_sql(query, engine)
        return data_frame
    def getStagePlayEventRates(self):
        engine = create_engine(self.connection_string)
        query = """
                SELECT eb.category,
                    (CASE WHEN price IS NULL THEN true ELSE false END) as price,
                    EXTRACT(HOUR FROM start_date)                                             as start_date,
                    EXTRACT(HOUR FROM end_date)                                               as end_date,
                    eb.private,
                    er.rate
                FROM event_rate er
                        INNER JOIN event_stage_play eb ON er.event_type = eb.event_type AND er.event_id = eb.id
                ORDER BY random()
                LIMIT 1500;
                """
        data_frame = pd.read_sql(query, engine)
        return data_frame
    
    def getUpcomingMusicalEvents(self):
        engine = create_engine(self.connection_string)
        query = """
        select  id,
                event_type,
                category,
                (CASE WHEN price IS NULL THEN true ELSE false END) as price,
                EXTRACT(HOUR FROM start_date)                            as start_date,
                EXTRACT(HOUR FROM end_date)                              as end_date,
                private
        from event_musical
        where start_date > now();
        """
        data_frame = pd.read_sql(query, engine)
        return data_frame
    
    def getUpcomingSportEvents(self):
        engine = create_engine(self.connection_string)
        query = """
        select  id,
                event_type,
                category,
                (CASE WHEN price IS NULL THEN true ELSE false END) as price,
                EXTRACT(HOUR FROM start_date)                            as start_date,
                EXTRACT(HOUR FROM end_date)                              as end_date,
                private
        from event_sport
        where start_date > now();
        """
        data_frame = pd.read_sql(query, engine)
        return data_frame
    def getUpcomingNatureEvents(self):
        engine = create_engine(self.connection_string)
        query = """
        select  id,
                event_type,
                category,
                (CASE WHEN price IS NULL THEN true ELSE false END) as price,
                EXTRACT(HOUR FROM start_date)                            as start_date,
                EXTRACT(HOUR FROM end_date)                              as end_date,
                private
        from event_nature
        where start_date > now();
        """
        data_frame = pd.read_sql(query, engine)
        return data_frame
    def getUpcomingStagePlayEvents(self):
        engine = create_engine(self.connection_string)
        query = """
        select  id,
                event_type,
                category,
                (CASE WHEN price IS NULL THEN true ELSE false END) as price,
                EXTRACT(HOUR FROM start_date)                            as start_date,
                EXTRACT(HOUR FROM end_date)                              as end_date,
                private
        from event_stage_play
        where start_date > now();
        """
        data_frame = pd.read_sql(query, engine)
        return data_frame