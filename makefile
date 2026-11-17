dev_project="fcg-bi-dev"
dev_service_account="bi-dev-dataflow@fcg-bi-dev.iam.gserviceaccount.com"

prod_project="fcg-bi-prod"
prod_service_account="bi-prod-dataflow@fcg-bi-prod.iam.gserviceaccount.com"

function_name="bi-flow-parse-inspection-report-schema-files"
entry_point="parse_schema_files"
runtime="python37"
region="europe-west1"

# Note: removed --allow-unauthenticated command-line option from both commands

publish_funtion_to_dev:
	gcloud functions deploy ${function_name} --region ${region} \
	--entry-point ${entry_point} --runtime ${runtime} --trigger-http \
	--timeout 540 --memory 2048MB \
	--set-env-vars=IS_LOCAL=False,PROJECT_ID=${dev_project} \
	--service-account ${dev_service_account} --project ${dev_project}

publish_funtion_to_prod:
	gcloud functions deploy ${function_name} --region ${region} \
	--entry-point ${entry_point} --runtime ${runtime} --trigger-http \
	--timeout 540 --memory 2048MB \
	--set-env-vars=IS_LOCAL=False,PROJECT_ID=${prod_project} \
	--service-account ${prod_service_account} --project ${prod_project}