import os
import re

from .models import *
from core.models import (
    BigQueryDataType,
    Field,
    Job,
    JobTask,
    Join,
    SourceTable,
    TaskType,
)
from django.conf import settings
from django.db import connection as dj_conn
from django.db.models import Q
from django.db.models.query import QuerySet
from google.cloud import bigquery
from lib.helper import ifnull, isnullorwhitespace
from pandas import DataFrame, read_csv
from wordsegment import segment


__all__ = [
    "IBQClient",
    "CSVClient",
    "AppClient",
    "get_schema",
    "get_database_schema",
    "get_table",
]


class IBQClient(bigquery.Client):
    # Class for querying BigQuery INFORMATION_SCHEMA
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
                for j, c in enumerate(self._data.columns.values):
                    row_obj[c] = row[j]

                root["result"].append(row_obj)

            return root
        else:
            return {}


class CSVClient:
    # Class for returning data from CSV schema file.
    def __init__(
        self,
        path: str,
        schema_filter: list[str] = None,
        table_filter: dict = None,
    ) -> None:
        self._path = os.path.normpath(os.path.join(settings.MEDIA_ROOT, path))
        self._schema_filter = schema_filter
        if table_filter:
            self._table_filter = DataFrame(
                data=table_filter,
            )
        else:
            self._table_filter = None
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

    def get_data(self, query: str = None) -> DataFrame:
        """
        It reads a csv file, filters it based on the schema and table filters, and returns the filtered
        dataframe

        Args:
          query (str): str = None

        Returns:
          A dataframe with the following columns:
            table_schema
            table_name
            column_name
            data_type
            ordinal_position
            is_nullable
            alias
            raw_table_name
        """
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

            if self._table_filter is not None:
                outp = outp.join(
                    self._table_filter.set_index("table_name"),
                    how="inner",
                    on="table_name",
                )
                outp["raw_table_name"] = outp["table_name"]
                # outp.rename(columns={""})
                outp["table_name"] = outp["table_name"] + " " + outp["alias"]
            elif self._schema_filter:
                outp = outp[outp["table_schema"].isin(self._schema_filter)]

            if not "alias" in outp.columns:
                outp["alias"] = [None for r in range(0, len(outp))]

            if not "raw_table_name" in outp.columns:
                outp["raw_table_name"] = outp["table_name"]

            if query == "schema":
                unique_schemas = outp.table_schema.unique().tolist()
                outp = DataFrame(unique_schemas, columns=["table_schema"])
            elif query == "localschema":
                unique_schemas = outp.table_schema.unique().tolist()
                outp = DataFrame(unique_schemas, columns=["table_schema"])

            elif "table_name" in query.keys():
                outp = outp[
                    (outp.table_schema == query.get("database"))
                    & (outp.table_name == query.get("table_name"))
                ]
            elif query:
                outp = outp[outp.table_schema == query.get("database")]

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
                for j, c in enumerate(self._data.columns.values):
                    row_obj[c] = row[j]

                root["result"].append(row_obj)

            return root
        else:
            return {}


