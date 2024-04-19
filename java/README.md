# CodeLab GenAI Zenika - Java

## Installation

Pour lancer ce projet vous avez besoin:

- Java 17

Une fois le projet ouvert, vous pouvez installer les dépendances via la commande:

````bash
./mvnw clean package
````

Le suite du codelab aura lieu dans la classe `ChatBot`


Assurez-vous également que `Ollama` est démarrer, accessible et que le modèle OpenHermes est bien disponible.
Pour cela vous pouvez accéder à l'URL suivante: [http://localhost:11434/api/tags](http://localhost:11434/api/tags) et valider que OpenHermes est bien présent.

## Premier pas

Maintenant que tout est installé, nous allons pouvoir démarrer notre première application.

Afin d'appeler notre modèle, nous allons utiliser [LangChain](https://www.langchain.com/).

LangChain Community contient les intégrations pour les applications tierce comme Ollama.

Dans la class `ChatBot`, vous pouvez ajouter l'imports suivant :

```java
import dev.langchain4j.model.ollama.OllamaChatModel;
```

Notre modèle est actuellement accessible via l'URL `http://localhost:11434`

Nous allons créer l'objet permettant d'intéragir avec Ollama via le code suivant:

```java
OllamaChatModel llm = new OllamaChatModel.OllamaChatModelBuilder()
        .baseUrl("http://localhost:11434")
        .modelName("openhermes")
        .build();
```

Une fois cet objet créé nous allons pouvoir intéragir avec le modèle openhermes.
Pour cela on déclare un prompt:

```java
var prompt = UserMessage.from("Who are you ?");
```

Puis on invoque le modèle :

```java
var response = llm.generate(List.of(prompt));
System.out.println(response.content().text());
```

Executer la méthode main de la classe `ChatBot` pour lancer la première inférence du model.

Et voila! Nous avons effectué notre premier appel.

## Améliorons notre modèle

LangChain fournit un ensemble de fonction et d'utilitaire permettant de configurer plus finement notre application.

### Streaming de la réponse

Dans un premier temps, rendons notre application un peu plus vivante. Plutôt que de générer une réponse d'un coup, LangChain nous permet de streamer le flux de la réponse.

Pour cela, il faut modifier le type de model utiliser pour un model qui implémente l'interface `StreamingChatLanguageModel`.

On modifie la déclaration de notre model par le code suivant ainsi que l'appel au model:
```java
OllamaStreamingChatModel llm = new OllamaStreamingChatModel.OllamaStreamingChatModelBuilder()
        .baseUrl("http://localhost:11434")
        .modelName("openhermes")
        .build();

var prompt = UserMessage.from("Who are you ?");

llm.generate(List.of(prompt), new StreamingResponseHandler<AiMessage>() {
    @Override
    public void onNext(String s) {
        System.out.print(s);
    }

    @Override
    public void onError(Throwable throwable) {

    }
});
```

Réexecuter le fichier pour voir la différence


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

```java
OllamaChatModel llm = new OllamaChatModel.OllamaChatModelBuilder()
            .baseUrl("http://localhost:11434")
            .modelName("openhermes")
            .temperature(0.7)   
            .build();
```

Faite varier la temperature pour voir les différentes réponses possibles. 

## Conversation

### Prompt template

Afin d'éviter la répétition, LangChain nous donne la possibilité de variabiliser notre prompt.


Déclarer votre template:

```java
import dev.langchain4j.model.input.PromptTemplate;

var template = PromptTemplate.from("explain the purpose of this regular expression {{regexp}}");
var prompt = template
        .apply(
                Map.of("regexp", "^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$"))
        .toUserMessage();
```

L'invocation du modèle est identique:

```java
Response<AiMessage> response = llm.generate(List.of(prompt));
System.out.println(response.content().text());
```

Il est également possible de passer par `AiService`. Pour cela, on commence par créer une interface:

```java
interface RegExpAssistant {
    String explain(String regexp);
}
```

On annote la méthode de cette interface afin de lui injecter un template de prompt:

```java
@UserMessage("explain the purpose of this regular expression {{regexp}}")
String explain(@V("regexp") String regexp);
```
On peut maintenant instancier notre service et le tester:

```java
RegExpAssistant assistant = AiServices.create(RegExpAssistant.class, llm);
System.out.println(assistant.explain("^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$"));
```


