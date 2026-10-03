package com.example.agentloop.registry;

import tools.jackson.databind.JsonNode;
import tools.jackson.databind.ObjectMapper;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


public class ToolRegistry {
    //内部
    public record ToolParam(
            String paraName,
            String type,
            boolean required
    ) {
    }

    public record ToolDefinition(
            String name,
            String description,
            List<ToolParam> params
    ) {
    }

    //外部
    public record ZhipuTool(
            String type,
            ZhipuFunction function
    ) {
    }

    public record ZhipuFunction(
            String name,
            String description,
            ZhipuParameters parameters
    ) {
    }

    public record ZhipuParameters(
            String type,
            Map<String, ZhipuProperty> properties,
            List<String> required
    ) {
    }

    public record ZhipuProperty(
            String type
    ) {
    }

    //唯一数据源：在这里新增/删除工具，其他代码不用改
    public static final List<ToolDefinition> TOOL_LIST = List.of(
            new ToolDefinition("查用户信息",
                    "根据用户 ID 查询用户的基本信息",
                    List.of(new ToolParam("userId", "string", true))
            ),
            new ToolDefinition(
                    "校验密码格式",
                    "校验密码是否符合要求",
                    List.of(new ToolParam("password", "string", true))
            )
    );

    //消费①：控制台打印工具清单
    public static void printToolInventory() {
        System.out.println("可用工具：");
        for (int i = 0; i < TOOL_LIST.size(); i++) {
            ToolDefinition tool = TOOL_LIST.get(i);
            System.out.printf(" %d. %s —— %s%n", i + 1, tool.name(), tool.description());
            StringBuilder paraLine = new StringBuilder("     参数：");
            for (int j = 0; j < tool.params().size(); j++) {
                ToolParam param = tool.params().get(j);
                if (j > 0) {
                    paraLine.append(", ");
                }
                paraLine.append(param.paraName())
                        .append("(").append(param.type())
                        .append(", ").append(param.required() ? "必填" : "选填")
                        .append(")");
            }
            System.out.println(paraLine);
        }
    }

    //消费②：遍历TOOL_LIST，生成智谱API需要的tools数组
    public static List<ZhipuTool> buildZhipuTools() {
        return TOOL_LIST.stream().map(toolDefinition -> {
            Map<String, ZhipuProperty> propMap = new HashMap<>();
            List<String> requiredList = new ArrayList<>();

            for (ToolParam param : toolDefinition.params()) {
                propMap.put(param.paraName(), new ZhipuProperty(param.type()));
                if (param.required()) {
                    requiredList.add(param.paraName());
                }
            }
            ZhipuParameters parameters = new ZhipuParameters("object", propMap, requiredList);
            ZhipuFunction function = new ZhipuFunction(toolDefinition.name(), toolDefinition.description(), parameters);
            return new ZhipuTool("function", function);
        }).toList();
    }

    //消费③：工具mock实现（工具的手，假数据）
    public static String mockQueryUser(String userId) {
        if ("1001".equals(userId)) {
            return """
                    {
                        "userId":"1001",
                        "username":"xmy",
                        "password":"Abc123456",
                        "phone":17702794614
                    }
                    """;
        } else {
            return "{\"msg\":\"找不到该用户\"}";
        }
    }

    public static String mockCheckPasswordFormat(String password) {
        boolean hasLetter = password.chars().anyMatch(Character::isLetter);
        boolean hasDigit = password.chars().anyMatch(Character::isDigit);
        boolean lenOk = password.length() >= 8;
        if (hasLetter && hasDigit && lenOk) {
            return "{\"msg\":\"密码格式正确\"}";
        } else {
            return "{\"result\":false,\"msg\":\"密码格式错误，需要≥8位，同时包含字母和数字\"}";
        }
    }

    public static final ObjectMapper MAPPER = new ObjectMapper();

    public static String executeMockTool(String toolName, String argsJson) {
        JsonNode args = MAPPER.readTree(argsJson);
        if ("查用户信息".equals(toolName)) {
            String userId = args.get("userId").stringValue();
            return mockQueryUser(userId);
        } else if ("校验密码格式".equals(toolName)) {
            String password = args.get("password").stringValue();
            return mockCheckPasswordFormat(password);
        } else {
            return "未知工具" + toolName;
        }
    }

    public static void main(String[] args) {
        printToolInventory();
        System.out.println("\n---测试查用户信息 1001---");
        System.out.println(mockQueryUser("1001"));

        System.out.println("\n---测试校验密码---");
        System.out.println(mockCheckPasswordFormat("Abc123456"));
    }
}
