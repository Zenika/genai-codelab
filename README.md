# CodeLab GenAI Zenika 

Bienvenue dans ce CodeLab autour de la GenAI.

## L'objectif

Developper une application permettant d'appeler des LLM (Large Language Model) customizer.

## Les technos

Pour ce CodeLab, nous allons principalement utiliser deux librairies / programmes:

- [Ollama](https://ollama.com/) : Permet de faire des inférences sur un modèle en local
- [LangChain](https://www.langchain.com/) : Framework permettant de construire des applications basé sur des LLM

Côté modèle, nous allons utiliser [Mistral 7B](https://mistral.ai/) un modèle générique de génération de texte.

Le CodeLab peut être réalisé dans différents langages: 

- [Python](./python/README.md)
- [Java](./java/README.md)
- [Javascript](./js/README.md)

Afin de simplifier le déploiement pour les participants, il est possible de déployer Ollama et ChromaDB sur le cloud.
Tout est décrit [ici](./deployment/README.md)

## Pré-requis matériel

En fonction de la taille du modèle choisit, une certaine configuration mémoire est requise:
* Pour un modèlé à 7 milliards de paramètres (7B) : 8Go de RAM
* Pour un modèlé à 13 milliards de paramètres (13B) : 16Go de RAM
* Pour un modèlé à 70 milliards de paramètres (70B) : 64Go de RAM


## Installation 

Afin de pouvoir faire des inférences en local, il est nécéssaire :

- Installer [Ollama](https://ollama.com/download)
- De récupérer un modèle depuis la librairie : https://ollama.com/library
- Pour les Tps, nous allons nous baser sur le modèle `openhermes`

Pour télécharger un modèle, cela peut être fait de deux façon: 

- En ligne de commande: `ollama pull openhermes`
- Via l'API: `curl -XPOST http://localhost:11434/api/pull -d '{"name": "openhermes"}'`
