package com.example.agentloop.runner;

import com.example.agentloop.message.ChatMessage;
import com.example.agentloop.message.ToolCall;
import com.example.agentloop.registry.ToolRegistry;
import org.springframework.boot.CommandLineRunner;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientResponseException;

import java.util.ArrayList;
import java.util.List;

@Component
public class ChatRunner implements CommandLineRunner {
    private static final String URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions";

    //请求体
    public record ChatRequest(String model, List<ChatMessage> messages, List<ToolRegistry.ZhipuTool> tools,
                              double temperature) {
    }

    //响应体
    public record ChatResponse(List<Choice> choices) {
    }

    public record Choice(ChatMessage message) {
    }


    @Override
    public void run(String... args) throws Exception {
        System.out.println("ChatRunner started");
        ToolRegistry.printToolInventory();

        String key = System.getenv("ZHIPU_API_KEY");
        if (key == null) {
            throw new RuntimeException("ZHIPU_API_KEY not found");
        }

        ArrayList<ChatMessage> messages = new ArrayList<>();
        String userInput = "帮我查userId=1001的用户，校验他的密码格式";
        messages.add(ChatMessage.ofUser(userInput));
        int round = 0;
        while (true) {
            round++;
            System.out.println("\n===== 第 " + round + " 轮 =====");
            ChatRequest body = new ChatRequest(
                    "glm-4.7",
                    messages,
                    ToolRegistry.buildZhipuTools(),
                    0.7
            );
            RestClient restClient = RestClient.create();
            ChatResponse response;
            try {
                response = restClient.post()
                        .uri(URL)
                        .headers(h -> {
                            h.set("Authorization", "Bearer " + key);
                            h.setContentType(MediaType.APPLICATION_JSON);
                        })
                        .body(body)
                        .retrieve()
                        .body(ChatResponse.class);
            } catch (RestClientResponseException e) {
                System.out.println("HTTP " + e.getStatusCode() + ": " + e.getResponseBodyAsString());
                break;
            } catch (Exception e) {
                System.out.println("请求失败：" + e.getMessage());
                break;
            }
            if (response == null || response.choices() == null || response.choices().isEmpty()) {
                System.out.println("模型返回空响应");
                break;
            }
            ChatMessage assistantMsg = response.choices().get(0).message();
            messages.add(assistantMsg);

            List<ToolCall> toolCallList = assistantMsg.tool_calls();
            if (toolCallList != null && !toolCallList.isEmpty()) {
                for (ToolCall Call : toolCallList) {
                    String toolName = Call.function().name();
                    String argsJson = Call.function().arguments();
                    System.out.println(">>> 执行工具：" + toolName);
                    System.out.println(">>> 工具原始参数：" + argsJson);
                    String toolResult;
                    try {
                        toolResult = ToolRegistry.executeMockTool(Call.function().name(), argsJson);
                    } catch (Exception e) {
                        toolResult = "工具调用异常：" + e.getMessage();
                    }
                    System.out.println(">>> 工具返回结果：" + toolResult);
                    ChatMessage toolMsg = ChatMessage.tool(toolResult, Call.id());
                    messages.add(toolMsg);
                    System.out.println(">>> 已把tool结果添加进messages列表");
                }
            } else {
                System.out.println("AI最终回答：" + assistantMsg.content());
                break;
            }
        }
    }
}