## One Shot / Few Shot learning

Il existe différentes techniques permettant de contextualiser les réponses. Une première technique consiste à passer des
exemples de questions / réponses dans le contexte.

Dans un premier temps, on commence par définir une simple interface avec laquelle nous allons pouvoir intéragir:

```java
interface Assistant {
    
    String predictAnimalSound(String animal);
    
}
```

On annote notre interface pour lui fournir un context contenant les exemples nécéssaires:

```java
@SystemMessage("You are an animal sound expert, able to give the sound an animal does based on the name of the animal")
@UserMessage("cow: moo, cat: meow, dog: woof, {{it}}: ")
String predictSound(String animal);
```

On peut maintenant instancier notre service et le tester:

```java
Assistant assistant = AiServices.create(Assistant.class, llm);
System.out.println(assistant.predictSound("lion"));
```

## Résumé d'un texte:

Langchain4j ne possède pas autant d'intégration que la version Python mais il est possible de facilement
résumé un texte, pour cela, nous avons besoin de plusieurs objets

```java
EmbeddingModel embeddingModel = new OllamaEmbeddingModel("http://localhost:11434", "openhermes", Duration.of(60, ChronoUnit.SECONDS), 2);
EmbeddingStore<TextSegment> embeddingStore = new InMemoryEmbeddingStore<>();

EmbeddingStoreIngestor ingestor = EmbeddingStoreIngestor.builder()
        .documentSplitter(DocumentSplitters.recursive(300, 0))
        .embeddingModel(embeddingModel)
        .embeddingStore(embeddingStore)
        .build();
```

Tout d'abord, nous avons déclarer un model permettant de calculer des embeddings. Nous avons ensuite créer un objet permettant de stocker ces embeddings en mémoire. 

Enfin, nous avons créer un objet permettant d'assembler: notre modèle de calcul d'embeddings, notre store ainsi qu'un objet permettant de découper le texte en "chunk".

Pour découper le document, nous avons dans un premier temps besoin de le parser, pour cela, LangChain4J fournit une classe utilitaire: 
```java
Document document = loadDocument(Path.of("java_introduction.txt"), new TextDocumentParser());
```

Une fois ce document parsé, on peut l'indexer:

```java
ingestor.ingest(document);
```

Une fois cela fait, nous pouvons alors définir une nouvelle `chain` qui se basera sur notre index d'embeddings en mémoire:

```java
ConversationalRetrievalChain c = ConversationalRetrievalChain.builder()
        .chatLanguageModel(llm)
        .retriever(EmbeddingStoreRetriever.from(embeddingStore, embeddingModel))
        .build();
```

Nous pouvons alors demander au modèle de nous faire un résumé: 

```java
System.out.println(c.execute("Write a concise summary of the following of the java_introduction.txt document"));
```
Dans le cas ou nous avons de très gros document ou un ensemble de document, il est préférable d'utiliser une base de données vectorielle pour stocker nos embeddings.

## Et si il avait un peu de mémoire ?

Par défaut, chaque invocation au modèle se comportera comme si c'était la première.
Afin de simuler une conversation, il est possible de configurer une mémoire à notre modèle.

Pour ce faire, on peut utiliser un template de prompt qui va assembler un historique de nos message à chaque nouvelle inférence.

Langchain nous propose un objet permettant de gérer un historique de message:

```java
var store = new InMemoryChatMemoryStore();

var memory = new MessageWindowChatMemory.Builder()
        .chatMemoryStore(store)
        .build();
```
On peut ensuite initialiser notre `chain` : 

```java
import dev.langchain4j.chain.ConversationalChain;

ConversationalChain chain = ConversationalChain.builder()
            .chatLanguageModel(llm)
            .chatMemory(memory)
            .maxMessages(10)
            .build();
```

Nous pouvons ensuite inférer notre modèle plusieurs fois et vérifier qu'il a bien de la mémoire:

```java
var prompt1 = "Can you translate I love programming in French ?";
System.out.println("[Human]: " + prompt1);
System.out.println("[AI] : " + chain.execute(prompt1));

var prompt2 = "What did I just ask you ?";
System.out.println("[Human]: " + prompt2);
System.out.println("[AI] : " + chain.execute(prompt2));
```
