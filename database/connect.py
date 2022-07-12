import re

from sqlalchemy import create_engine, event, schema
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from config import DB_URI

DEFAULT_SCHEMA = 'collisions'

class ConnectDb:

    def __init__(self):

        self.DB_URI = DB_URI
        self.schema_name = DEFAULT_SCHEMA
        self.engine = create_engine(
            self.DB_URI,
            # executemany_mode='values_plus_batch',
            executemany_mode='values',
            executemany_values_page_size=10_000,
            executemany_batch_page_size=500,
            connect_args={
                "options": "-c timezone=utc"
            }
        )

        # initialize this as null
        self._session = None

        # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
        # Set up default configs here:
        self.autoflush = False
        self.expire_on_commit = False
        # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -


        # ----------------------------------------------------------------------
        # SOME REALLY USEFUL TESTS
        # If the db doesn't exist
        try:
            self.engine.connect()

        except OperationalError:

            # Do some fancy regex to get the db uri without the db
            pattern = re.compile(r'(?P<port>[0-9]{4})\/(?P<db>.*$)')
            tmp_DB_URI = pattern.sub('\g<port>', self.DB_URI)

            # Also get the db name
            tmp_DATABASE_NAME = pattern.search(self.DB_URI).group('db')

            # Create your engine and try to create the db
            tmp_engine = create_engine(tmp_DB_URI)


            try:
                with tmp_engine.connect() as conn:
                    conn.execute("commit")
                    conn.execute(f'CREATE DATABASE {tmp_DATABASE_NAME}')
                    conn.close()

            except Exception as db_exc:
                print(db_exc)

        # If the schema doesn't exist:
        if not self.engine.dialect.has_schema(self.engine, self.schema_name):
            self.engine.execute(schema.CreateSchema(self.schema_name))


    # --------------------------------------------------------------------------

    # Use engine connection instead of session
    @property
    def conn(self):
        """
        Use engine connection instead of session

        Example
        -------
        ```python
        with self.conn as conn:
            result = connection.execute(text("select * from users"))
        ```
        """
        return self.engine.connect()


    @property
    def batch_conn(self):
        """
        Create a psycopg engine to transact with bulk statements

        Use as follows
        -----
        ```python3
        all_url_content = [dict(url=key, html=value) for key, value in results.items()]

        with self.sm.connect() as conn:
            conn.execute(insert(UrlContent), all_url_content)
        ```
        """

        return self.batch_engine.connect()


    @property
    def session(self):
        """
        Lazy load a session. The session doesn't exist until the `self.session` command is called.

        To access the "main session" execute the following:
        >> session = self.session

        To create a new session (useful for multiprocessing):
        >> session = self._create_session()

        ----
        For more details on sessions, read here: https://docs.sqlalchemy.org/en/13/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it
        """
        if not self._session:
            self._session = self._create_session()

        return self._session


    def _create_session(self, batch=False, **kwargs):
        """
        This command explicitly creates a new session by calling the sessionmaker.
            ... Synonymous with `sessionmaker(bind=self.engine)`

        NOTE: Use carefully.
        """

        kwargs['autoflush'] = kwargs.get('autoflush', self.autoflush)
        kwargs['expire_on_commit'] = kwargs.get('expire_on_commit', self.expire_on_commit)

        return sessionmaker(bind=self.engine, **kwargs)()

    # --------------------------------------------------------------------------
    
