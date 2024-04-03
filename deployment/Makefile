.PHONY: info

LOCATION=us-east1

info:
	gcloud run services describe ollama --region=$(LOCATION) --format='value(status.url)' --project=$(PROJECT_ID)
	gcloud run services describe chromadb --region=$(LOCATION) --format='value(status.url)' --project=$(PROJECT_ID)

init: create-buckets deploy
	
deploy: deploy-olloma deploy-chromadb

create-buckets:
	-gcloud storage buckets create gs://chroma-local-data --location=$(LOCATION) --project=$(PROJECT_ID) 
	-gcloud storage buckets create gs://ollama-local-models --location=$(LOCATION) --project=$(PROJECT_ID) 

deploy-ollama:
	-gcloud run services replace ./cloudrun-ollama.yml --region=$(LOCATION) --project=$(PROJECT_ID)

deploy-chromadb:
	-gcloud run services replace ./cloudrun-chromadb.yml --region=$(LOCATION) --project=$(PROJECT_ID)

pull:
	gcloud run services describe ollama --region=$(PROJECT_ID) --format='value(status.url)' --project=$(PROJECT_ID)