# Déploiement sur Google Cloud Platform

__DISCLAIMER:__ Cette configuration à uniquement vocation à servie un CodeLab, elle n'est pas du tout viable pour une production.

## Introduction

Afin d'éviter à tous les participants d'avoir à:
* Télécharger et installer Ollama
* Récupérer un model depuis internet
* Télécharger et installer Chromadb

On propose de le dépoloyer et de le mutualiser sur un infrastructure cloud temporaire. 

Pour cela, nous allons: 
* Créer un bucket Google Cloud Storage permettant de stocker les modèles ollama
* Créer un bucket Google Cloud Storage permettant de stocker les index ChromaDB

## Création des buckets Google Cloud Storage

Pour initier les bukets GCS, vous pouvez exécuté la commande : 

```shell
make create-buckets LOCATION=us-east1 PROJECT_ID=my-projectid
```

Cette commande va lancer la création de deux buckets dans la région et le projet que vous aurez spécifié. 

## Déploiement des services

Pour simplifier les déploiements, on va se baser sur des images Docker pour le déploiement de Ollama ainsi que ChromaDB et nous allons utiliser le service CloudRun. 

Le déploiement de Ollama se fait en exécutant la commande: 

```shell
make deploy-ollama
```

Le déploiement de ChromaDB se fait en exécutant la commande: 

```shell
make deploy-chromadb
```

## Récupération des informations de connexion

Les services Ollama et ChromaDB sont accessible via une url. Ces urls peuvent être listés via la commande:

```shell
make info
```