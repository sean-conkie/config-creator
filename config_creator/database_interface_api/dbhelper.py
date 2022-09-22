import os
import re

from .models import *
from core.models import Field, Job, JobTask, Join, SourceTable
from django.conf import settings
from django.db.models import Q
from google.cloud import bigquery
from lib.baseclasses import ConnectionType
from lib.helper import isnullorwhitespace
from pandas import DataFrame, read_csv, isna
from wordsegment import segment


__all__ = [
    "get_schema",
    "get_database_schema",
    "get_table",
]


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
                for j, c in enumerate(self._data.columns.values):
                    row_obj[c] = row[j]

                root["result"].append(row_obj)

            return root
        else:
            return {}


class CSVClient:
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


def get_schema(
    connection: dict,
    job_id: int = None,
    task_id: int = None,
    user_id: int = None,
) -> dict:

    client = None
    query = None
    if connection.get("connection_type") == ConnectionType.JOB:
        if task_id:
            job_id = JobTask.objects.get(id=task_id).job_id
        destination_datasets = []
        for task in JobTask.objects.filter(job_id=job_id):
            dataset = {
                "name": task.destination_dataset,
                "content": [],
                "type": "dataset",
                "connection_id": connection.get("id"),
                "connection_name": connection.get("name"),
            }

            if dataset not in destination_datasets:
                destination_datasets.append(dataset)

        return {"result": destination_datasets}

    elif connection.get("connection_type") == ConnectionType.LOCAL:
        # check if user has a connection with same project
        # if they do, create query and run it with source table filter
        # if they don't build the details from what has been committed
        connections = Connection.objects.filter(
            Q(connectionstring=connection.get("name")) | Q(name=connection.get("name")),
            user_id=user_id,
        )
        connection = None
        if connections.exists():
            user_connection = connections[0]
            connection_type = ConnectionType(user_connection.connectiontype.id)

            connection = {
                "id": 0,
                "name": user_connection.name,
                "credentials": user_connection.credentials,
                "connection_string": user_connection.connectionstring,
                "user_name": user_connection.user_name,
                "host": user_connection.host,
                "sid": user_connection.sid,
                "port": user_connection.port,
                "schema": user_connection.schema,
                "secret_key": user_connection.secret_key,
                "connection_type": connection_type,
            }

        task_datasets = [
            table.dataset_name
            for table in SourceTable.objects.filter(task_id=task_id)
            if table.source_project == connection.get("name")
        ]

        task_datasets.extend(
            [
                join.left_table.dataset_name
                for join in Join.objects.filter(task_id=task_id)
                if join.left_table.source_project == connection.get("name")
            ]
        )

        task_datasets.extend(
            [
                join.right_table.dataset_name
                for join in Join.objects.filter(task_id=task_id)
                if join.right_table.source_project == connection.get("name")
            ]
        )

        dataset_source = (
            JobTask.objects.select_related()
            .get(id=task_id)
            .job.get_property_object()
            .dataset_source
        )

        if dataset_source not in task_datasets:
            task_datasets.extend(dataset_source)

        if connection.get("connection_type") == ConnectionType.BIGQUERY:
            client = IBQClient(connection.get("connection_string"))
            dataset_condition = ",".join([f"'{c}'" for c in task_datasets])
            query = f"select schema_name table_schema from `region-eu`.INFORMATION_SCHEMA.SCHEMATA where schema_name in ({dataset_condition}) order by 1"
        elif connection.get("connection_type") == ConnectionType.CSV:
            query = "schema"
            client = CSVClient(
                connection.get("schema").name,
                schema_filter=task_datasets,
            )

        else:

            return {
                "result": [
                    {
                        "name": r,
                        "content": [],
                        "type": "dataset",
                        "connection_id": connection.get("id"),
                        "connection_name": connection.get("name"),
                    }
                    for r in task_datasets
                ],
            }

    elif connection.get("connection_type") == ConnectionType.BIGQUERY:
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
                "connection_name": connection.get("name"),
            }
            for r in rs.get("result", [])
        ],
    }

    return outp