class AppClient(object):
    def __init__(
        self,
        connection: Connection,
        dataset_name: str = None,
        job_id: int = None,
        task_id: int = None,
    ) -> None:
        self._connection = connection
        self._dataset = (
            Dataset.objects.get(connection__name=connection.name, name=dataset_name)
            if dataset_name
            else None
        )
        self._job_id = job_id
        self._task_id = task_id

    @property
    def data(self) -> DataFrame:
        """
        The function data() returns the dataframe of the object

        Returns:
          The dataframe is being returned.
        """
        return self._data

    def get_data(self, query: str = None) -> DataFrame:
        """
        > The function returns a pandas DataFrame of the columns in the dataset

        Args:
          query (str): The query to run.

        Returns:
          A DataFrame object
        """

        dataset_cols = ["id", "connection_id", "table_schema"]
        table_cols = [
            "table_schema",
            "table_name",
            "raw_table_name",
            "alias",
            "column_name",
            "data_type",
            "ordinal_position",
            "is_nullable",
        ]
        qs = []
        if self._job_id and query:
            qs = _tasks_to_destination_table(
                JobTask.objects.filter(
                    ~Q(type=TaskType.objects.get(name="Truncate Table")),
                    job_id=self._job_id,
                    destination_table=query,
                )
            )

            dfcols = table_cols
        elif self._job_id and self._dataset:
            qs = _tasks_to_destination_table(
                JobTask.objects.filter(
                    ~Q(type=TaskType.objects.get(name="Truncate Table")),
                    job_id=self._job_id,
                    destination_dataset=self._dataset.name,
                )
            )

            dfcols = table_cols

        elif self._job_id:

            qs = _tasks_to_destination_dataset(
                JobTask.objects.filter(
                    job_id=self._job_id,
                ),
                self._connection,
            )

            dfcols = dataset_cols

        elif self._task_id and self._dataset:
            qs = _tasks_to_source_table(
                JobTask.objects.filter(
                    id=self._task_id,
                ),
                self._connection,
                self._dataset,
                query,
            )

            dfcols = table_cols

        elif self._task_id:

            qs = _tasks_to_source_dataset(
                JobTask.objects.filter(
                    id=self._task_id,
                ),
                self._connection,
            )

            dfcols = dataset_cols

        elif query:
            qs = _columns_to_source_table(
                self._dataset,
                query,
            )

            dfcols = table_cols
        elif self._dataset:
            # qs = _columns_to_source_table(
            #     self._dataset,
            # )
            qs = [
                {
                    "table_schema": self._dataset.name,
                    "table_name": t.name,
                    "raw_table_name": t.name,
                    "alias": None,
                    "column_name": None,
                    "data_type": None,
                    "ordinal_position": None,
                    "is_nullable": None,
                }
                for t in Table.objects.select_related().filter(dataset=self._dataset)
            ]

            dfcols = table_cols
        else:
            qs = _datasets_to_source_dataset(
                Dataset.objects.select_related().filter(connection=self._connection),
            )
            dfcols = dataset_cols

        if len(qs) == 0:
            outp = DataFrame(columns=dfcols)

        outp = DataFrame(qs, columns=dfcols)
        self._data = outp
        return outp

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
                for j, c in enumerate(self._data.columns.values):
                    row_obj[c] = row[j]

                root["result"].append(row_obj)

            return root
        else:
            return {}


def get_schema(
    connection: Connection,
    client: object,
    query: str = None,
) -> dict:

    """
    > This function returns a list of dictionaries, each containing the name of a schema and a list of
    tables in that schema

    Args:
      connection (Connection): Connection
      client (object): The client object that you created in the previous step.
      query (str): The query to run.

    Returns:
      A list of dictionaries.
    """

    client.get_data(query).sort_values(by=["table_schema"])

    rs = client.to_json()

    outp = {
        "result": [
            {
                "name": r.get("table_schema"),
                "content": [],
                "type": "dataset",
                "connection_id": connection.id,
                "connection_name": connection.name,
            }
            for r in rs.get("result", [])
        ],
    }

    return outp


def get_database_schema(
    connection: Connection,
    client: object,
    query: int = None,
) -> dict:

    tables = []

    client.get_data(query).sort_values(by=["table_name", "ordinal_position"])
    outp_tables = []
    for table in client.data["table_name"].unique():
        cols = [
            {
                "dataset": ifnull(row.get("table_schema"), "").lower(),
                "table_name": ifnull(row.get("table_name"), "").lower(),
                "alias": ifnull(row.get("alias"), "").lower(),
                "raw_table_name": ifnull(
                    row.get("raw_table_name", "table_name"), ""
                ).lower(),
                "column_name": ifnull(row.get("column_name"), "").lower(),
                "target_name": "_".join(
                    [w for w in segment(ifnull(row.get("column_name"), ""))]
                ),
                "data_type": ifnull(row.get("data_type"), "").lower(),
                "ordinal_position": ifnull(str(row.get("ordinal_position")), ""),
                "is_nullable": True
                if ifnull(row.get("is_nullable"), "") == "YES"
                else False,
                "type": "column",
                "connection_id": connection.id,
            }
            for index, row in client.data[client.data.table_name.eq(table)]
            .sort_values(by=["table_name", "ordinal_position"])
            .iterrows()
            if ifnull(row.get("column_name"), "") != ""
        ]

        table_outp = {
            "name": table,
            "dataset": client.data.iloc[0]["table_schema"],
            "type": "table",
            "connection_id": connection.id,
            "connection_name": connection.name,
        }

        if len(cols) > 0:
            table_outp["content"] = cols

        outp_tables.append(table_outp)

    outp = {
        "result": outp_tables,
    }

    return outp


