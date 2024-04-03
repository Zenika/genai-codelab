# CodeLab GenAI Zenika - JavaScript

## Installation

Pour lancer ce projet vous avez besoin:

- Node 17+

Une fois le projet ouvert, vous pouvez installer les dépendances via la commande:

````bash
npm install
````

On retrouve une dépendance vers `langchain`

Le suite du codelab aura lieu dans le fichier `src/app.js`

Assurez-vous également que `Ollama` est démarrer, accessible et que le modèle Mistral7B est bien disponible.
Pour cela vous pouvez accéder à l'URL suivante: (http://localhost:11434/api/tags)[http://localhost:11434/api/tags] et valider que Mistral est bien présent.

## Premier pas

Maintenant que tout est installé, nous allons pouvoir démarrer notre première application.

Afin d'appeler notre modèle, nous allons utiliser (LangChain)[https://www.langchain.com/].

LangChain Community contient les intégrations pour les applications tierce comme Ollama.

Dans le fichier `src/app.js`, vous pouvez ajouter l'imports suivant :

```javascript
const { ChatOllama }  = require("@langchain/community/chat_models/ollama");
const { ChatPromptTemplate } = require("@langchain/core/prompts");
```

Notre modèle est actuellement accessible via l'URL `http://localhost:11434`

Nous allons créer l'objet permettant d'intéragir avec Ollama via le code suivant:

```javascript
const OLLAMA_URL = 'http://localhost:11434'
const MODEL = 'openhermes'

const llm = new ChatOllama({
  baseUrl: OLLAMA_URL,
  model: MODEL,
});
```

Une fois cet objet créé nous allons pouvoir intéragir avec le modèle mistral.
Pour cela on déclare un prompt:

```javascript
const prompt = 'Who are you ?'
```

Puis on invoque le modèle :

```javascript
const result = await llm.invoke(prompt);
console.log(result.content);
```

Executer le fichier `src/app.js` pour lancer la première inférence du model.

```bash
node src/app.js
```

Et voila! Nous avons effectué notre premier appel.

## Améliorons notre modèle

LangChain fournit un ensemble de fonction et d'utilitaire permettant de configurer plus finement notre application.


### Temperature

Afin de limiter les hallucinations des modèles, il est possible de faire varier le paramètre `temperature`.
Ce paramètre (compris entre 0 et 1) permet de définir la "créativité" du modèle.
Plus la valeur est proche de 1, plus le modèle va pouvoir halluciner.
Plus la valeur est proche de 0, plus le modèle va être déterministe.

--- 
> Règles de bases
>
>* Pour des taches de transformation (correction de fautes, extraction de données, conversion de format) on vise une temperature entre 0 et 0.3
>* Pour des taches d'écriture simple, de résumé, on vise une température proche de 0.5
>* Pour des taches nécessitant de la créativité (marketing, pub), on vise une température entre 0.7 et 1
---

Pour configurer la temperature, modifier la déclaration du modèle:

```javascript
const llm = new ChatOllama({
  baseUrl: OLLAMA_URL,
  model: MODEL,
  temperature: 0.9
});
```

Faite varier la temperature pour voir les différentes réponses possibles. 

## Conversation

### Prompt template

Afin d'éviter la répétition, LangChain nous donne la possibilité de variabiliser notre prompt.


Déclarer votre template:

```javascript
const { PromptTemplate } = require("@langchain/core/prompts");

const template = PromptTemplate.fromTemplate('explain me this Regular expression{regexp}')
const chain = template.pipe(llm)
```

L'invocation du modèle est identique:

```javascript
const result = await chain.invoke({regexp: '^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$'});
console.log(result.content)
```

## One Shot / Few Shot learning

Il existe différente technique permettant de contextualiser les réponses. Une première technique consiste à passer des 
exemples de questions / réponses dans le contexte. 
On peut faire notre propre template de prompt ou utiliser directement un prompt pré-configuré par LangChain:

```javascript
const { ChatPromptTemplate, FewShotChatMessagePromptTemplate} = require("@langchain/core/prompts");
```

Dans un premier temps, on commence par définir un ensemble d'exemple qui vont aider notre modèle à répondre:

```javascript
const examples = [
    {'animal': 'cow', 'sound': 'moo'},
    {'animal': 'cat', 'sound': 'meow'},
    {'animal': 'dog', 'sound': 'woof'}
]
```

On créé ensuite un template de prompt pour y injecter nos exemple:

