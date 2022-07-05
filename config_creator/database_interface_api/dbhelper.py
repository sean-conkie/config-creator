from google.cloud import bigquery
from lib.baseclasses import ConnectionType
from lib.helper import isnullorwhitespace
from pandas import DataFrame


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


def get_schema(
    connection_id: int,
    connection: str,
    connection_type: ConnectionType,
) -> dict:
    """
    > This function returns a list of schemas for a given connection

    Args:
      connection (str): The connection string to the database.
      connection_type (ConnectionType): Type of connection

    Returns:
      A list of dictionaries with the connection name and an empty list of schemas.
    """

    client = None
    query = None
    if connection_type == ConnectionType.BIGQUERY:
        client = IBQClient(connection)
        query = (
            "select schema_name from `region-eu`.INFORMATION_SCHEMA.SCHEMATA order by 1"
        )

    client.get_data(query).sort_values(by=["schema_name"])

    rs = client.to_json()

    outp = {
        "result": [
            {
                "name": r.get("schema_name"),
                "content": [],
                "type": "dataset",
                "connection_id": connection_id,
            }
            for r in rs.get("result", [])
        ],
    }

    return outp


def get_database_schema(
    connection_id: int,
    connection: str,
    connection_type: ConnectionType,
    database: str,
) -> dict:
    """
    > This function takes a connection string, connection type and database name as input and returns a
    dictionary containing the schema of the database

    Args:
      connection (str): The connection string to the database.
      connection_type (ConnectionType): Type of connection
      database (str): the name of the database you want to get the schema for

    Returns:
      A dictionary with the database name as the key and a list of tables as the value.
    """

    client = None
    query = None
    if connection_type == ConnectionType.BIGQUERY:
        client = IBQClient(connection)
        query = f"select table_schema, table_name, column_name, data_type, ordinal_position, is_nullable from {connection}.`region-eu`.INFORMATION_SCHEMA.COLUMNS where table_schema = '{database}' order by 2, 5"

    client.get_data(query).sort_values(by=["table_name", "ordinal_position"])
    tables = []
    for table in client.data["table_name"].unique():
        cols = [
            {
                "dataset": client.data.iloc[r]["table_schema"],
                "table_name": client.data.iloc[r]["table_name"],
                "column_name": client.data.iloc[r]["column_name"],
                "data_type": client.data.iloc[r]["data_type"],
                "ordinal_position": client.data.iloc[r]["ordinal_position"],
                "is_nullable": True
                if client.data.iloc[r]["is_nullable"] == "YES"
                else False,
                "type": "column",
                "connection_id": connection_id,
            }
            for r in client.data[client.data.table_name.eq(table)].index.to_list()
        ]

        tables.append(
            {
                "name": table,
                "dataset": client.data.iloc[0]["table_schema"],
                "content": cols,
                "type": "table",
                "connection_id": connection_id,
            }
        )

    outp = {
        "result": tables,
    }

    return outp