def _tasks_to_destination_dataset(
    tasks: QuerySet,
    connection: Connection,
) -> list:
    """
    It takes a list of tasks and a connection, and returns a list of dictionaries with the connection id
    and table schema for each task

    Args:
      tasks (QuerySet): QuerySet
      connection (Connection): The connection object that you want to use to run the query.

    Returns:
      A list of dictionaries.
    """
    qs = list(
        {
            f"{d['connection_id']}-{d['table_schema']}": d
            for d in [
                {
                    "id": t.id,
                    "table_schema": t.destination_dataset,
                    "connection_id": connection.id,
                }
                for t in tasks
            ]
        }.values()
    )

    return qs


def _tasks_to_source_dataset(
    tasks: QuerySet,
    connection: Connection,
) -> list:
    """
    > It takes a list of tasks and a connection, and returns a list of source datasets

    Args:
      tasks (QuerySet): QuerySet
      connection (Connection): The connection to the database
    """

    qs = []

    for t in tasks:
        for st in SourceTable.objects.filter(task_id=t.id):
            if st.source_project == connection.name:
                qs.append(
                    {
                        "id": st.id,
                        "table_schema": st.dataset_name,
                        "connection_id": connection.id,
                    }
                )

    outp = list({f"{d['connection_id']}-{d['table_schema']}": d for d in qs}.values())

    return outp


def _datasets_to_source_dataset(datasets: QuerySet) -> list:

    qs = []

    for d in datasets:
        qs.append(
            {
                "id": d.id,
                "table_schema": d.name,
                "connection_id": d.connection.id,
            }
        )

    outp = list({f"{d['connection_id']}-{d['table_schema']}": d for d in qs}.values())

    return outp


def _tasks_to_destination_table(tasks: QuerySet) -> list:
    """
    It takes a list of tasks and returns a list of dictionaries that represent the columns of the tables
    that the tasks are loading

    Args:
      tasks (QuerySet): QuerySet

    Returns:
      A list of dictionaries.
    """
    qs = []

    for t in tasks:
        for c in (
            Field.objects.select_related()
            .filter(task_id=t.id, is_source_to_target=True)
            .order_by("position")
        ):
            qs.append(
                {
                    "table_schema": t.destination_dataset,
                    "table_name": t.destination_table,
                    "raw_table_name": t.destination_table,
                    "alias": None,
                    "column_name": c.name,
                    "data_type": c.data_type.name,
                    "ordinal_position": c.position,
                    "is_nullable": "YES" if c.is_nullable else "NO",
                }
            )

    return qs


def _columns_to_source_table(
    dataset: str,
    table: str = None,
) -> list:
    """
    It takes a dataset and table name, and returns a list of dictionaries, each of which contains the
    column name, data type, and source table for each column in the dataset

    Args:
      dataset (str): The name of the dataset you want to query.
      table (str): The name of the table in the dataset.

    Returns:
      A list of dictionaries.
    """
    where = (
        f"table_schema = '{dataset.name}' and raw_table_name = '{table}'"
        if table
        else f"table_schema = '{dataset.name}'"
    )
    query = f"select distinct * from database_interface_api_column_view where {where} order by table_name, ordinal_position"

    with dj_conn.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        qs = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return qs


def _tasks_to_source_table(
    tasks: QuerySet,
    connection: Connection,
    dataset: str = None,
    query: str = None,
) -> list:
    """
    It takes a list of tasks, a connection and a dataset and returns a list of dictionaries containing
    the data from the source tables used by the tasks

    Args:
      tasks (QuerySet): QuerySet
      connection (Connection): The connection to the database
      dataset (str): The dataset that the table is in.
      query (str): The name of the table you want to preview.

    Returns:
      A list of dictionaries.
    """

    qs = []
    is_query_empty = False if query else True

    for t in tasks:
        for st in SourceTable.objects.filter(task_id=t.id):
            query = st.table_name if is_query_empty else query
            # for each table used by the task, check that it's source project
            # matches the connection selected, that the dataset matches the dataset
            # selected, that the table_name matches the name selected (if any) and
            # that the table is not the tasks target table
            if (
                st.source_project == connection.name
                and (dataset.name == st.dataset_name or dataset is None)
                and (query == st.table_name)
                and st.alias != "trg"
            ):
                rs = AppClient(connection, dataset).get_data(query).to_dict("records")
                for r in rs:
                    r["alias"] = st.alias
                    r["table_name"] = f"{r['raw_table_name']} {st.alias}"

                qs.extend(rs)

    return qs