def get_database_schema(
    connection: dict,
    database: str,
    job_id: int = None,
    task_id: int = None,
    user_id: int = None,
) -> dict:

    client = None
    query = None
    tables = []

    if connection.get("connection_type") == ConnectionType.JOB:
        if task_id:
            job_id = JobTask.objects.get(id=task_id).job_id

        tables = []
        for task in JobTask.objects.filter(job_id=job_id):
            if task.destination_dataset == database:

                cols = [
                    {
                        "dataset": database,
                        "table_name": task.destination_table,
                        "alias": "",
                        "raw_table_name": task.destination_table,
                        "column_name": field.name,
                        "target_name": "_".join([w for w in segment(field.name)]),
                        "data_type": field.data_type.name,
                        "ordinal_position": field.position,
                        "is_nullable": field.is_nullable,
                        "type": "column",
                        "connection_id": connection.get("id"),
                    }
                    for field in Field.objects.filter(
                        task_id=task.id,
                        is_source_to_target=True,
                    ).order_by("position")
                ]

                if len(cols) > 0:
                    tables.append(
                        {
                            "name": task.destination_table,
                            "dataset": database,
                            "content": cols,
                            "type": "table",
                            "connection_id": connection.get("id"),
                            "connection_name": Job.objects.get(id=job_id)
                            .get_property_object()
                            .target_project,
                        }
                    )

        return {
            "result": tables,
        }

    elif connection.get("connection_type") == ConnectionType.LOCAL:
        # check if user has a connection with same project
        # if they do, create query and run it with source table filter
        # if they don't build the details from what has been committed
        connections = Connection.objects.filter(
            Q(connectionstring=connection.get("name")) | Q(name=connection.get("name")),
            user_id=user_id,
        )
        connection = None
        if connections.exists():
            user_connection = connections[0]
            connection_type = ConnectionType(user_connection.connectiontype.id)

            connection = {
                "id": user_connection.id,
                "name": user_connection.name,
                "credentials": user_connection.credentials,
                "connection_string": user_connection.connectionstring,
                "user_name": user_connection.user_name,
                "host": user_connection.host,
                "sid": user_connection.sid,
                "port": user_connection.port,
                "schema": user_connection.schema,
                "secret_key": user_connection.secret_key,
                "connection_type": connection_type,
            }
        driving_table = JobTask.objects.select_related().get(id=task_id).driving_table
        tables = list(
            SourceTable.objects.filter(
                task_id=task_id,
                source_project=connection.get("name"),
                dataset_name=database,
            )
        )

        if connection.get("connection_type") == ConnectionType.BIGQUERY:

            task_tables = [
                f"select '{table.table_name}' table_name, '{table.alias}' alias "
                for table in tables
                if table.source_project == connection.get("name")
                and table.dataset_name == database
            ]

            if driving_table not in task_tables:
                task_tables.extend(
                    [f"select '{driving_table}' table_name, 'src' alias "]
                )

            client = IBQClient(connection.get("connection_string"))
            table_condition = " union all ".join(task_tables)
            query = f"select distinct s.table_schema, concat(s.table_name, ' ', st.alias) table_name, s.table_name raw_table_name, st.alias alias, s.column_name, s.data_type, s.ordinal_position, s.is_nullable from {connection.get('connection_string')}.{database}.INFORMATION_SCHEMA.COLUMNS s inner join ({table_condition}) st on s.table_name = st.table_name order by 2, 5"

        elif connection.get("connection_type") == ConnectionType.CSV:

            task_datasets = [
                table.dataset_name
                for table in SourceTable.objects.filter(task_id=task_id)
                if table.source_project == connection.get("name")
            ]

            dataset_source = (
                JobTask.objects.select_related()
                .get(id=task_id)
                .job.get_property_object()
                .dataset_source
            )

            if dataset_source not in task_datasets:
                task_datasets.extend(dataset_source)

            task_tables = {"table_name": [], "alias": []}
            for table in tables:
                if (
                    table.source_project == connection.get("name")
                    or table.source_project is None
                ):
                    task_tables["table_name"].append(table.table_name)
                    task_tables["alias"].append(table.alias)

            client = CSVClient(
                connection.get("schema").name,
                schema_filter=task_datasets,
                table_filter=task_tables,
            )

            query = {
                "database": database,
            }

        else:

            return {
                "result": [
                    {
                        "dataset": database,
                        "table_name": r,
                        "column_name": None,
                        "data_type": None,
                        "ordinal_position": None,
                        "is_nullable": None,
                        "type": "column",
                        "connection_id": connection.get("id"),
                        "connection_name": Job.objects.get(id=job_id)
                        .get_property_object()
                        .target_project,
                    }
                    for r in task_tables
                ],
            }

    elif connection.get("connection_type") == ConnectionType.BIGQUERY:
        client = IBQClient(connection.get("connection_string"))
        query = f"select table_schema, table_name, table_name raw_table_name, null alias, column_name, data_type, ordinal_position, is_nullable from {connection.get('connection_string')}.{database}.INFORMATION_SCHEMA.COLUMNS order by 2, 5"

    elif connection.get("connection_type") == ConnectionType.CSV:
        query = {
            "database": database,
        }
        client = CSVClient(connection.get("schema").name)

    client.get_data(query).sort_values(by=["table_name", "ordinal_position"])
    outp_tables = []
    for table in client.data["table_name"].unique():
        cols = [
            {
                "dataset": row["table_schema"].lower(),
                "table_name": row["table_name"].lower(),
                "alias": None if isna(row["alias"]) else row["alias"].lower(),
                "raw_table_name": row["table_name"].lower()
                if row["raw_table_name"] is None
                else row["raw_table_name"].lower(),
                "column_name": row["column_name"].lower(),
                "target_name": "_".join([w for w in segment(row["column_name"])]),
                "data_type": row["data_type"].lower(),
                "ordinal_position": row["ordinal_position"],
                "is_nullable": True if row["is_nullable"] == "YES" else False,
                "type": "column",
                "connection_id": connection.get("id"),
            }
            for index, row in client.data[client.data.table_name.eq(table)]
            .sort_values(by=["table_name", "ordinal_position"])
            .iterrows()
        ]

        outp_tables.append(
            {
                "name": table,
                "dataset": client.data.iloc[0]["table_schema"],
                "content": cols,
                "type": "table",
                "connection_id": connection.get("id"),
                "connection_name": connection.get("name"),

            }
        )

    # check tables, it will be populated if local data
    # is being searched, if any table is missing add it.

    job_tasks = (
        JobTask.objects.filter(
            ~Q(id=task_id),
            job_id=JobTask.objects.get(id=task_id).job_id,
        )
        if task_id
        else []
    )
    for table in tables:
        if table.source_project == connection.get("name"):

            task = None
            table_to_check = None
            for t in job_tasks:
                if table.table_name == t.destination_table:
                    task = t
                    break

            if task:

                cols = [
                    {
                        "dataset": table.dataset_name,
                        "table_name": f"{table.table_name} {table.alias}",
                        "alias": table.alias,
                        "raw_table_name": table.table_name,
                        "column_name": field.name,
                        "target_name": "_".join([w for w in segment(field.name)]),
                        "data_type": field.data_type.name,
                        "ordinal_position": field.position,
                        "is_nullable": field.is_nullable,
                        "type": "column",
                        "connection_id": connection.get("id"),
                    }
                    for field in Field.objects.filter(
                        task_id=t.id,
                        is_source_to_target=True,
                    ).order_by("position")
                ]

                table_to_check = {
                    "name": f"{table.table_name} {table.alias}"
                    if table.alias
                    else table.table_name,
                    "dataset": table.dataset_name,
                    "content": cols,
                    "type": "table",
                    "connection_id": connection.get("id"),
                }

            if table_to_check and not table_to_check in outp_tables:
                outp_tables.append(table_to_check)

    outp = {
        "result": outp_tables,
    }

    return outp


