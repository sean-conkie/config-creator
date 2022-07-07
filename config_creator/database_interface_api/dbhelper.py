import os

from django.conf import settings
from google.cloud import bigquery
from lib.baseclasses import ConnectionType
from lib.helper import isnullorwhitespace
from pandas import DataFrame, read_csv


_all_ = ["get_schema", "get_database_schema"]


class IBQClient(bigquery.Client):
    def __init__(self, project: str) -> None:
        bigquery.Client.__init__(self, project)
        self._data = None
        self._query = None

    def get_data(self, query: str) -> DataFrame:
        """
        It takes a query string, runs it on the BigQuery service, and returns the results as a Pandas
        DataFrame.

        Args:
          query (str): The query to run.

        Returns:
          A dataframe
        """
        if isnullorwhitespace(query):
            raise ValueError("Parameter 'query' must be provided.")

        job = self.query(query)
        outp = job.result().to_dataframe()
        self._data = outp
        return outp

    @property
    def data(self) -> DataFrame:
        """
        The function data() returns the dataframe of the object

        Returns:
          The dataframe is being returned.
        """
        return self._data

    def to_json(self):
        """
        It takes the dataframe, iterates over the rows, and creates a dictionary for each row, where the
        keys are the column names and the values are the values in the row

        Returns:
          A dictionary with a key of "result" and a value of a list of dictionaries.
        """

        if not self._data is None:
            root = {"result": []}
            for i in self._data.index:
                row = self._data.iloc[i].to_list()
                row_obj = {}
                for i, c in enumerate(self._data.columns.values):
                    row_obj[c] = row[i]

                root["result"].append(row_obj)

            return root
        else:
            return {}


class CSVClient:
    def __init__(self, path: str) -> None:
        self._path = os.path.normpath(os.path.join(settings.MEDIA_ROOT, path))
        self._data = None

    @property
    def path(self) -> str:
        """
        Returns the path
        """
        return self._path

    @property
    def data(self) -> DataFrame:
        """
        The function data() returns the dataframe of the object

        Returns:
          The dataframe is being returned.
        """
        return self._data

    def get_data(self, query=None):
        if os.path.exists(self._path):

            outp = read_csv(
                self._path,
                names=[
                    "table_schema",
                    "table_name",
                    "column_name",
                    "data_type",
                    "ordinal_position",
                    "is_nullable",
                ],
            )

            if query == "schema":
                unique_schemas = outp.table_schema.unique().tolist()
                outp = DataFrame(unique_schemas, columns=["table_schema"])
            elif query:
                outp = outp[outp.table_schema == query]

            self._data = outp

            return outp
        else:
            return DataFrame([])

    def to_json(self):
        """
        It takes the dataframe, iterates over the rows, and creates a dictionary for each row, where the
        keys are the column names and the values are the values in the row

        Returns:
          A dictionary with a key of "result" and a value of a list of dictionaries.
        """

        if not self._data is None:
            root = {"result": []}
            for i in self._data.index:
                row = self._data.iloc[i].to_list()
                row_obj = {}
                for i, c in enumerate(self._data.columns.values):
                    row_obj[c] = row[i]

                root["result"].append(row_obj)

            return root
        else:
            return {}


def get_schema(
    connection: dict,
) -> dict:

    client = None
    query = None
    if connection.get("connection_type") == ConnectionType.BIGQUERY:
        client = IBQClient(connection.get("connection_string"))
        query = "select schema_name table_schema from `region-eu`.INFORMATION_SCHEMA.SCHEMATA order by 1"

    elif connection.get("connection_type") == ConnectionType.CSV:
        query = "schema"
        client = CSVClient(connection.get("schema").name)

    client.get_data(query).sort_values(by=["table_schema"])

    rs = client.to_json()

    outp = {
        "result": [
            {
                "name": r.get("table_schema"),
                "content": [],
                "type": "dataset",
                "connection_id": connection.get("id"),
            }
            for r in rs.get("result", [])
        ],
    }

    return outp


def get_database_schema(
    connection: dict,
    database: str,
) -> dict:

    client = None
    query = None
    if connection.get("connection_type") == ConnectionType.BIGQUERY:
        client = IBQClient(connection)
        query = f"select table_schema, table_name, column_name, data_type, ordinal_position, is_nullable from {connection}.`region-eu`.INFORMATION_SCHEMA.COLUMNS where table_schema = '{database}' order by 2, 5"

    elif connection.get("connection_type") == ConnectionType.CSV:
        query = database
        client = CSVClient(connection.get("schema").name)

    client.get_data(query).sort_values(by=["table_name", "ordinal_position"])
    tables = []
    for table in client.data["table_name"].unique():
        cols = [
            {
                "dataset": row["table_schema"],
                "table_name": row["table_name"],
                "column_name": row["column_name"],
                "data_type": row["data_type"],
                "ordinal_position": row["ordinal_position"],
                "is_nullable": True if row["is_nullable"] == "YES" else False,
                "type": "column",
                "connection_id": connection.get("id"),
            }
            for index, row in client.data[client.data.table_name.eq(table)].iterrows()
        ]

        tables.append(
            {
                "name": table,
                "dataset": client.data.iloc[0]["table_schema"],
                "content": cols,
                "type": "table",
                "connection_id": connection.get("id"),
            }
        )

    outp = {
        "result": tables,
    }

    return outp
