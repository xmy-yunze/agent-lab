package com.example.agentloop.registry;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Day 4 收口回归测试：守住两个最容易退化的点——
 * 1. 计算类工具的真实求和逻辑（曾焊死 898.0）
 * 2. 参数真实流入 mock（曾无视 args 焊死 zhangsan，1002 反证用例）
 */
class ToolRegistryTest {

    // 模型实际传参形状：参数类型声明为 string，订单数组被序列化成字符串（需二次解析）
    @Test
    void calcTotalAmount_parsesNestedJsonString() {
        String argsJson = """
                {"orderListJson": "[{\\"orderId\\":\\"o001\\",\\"amount\\":299},{\\"orderId\\":\\"o002\\",\\"amount\\":599}]"}
                """;
        String result = ToolRegistry.executeMockTool("计算订单总金额", argsJson);
        assertTrue(result.contains("\"totalAmount\":898.0"), "求和结果不符: " + result);
    }

    // 容错分支：万一模型直接传数组而不是字符串，也要算对
    @Test
    void calcTotalAmount_parsesDirectArray() {
        String argsJson = """
                {"orderListJson": [{"orderId": "o001", "amount": 100}, {"orderId": "o002", "amount": 200}]}
                """;
        String result = ToolRegistry.executeMockTool("计算订单总金额", argsJson);
        assertTrue(result.contains("\"totalAmount\":300.0"), "求和结果不符: " + result);
    }

    // 1002 反证：参数必须真的流进 mock（1002 = lisi，不是写死的 1001 数据）
    @Test
    void queryUser_paramsFlowThrough() {
        String result = ToolRegistry.executeMockTool("查用户信息", "{\"userId\": \"1002\"}");
        assertTrue(result.contains("lisi"), "参数未流入 mock: " + result);
    }
}