def get_table(
    connection: dict,
    database: str,
    table_name: str,
    task_id: int = None,
) -> dict:

    client = None
    query = None

    m = re.search(
        r"^\b(?P<table_name>[a-z_-]+)\b(?:\s(?P<alias>[a-z_-]+))?",
        table_name,
        re.IGNORECASE,
    )
    cleansed_table_name = m.group("table_name")
    alias = m.group("alias") if m.group("alias") else table_name

    if connection.get("connection_type") == ConnectionType.JOB:
        job_id = JobTask.objects.get(id=task_id).job_id

        for task in JobTask.objects.filter(job_id=job_id):
            if (
                task.destination_table == cleansed_table_name
                and task.write_disposition != 4
            ):

                cols = [
                    {
                        "dataset": database,
                        "table_name": task.destination_table,
                        "alias": "",
                        "raw_table_name": task.destination_table,
                        "column_name": field.name,
                        "target_name": "_".join([w for w in segment(field.name)]),
                        "data_type": field.data_type.name,
                        "ordinal_position": field.position,
                        "is_nullable": field.is_nullable,
                        "is_primary_key": field.is_primary_key,
                        "type": "column",
                        "connection_id": connection.get("id"),
                    }
                    for field in Field.objects.filter(
                        task_id=task.id,
                        is_source_to_target=True,
                    ).order_by("position")
                ]

                if len(cols) > 0:
                    table = {
                        "result": {
                            "name": task.destination_table,
                            "dataset": database,
                            "content": cols,
                            "type": "table",
                            "connection_id": connection.get("id"),
                        }
                    }

                    return table

    elif connection.get("connection_type") == ConnectionType.BIGQUERY:
        client = IBQClient(connection.get("connection_string"))
        query = f"select table_schema, table_name, column_name, data_type, ordinal_position, is_nullable from {connection.get('connection_string')}.{database}.INFORMATION_SCHEMA.COLUMNS where table_name = '{cleansed_table_name}' order by 2, 5"

    elif connection.get("connection_type") == ConnectionType.CSV:
        query = {
            "database": database,
            "table_name": table_name,
        }
        client = CSVClient(connection.get("schema").name)

    client.get_data(query).sort_values(by=["table_name", "ordinal_position"])

    cols = [
        {
            "dataset": row["table_schema"],
            "table_name": row["table_name"],
            "alias": alias,
            "column_name": row["column_name"],
            "target_name": "_".join([w for w in segment(row["column_name"])]),
            "data_type": row["data_type"],
            "ordinal_position": row["ordinal_position"],
            "is_nullable": True if row["is_nullable"] == "YES" else False,
            "type": "column",
            "connection_id": connection.get("id"),
        }
        for index, row in client.data.iterrows()
    ]

    outp = {
        "result": {
            "name": table_name,
            "dataset": database,
            "content": cols,
            "type": "table",
            "connection_id": connection.get("id"),
        },
    }

    return outp
