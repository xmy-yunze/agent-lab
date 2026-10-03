package com.example.agentloop.message;

import java.util.List;

public record ChatMessage(
        String role,
        String content,
        List<ToolCall> tool_calls,
        String tool_call_id
) {
    public static ChatMessage ofUser(String content) {
        return new ChatMessage("user", content, null, null);
    }

    public static ChatMessage Assistant(String content, List<ToolCall> toolCalls) {
        return new ChatMessage("assistant", content, toolCalls, null);
    }

    public static ChatMessage tool(String toolResultContent, String toolCallId) {
        return new ChatMessage("tool", toolResultContent, null, toolCallId);
    }
}