```javascript
const examplePrompt = ChatPromptTemplate.fromTemplate(`human: {animal} ai: {sound}`)
```

Initialiser le template contenant tous les exemples ainsi que la question:

```javascript
const fewShotPrompt = new FewShotChatMessagePromptTemplate({
  prefix:
    "based on the following example, write the sound the animal does",
  suffix: "Human: {animal}",
  examplePrompt,
  examples,
  inputVariables: ["animal"],
});
```

Pour invoquer notre modèle:

```javascript
const fewShotChain = fewShotPrompt.pipe(llm)
const result = await fewShotChain.invoke({animal: 'lion'});
console.log(result.conten);
```


## Prompt pré-configuré

Langchain nous propose un ensemble de pré-configuré. Dans cet exemple, nous allons utiliser la `chain`: `loadSummarizationChain`
qui n'ait rien d'autre qu'un template de prompt:

```
prompt_template = """Write a concise summary of the following:
{text}
CONCISE SUMMARY:"""
```

### Résumé d'un texte: 

Pour résumer un texte, on peut se baser sur la fonction `loadSummarizationChain`

```javascript
const { loadSummarizationChain } = require("langchain/chains");
const { RecursiveCharacterTextSplitter } = require("langchain/text_splitter");
const fs = require("fs");
```

L'utilisation de cette `chain` ce fait de la façon suivante:

```javascript
const summarizationChain = loadSummarizationChain(llm, { type: "map_reduce" });
```

En plus de fournir des prompt pré-enregistré, LangChain fournit également un ensemble de classe utilitaire permettant de charger différent type de données: JSON, CSV, lien web, ...

Pour notre example, nous allons utiliser un simple fichier texte.

```javascript
const text = fs.readFileSync("java_introduction.txt", "utf8");
```

Une fois le texte chargé, on découpe le document en chunk

```javascript
const textSplitter = new RecursiveCharacterTextSplitter({ chunkSize: 1000 });
textSplitter.createDocuments([text]).then((docs) => );
```

On peut ensuite inférer notre `chain`:

```javascript
const docs = await textSplitter.createDocuments([text]);
const summary = await summarizationChain.invoke({input_documents: docs});
console.log(summary)
```

Cette technique fonctionne pour les documents ayant une taille suffisamment petite pour injecter dans le contexte du LLM. 

Dans le cas d'un long document, il sera nécéssaire de découper notre document. On peut s'orienter vers des solutions de type RAG


## Et si il avait un peu de mémoire ? 

Par défaut, chaque invocation au modèle se comportera comme si c'était la première.
Afin de simuler une conversation, il est possible de configurer une mémoire à notre modèle. 

Pour ce faire, on peut utiliser un template de prompt qui va assembler un historique de nos message à chaque nouvelle inférence. 

Langchain nous propose un objet permettant de gérer un historique de message:

```javascript
const { ChatMessageHistory } = require("langchain/stores/message/in_memory");
```
Cet historique est intrégrer directement dans un prompt:

```javascript
const { MessagesPlaceholder } = require("@langchain/core/prompts");

const runnableWithMessageHistoryPrompt = ChatPromptTemplate.fromMessages([
  [
    "system",
    "You are a helpful assistant. Answer all questions to the best of your ability.",
  ],
  new MessagesPlaceholder("chat_history"),
  ["human", "{input}"],
]);

const chain2 = runnableWithMessageHistoryPrompt.pipe(llm);
```

La conversation et la mémoire peuvent être instanciés de la façon suivante:

```javascript
const { ChatMessageHistory } = require("langchain/stores/message/in_memory");
const { RunnableWithMessageHistory } = require("@langchain/core/runnables");

const chatHistory = new ChatMessageHistory();

const chainWithMessageHistory = new RunnableWithMessageHistory({
  runnable: chain2,
  getMessageHistory: (_sessionId) => chatHistory,
  inputMessagesKey: "input",
  historyMessagesKey: "chat_history",
});
```

Et inféré via l'appel à la méthode `invoke`:

```javascript
 const r1 = await chainWithMessageHistory.invoke(
      {
        input:
          "Translate this sentence from English to French: I love programming.",
      },
      { configurable: { sessionId: "unused" } }
    );
  console.log(r1.content);
  const r2 = await chainWithMessageHistory.invoke(
    {
      input:
        "What Did I just ask you ?",
    },
    { configurable: { sessionId: "unused" } }
    );
  console.log(r2.content);
```

