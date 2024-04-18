package com.zenika.genai.codelab;


import dev.langchain4j.model.ollama.OllamaChatModel;


public class ChatBot {

    private static final String OLLAMA_URL = "http://localhost:11434";
    private static final String MODEL = "openhermes";

    public static void main(String[] args) {

        OllamaChatModel llm = new OllamaChatModel.OllamaChatModelBuilder()
                .baseUrl("http://localhost:11434")
                .modelName("openhermes")
                .temperature(0.3)
                .build();

    }

}



