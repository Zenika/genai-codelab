
## Comment rendre le modèle spécifique à mon domaine

Afin d'obtenir des réponses liée à un context particulier, il est possible de

### Génération d'embedding

Pour construire notre base de connaissance, nous allons devoir convertir nos documents / donnée en embeddings.
Il y a différents algorithm / librairie permettant de générer des embeddings. 
LangChain fournit différentes intégration pour générer les embeddings en fonction du model utilisé. 

Dans notre cas, nous allons utiliser le code suivant: 

```python
from langchain_community.embeddings import OllamaEmbeddings

embeddings_generator = OllamaEmbeddings(model = 'mistral')
```

Nous pouvons tester que le générateur fonctionne correctement avec le code suivant:

```python
text = 'this is a sentence'

text_embedding = embeddings_generator.embed_query(text)

# Affichage du début de l'embedding
print(text_embedding[:5]) 
```

Les embeddings ayant un taille maximale (dépendant du model), l'indexation d'un document complet nécessite le découpage 
du document en `chunk`. 
Pour cela, LangChain met à disposition un package permettant de découper différent type de document `langchain-text-splitters`. 

Une fois les embeddings généré, on peut les insérer dans une base de données vectorielle, il en existe plusieurs:

* ChromaDB
* FAISS
* Lance