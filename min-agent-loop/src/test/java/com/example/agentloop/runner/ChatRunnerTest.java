package com.example.agentloop.runner;

import com.example.agentloop.registry.ToolRegistry;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ChatRunnerTest {
    @Test
    void unknownToolCountsAsFailure() {
        String result = ToolRegistry.executeMockTool("不存在的工具", "{}");
        assertEquals(3, ChatRunner.nextFailureCount(2, result));
    }

    @Test
    void invalidArgumentsCountAsFailure() {
        String result = ToolRegistry.executeMockTool("查用户信息", "{");
        assertEquals(1, ChatRunner.nextFailureCount(0, result));
    }

    @Test
    void successfulToolResetsConsecutiveFailures() {
        String result = ToolRegistry.executeMockTool("查用户信息", "{\"userId\":\"1002\"}");
        assertEquals(0, ChatRunner.nextFailureCount(2, result));
    }
}
