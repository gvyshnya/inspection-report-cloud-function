from google.oauth2 import service_account
from google.cloud import storage

from typing import Dict

from flask import Flask, request, Response

import os
import json
import objectpath
import pandas as pd

JSON_REPORT_BUCKET_NAME = 'inspection_report_schema_files'

inspection_report_schema_info_csv = 'report_schema_info.csv'

inspection_report_field_token = 'inspection.field'

col_names = ['schema_name', 'fields_number']

write_to_local = False

gcp_project = os.environ.get("PROJECT_ID", "fcg-bi-dev")

app = Flask(__name__)


def get_number_of_inspection_report_fields(json_data):
    tree_obj = objectpath.Tree(json_data)

    field_nodes = tree_obj.execute('$..title')
    report_field_count = 0

    for node in field_nodes:
        if inspection_report_field_token in node:
            report_field_count += 1

    return report_field_count


@app.route("/", methods=["POST"])
def parse_schema_files(request: request):
    final_df = pd.DataFrame(columns=col_names)

    client = storage.Client()

    bucket = client.get_bucket(JSON_REPORT_BUCKET_NAME)

    blobs = bucket.list_blobs(prefix='report')
    for blob in blobs:
        json_file_name = blob.name
        if json_file_name.endswith('.json'):
            # read the inspection report schema file from GCS bucket
            data = json.loads(blob.download_as_string(client=None))

            report_field_count = get_number_of_inspection_report_fields(data)
            tokens = json_file_name.split(".")
            schema_name = tokens[0].strip()  # get the file name without extensions as a schema_name
            element_list = [[schema_name, report_field_count]]
            if final_df.shape[0] < 1:
                final_df = pd.DataFrame(data=element_list, columns=col_names)
            else:
                element_df = pd.DataFrame(data=element_list, columns=col_names)
                # concatenate
                frames = [final_df, element_df]
                final_df = pd.concat(frames)
    final_df.to_gbq('semantics_central.InspectionReportSchemas',
        gcp_project,
        chunksize=None,
        if_exists='replace'
    )
    print("Completed successfully")
