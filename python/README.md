# CodeLab GenAI Zenika - Python


## Installation

Pour lancer ce projet vous avez besoin:

- Python 3.9+
- Poetry

Une fois les outils installer, vous pouvez installer les dépendances via la commande: 

````bash
poetry install
````

Le suite du codelab aura lieu dans `src/app.py`


Assurez-vous également que `Ollama` est démarrer, accessible et que le modèle Mistral7B est bien disponible.
Pour cela vous pouvez accéder à l'URL suivante: (http://localhost:11434/api/tags)[http://localhost:11434/api/tags] et valider que Mistral est bien présent.

## Premier pas

Maintenant que tout est installé, nous allons pouvoir démarrer notre première application. 

Afin d'appeler notre modèle, nous allons utiliser (LangChain)[https://www.langchain.com/]. 

LangChain Community contient les intégrations pour les applications tierce comme Ollama.

Dans votre fichier `src/app.py`, vous pouvez ajouter l'import suivant :

```python
from langchain_community.llms import ollama
```

Notre modèle est actuellement accessible via l'URL `http://localhost:11434`

Nous allons créer l'objet permettant d'intéragir avec Ollama via le code suivant: 

```python
llm = ollama.Ollama(
    base_url=OLLAMA_URL, 
    model='mistral',
)
```

Une fois cet objet créé nous allons pouvoir intéragir avec le modèle mistral. 
Pour cela on déclare un prompt: 

```python
prompt = 'Who are you ?'
```

Puis on invoque le modèle :

```python
response = llm.invoke(prompt)
print(response)
```

Pour exécuter le fichier, exécuter la commande suivante: 

```python
poetry run python src/app.py
```

Et voila! Nous avons effectué notre premier appel. 

## Améliorons notre modèle

LangChain fournit un ensemble de fonction et d'utilitaire permettant de configurer plus finenement notre application. 

### Streaming 

Dans un premier temps, rendons notre application un peu plus vivante. Plutôt que de générer une réponse d'un coup, LangChain nous permet de streamer le flux de la réponse.

Pour cela, ajouter les imports suivants:

```python
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
```

Modifier la création de notre objet `llm` pour y ajouter un `callback_manager` permettant de streamer la réponse:

```python
llm = ollama.Ollama(
    base_url=OLLAMA_URL, 
    model='mistral',
    callback_manager= CallbackManager([StreamingStdOutCallbackHandler()])
)
```

Réexecuter le fichier pour voir la différence:

```python
poetry run python src/app.py
```

### Temperature 

Afin de limiter les hallucinations des modèles, il est possible de faire varier le paramètre `temperature`. 
Ce paramètre (compris entre 0 et 1) permet de définir la "créativité" du modèle. 
Plus la valeur est proche de 1, plus le modèle va pouvoir halluciner.
Plus la valeur est proche de 0, plus le modèle va être déterministe.

Pour configurer la temperature, modifier la déclaration du modèle:

```python
llm = ollama.Ollama(
    base_url=OLLAMA_URL, 
    model='mistral',
    temperature=0.5,
    callback_manager= CallbackManager([StreamingStdOutCallbackHandler()])
)
```
## Conversation

### Prompt template

Afin d'éviter la répétition, LangChain nous donne la possibilité de variabiliser notre prompt.

Pour cela, ajoutez l'import suivant:

```python
from langchain_core.prompts import ChatPromptTemplate
```

Déclarer votre template:

```python
prompt = ChatPromptTemplate.from_messages([
    ('system', 'You are a french instructor'),
    ('user', 'explain {concept} ')
])
```

Langchain permet de creér des `chain`, un enchainement de fonction. Les fonctions vont consommer les réponses des fonctions précédentes. 

Nous pouvons créer notre `chain` via le code suivant:

```python
chain = prompt | llm
```

L'invocation de notre model ese fait maintenant en appelant:

```python
response = chain.invoke({'concept': 'DDD'})
```


### Et si il avait un peu de mémoire ? 

Par défaut, chaque invocation au modèle se comportera comme si c'était la première.
Afin de simuler une conversation, il est possible de configurer une mémoire à notre modèle. 

Pour ce faire:

```python
from langchain.memory import ChatMessageHistory

chat_history = ChatMessageHistory()
```



## One Shot / Few Shot learning




## Prompt pré-configuré

https://python.langchain.com/docs/use_cases/summarization#quickstart

### Résumé d'un texte: 

Pour résumer un texte, on peut se baser sur la fonction `load_summarize_data`

```python
from langchain.chains.summarize import load_summarize_chain
```

L'utilisation de cette `chain` ce fait de la façon suivante:

```python
chain = load_summarize_chain(llm, chain_type="stuff")
```

En plus de fournir des prompt pré-enregistré, LangChain fournit également un ensemble de classe utilitaire permettant de charger différent type de données: JSON, CSV, lien web, ...

Pour notre example, nous allons utiliser le `WebBaseLoader`

```python
from langchain_community.document_loaders import WebBaseLoader
```

Prenons par exemple le contenu d'une page wikipédia: https://fr.wikipedia.org/wiki/Grand_mod%C3%A8le_de_langage

```python
loader = WebBaseLoader('https://fr.wikipedia.org/wiki/Grand_mod%C3%A8le_de_langage')
docs = loader.load()
summary = chain.invoke(docs)
```

Cette technique fonctionne pour les documents ayant une taille suffisament petite pour injecter dans le contexte du LLM. 

Dans le cas d'un long document, il 

## Comment rendre le modèle spécifique à mon domaine

Afin d'obtenir des réponses liée à un context particulier, il est possible de
limiter 