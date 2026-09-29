package com.example.agentloop;

import org.springframework.boot.CommandLineRunner;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientResponseException;

import java.util.List;

@Component
public class ChatRunner implements CommandLineRunner {
    private static final String URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions";

    //请求体
    public record ChatRequest(String model, List<ChatMessage> messages, double temperature) {
    }

    public record ChatMessage(String role, String content) {
    }
    //响应体
    public record ChatResponse(List<Choice> choices){}
    public record Choice(Message message){}
    public record Message(String content){}

    @Override
    public void run(String... args) throws Exception {
        System.out.println("ChatRunner started");
        ToolRegistry.printToolInventory();

        String key = System.getenv("ZHIPU_API_KEY");
        if (key == null) {
            throw new RuntimeException("ZHIPU_API_KEY not found");
        }
        ChatRequest body=new ChatRequest(
                "glm-4.7",
                List.of(new ChatMessage("user","你好，简单介绍一下自己")),
                0.7
        );
        RestClient restClient=RestClient.create();
        try{
            ChatResponse response=restClient.post()
                    .uri(URL)
                    .headers(h->{
                        h.set("Authorization", "Bearer " + key);
                        h.setContentType(MediaType.APPLICATION_JSON);
                    })
                    .body(body)
                    .retrieve()
                    .body(ChatResponse.class);
            if (response!=null && response.choices()!=null && !response.choices().isEmpty()){
                String content=response.choices.get(0).message().content();
                System.out.println("AI: " + content);
            }else{
                System.out.println("响应为空");
            }
        }catch (RestClientResponseException e){
            System.out.println("HTTP "+e.getStatusCode()+": "+e.getResponseBodyAsString());
        }catch (Exception e){
            System.out.println("请求失败："+e.getMessage());
        }
    }
}
