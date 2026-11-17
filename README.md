# Inspection Report Cloud Function

Inspection Report Schema Processing Cloud Function is the cloud-based serverless version of the business logic in the scripts implemented in ABC's Inspection Report Parsing tool.

**Note:** The cloud function displayed the long running cycles in production, exceeding the maximal cap of 540 s to run. Therefore, this function won't work in production, and the respective logic will be re-packed as an Airflow DAG script.