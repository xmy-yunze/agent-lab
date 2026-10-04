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
import java.util.Scanner;

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
        String userInput = "给用户 1001 发送短信验证码通知，凡工具返回 error，必须如实告知失败，不得声称成功";
        messages.add(ChatMessage.ofUser(userInput));
        int round = 0;
        final int MAX_ROUNDS = 10;
        int consecutiveFail = 0;
        final int MAX_CONSECUTIVE_FAIL = 3;
        while (true) {
            if (round >= MAX_ROUNDS) {
                System.out.println("【退出】已达到最大轮次" + MAX_ROUNDS + "，强制终止Agent循环");
                break;
            }
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
                System.out.println("【退出‑接口异常】HTTP错误：" + e.getResponseBodyAsString());
                break;
            } catch (Exception e) {
                System.out.println("【退出‑接口异常】请求失败：" + e.getMessage());
                break;
            }
            if (response == null || response.choices() == null || response.choices().isEmpty()) {
                System.out.println("【退出】模型返回空响应");
                break;
            }
            ChatMessage assistantMsg = response.choices().get(0).message();
            messages.add(assistantMsg);

            List<ToolCall> toolCallList = assistantMsg.tool_calls();
            if (toolCallList != null && !toolCallList.isEmpty()) {
                for (ToolCall call : toolCallList) {
                    String toolName = call.function().name();
                    String argsJson = call.function().arguments();
                    System.out.println(">>> 执行工具：" + toolName);
                    System.out.println(">>> 工具原始参数：" + argsJson);
                    String toolResult;
                    try {
                        toolResult = ToolRegistry.executeMockTool(call.function().name(), argsJson);
                        consecutiveFail = 0;

                    } catch (Exception e) {
                        toolResult = "工具调用异常：" + e.getMessage();
                        System.out.println("【工具执行失败】" + toolName + "，错误信息：" + e.getMessage());
                        consecutiveFail++;
                    }
                    System.out.println(">>> 工具返回结果：" + toolResult);
                    ChatMessage toolMsg = ChatMessage.tool(toolResult, call.id());
                    messages.add(toolMsg);
                    System.out.println(">>> 已把tool结果添加进messages列表");
                }
                if (consecutiveFail >= MAX_CONSECUTIVE_FAIL) {
                    System.out.println("【退出‑工具执行失败】连续" + consecutiveFail + "次工具执行失败，强制终止Agent循环");
                    break;
                }
            } else {
                System.out.println("【退出‑正常完成】模型不再调用工具，任务结束");
                System.out.println("AI最终回答：" + assistantMsg.content());
                break;
            }
        }
    }
}