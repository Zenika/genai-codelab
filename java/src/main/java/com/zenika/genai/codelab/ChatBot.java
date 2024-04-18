package com.zenika.genai.codelab;

import dev.langchain4j.chain.ConversationalChain;
import dev.langchain4j.chain.ConversationalRetrievalChain;
import dev.langchain4j.data.document.Document;
import dev.langchain4j.data.document.parser.TextDocumentParser;
import dev.langchain4j.data.document.splitter.DocumentSplitters;
import dev.langchain4j.data.message.AiMessage;
import dev.langchain4j.data.message.UserMessage;
import dev.langchain4j.data.segment.TextSegment;
import dev.langchain4j.memory.chat.MessageWindowChatMemory;
import dev.langchain4j.model.StreamingResponseHandler;
import dev.langchain4j.model.embedding.EmbeddingModel;
import dev.langchain4j.model.input.PromptTemplate;
import dev.langchain4j.model.ollama.OllamaChatModel;
import dev.langchain4j.model.ollama.OllamaEmbeddingModel;
import dev.langchain4j.model.ollama.OllamaStreamingChatModel;
import dev.langchain4j.model.output.Response;
import dev.langchain4j.retriever.EmbeddingStoreRetriever;
import dev.langchain4j.service.AiServices;
import dev.langchain4j.service.SystemMessage;
import dev.langchain4j.service.V;
import dev.langchain4j.store.embedding.EmbeddingStore;
import dev.langchain4j.store.embedding.EmbeddingStoreIngestor;
import dev.langchain4j.store.embedding.inmemory.InMemoryEmbeddingStore;
import dev.langchain4j.store.memory.chat.InMemoryChatMemoryStore;

import java.nio.file.Path;
import java.time.Duration;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.Map;

import static dev.langchain4j.data.document.loader.FileSystemDocumentLoader.loadDocument;

public class ChatBot {

    private static final String OLLAMA_URL = "http://localhost:11434";
    private static final String MODEL = "openhermes";

    public static void main(String[] args) {

        OllamaChatModel llm = new OllamaChatModel.OllamaChatModelBuilder()
                .baseUrl("http://localhost:11434")
                .modelName("openhermes")
                .temperature(0.3)
                .build();

        // First step
        var prompt = UserMessage.from("Who are you ?");
        var response = llm.generate(List.of(prompt));
        System.out.println(response.content().text());

        // Prompt Template - 1
        var template = PromptTemplate.from("explain the purpose of this regular expression {{regexp}}");
        var regexpPrompt = template
                .apply(
                        Map.of("regexp", "^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$"))
                .toUserMessage();
        Response<AiMessage> regexpResponse = llm.generate(List.of(regexpPrompt));
        System.out.println(regexpResponse.content().text());

        // Prompt Template - 2
        RegExpAssistant assistant = AiServices.create(RegExpAssistant.class, llm);
        System.out.println(assistant.explain("^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$"));

        // FewShot Learning
        AnimalAssistant animalAssistant = AiServices.create(AnimalAssistant.class, llm);
        System.out.println(animalAssistant.predictAnimalSound("lion"));

        // Text Summary
        EmbeddingModel embeddingModel = new OllamaEmbeddingModel("http://localhost:11434", "openhermes", Duration.of(60, ChronoUnit.SECONDS), 2);
        EmbeddingStore<TextSegment> embeddingStore = new InMemoryEmbeddingStore<>();

        EmbeddingStoreIngestor ingestor = EmbeddingStoreIngestor.builder()
                .documentSplitter(DocumentSplitters.recursive(300, 0))
                .embeddingModel(embeddingModel)
                .embeddingStore(embeddingStore)
                .build();
        Document document = loadDocument(Path.of("src/main/resources/java_introduction.txt"), new TextDocumentParser());
        ingestor.ingest(document);
        ConversationalRetrievalChain c = ConversationalRetrievalChain.builder()
                .chatLanguageModel(llm)
                .retriever(EmbeddingStoreRetriever.from(embeddingStore, embeddingModel))
                .build();

        System.out.println(c.execute("Write a concise summary of the following of the java_introduction.txt document"));

        // Conversation Memory
        var store = new InMemoryChatMemoryStore();

        var memory = new MessageWindowChatMemory.Builder()
                .chatMemoryStore(store)
                .maxMessages(10)
                .build();
        ConversationalChain chain = ConversationalChain.builder()
                .chatLanguageModel(llm)
                .chatMemory(memory)
                .build();

        var prompt1 = "Can you translate I love programming in French ?";
        System.out.println("[Human]: " + prompt1);
        System.out.println("[AI] : " + chain.execute(prompt1));

        var prompt2 = "What did I just ask you ?";
        System.out.println("[Human]: " + prompt2);
        System.out.println("[AI] : " + chain.execute(prompt2));
    }





    public interface RegExpAssistant {
        @dev.langchain4j.service.UserMessage("explain the purpose of this regular expression {{regexp}}")
        String explain(@V("regexp") String regexp);
    }

    interface AnimalAssistant {
        @SystemMessage("You are an animal sound expert, able to give the sound an animal does based on the name of the animal")
        @dev.langchain4j.service.UserMessage("cow: moo, cat: meow, dog: woof, {{it}}: ")
        String predictAnimalSound(String animal);

    }
}



