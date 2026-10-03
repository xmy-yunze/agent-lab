package com.example.agentloop.message;

public record ToolCall(
        String id,
        ToolCallFunction function,
        String type) {
}
