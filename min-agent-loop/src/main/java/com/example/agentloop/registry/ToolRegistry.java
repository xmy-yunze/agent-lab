package com.example.agentloop.registry;

import tools.jackson.core.JacksonException;
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
            ),
            new ToolDefinition("查询最近订单",
                    "根据用户userId，查询该用户最近的订单集合，返回订单id、商品id、单笔金额",
                    List.of(new ToolParam("userId", "string", true))
            ),
            new ToolDefinition("计算订单总金额",
                    "接收订单列表，计算全部订单金额总和，返回总金额数值",
                    List.of(new ToolParam("orderListJson", "string", true))
            ),
            new ToolDefinition("查询库存",
                    "根据商品id查询当前商品库存数量，返回库存数字",
                    List.of(new ToolParam("goodsId", "string", true))
            ),
            new ToolDefinition("发送站内通知",
                    "向指定用户发送一条站内通知消息，返回发送成功标记",
                    List.of(
                            new ToolParam("userId", "string", true),
                            new ToolParam("msgContent", "string", true)
                    )
            ),
            new ToolDefinition("查询操作日志",
                    "根据用户ID查询用户操作行为日志，返回多条日志记录",
                    List.of(new ToolParam("userId", "string", true))
            ),
            new ToolDefinition("获取用户收货地址",
                    "根据用户ID获取用户保存的收货地址信息",
                    List.of(new ToolParam("userId", "string", true))
            ),
            new ToolDefinition("查询账户余额",
                    "查询用户账户余额，返回余额浮点数",
                    List.of(new ToolParam("userId", "string", true))
            ),
            new ToolDefinition("关闭用户会话",
                    "关闭当前用户会话，标记会话结束，不需要返回业务数据",
                    List.of(new ToolParam("userId", "string", true))
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
        } else if ("1002".equals(userId)) {
            return """
                    {
                    "userId":"1002",
                    "username":"lisi",
                    "password":"Def789012",                    
                    "phone":"13800138000"                    
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
        JsonNode args;
        try {
            args = MAPPER.readTree(argsJson);
        } catch (JacksonException e) {
            return "{\"error\":\"参数JSON解析失败\"}";
        }
        return switch (toolName) {
            case "查用户信息" -> {
                String userIdText = args.get("userId").asString();
                yield mockQueryUser(userIdText);
            }
            case "校验密码格式" -> {
                String pwd = args.get("password").asString();
                yield mockCheckPasswordFormat(pwd);
            }
            case "查询最近订单" -> {
                String uid = args.get("userId").asString();
                System.out.println("[mock查询最近订单]收到userId参数：" + uid);
                yield """
                        {"userId":"%s","orders":[{"orderId":"o001","goodsId":"g101","amount":299},{"orderId":"o002","goodsId":"g102","amount":599}]}
                        """.formatted(uid);
            }
            case "计算订单总金额" -> {
                //计算类工具：数据可以假，逻辑不能假——对传入订单真实求和
                JsonNode orders = args.get("orderListJson");
                if (orders.isString()) {
                    //参数类型声明为 string，模型会把订单数组序列化成字符串传入，需二次解析
                    orders = MAPPER.readTree(orders.asString());
                }
                double total = 0;
                for (JsonNode order : orders) {
                    total += order.get("amount").asDouble();
                }
                yield "{\"totalAmount\":" + total + "}";
            }
            case "查询库存" -> "{\"goodsId\":\"g101\",\"stock\":126}";
            case "发送站内通知" -> "{\"success\":true,\"note\":\"通知已推送完成\"}";
            case "查询操作日志" -> {
                String uid = args.get("userId").asString();
                System.out.println("[mock查询操作日志]收到userId参数：" + uid);
                yield """
                        {"userId":"%s","logs":[{"time":"2026‑10‑04 10:20","action":"login"},{"time":"2026‑10‑04 11:00","action":"order"}]}
                        """.formatted(uid);
            }
            case "获取用户收货地址" -> {
                String uid = args.get("userId").asString();
                System.out.println("[mock获取用户收货地址]收到userId参数：" + uid);
                yield """
                        {"userId":"%s","address":"湖北省武汉市洪山区XX街道XX小区"}
                        """.formatted(uid);
            }
            case "查询账户余额" -> {
                String uid = args.get("userId").asString();
                System.out.println("[mock查询账户余额]收到userId参数：" + uid);
                yield "{\"userId\":\"%s\",\"balance\":1560.78}".formatted(uid);
            }
            case "关闭用户会话" -> "{\"sessionClosed\":true}";
            default -> "{\"error\":\"未知工具：" + toolName + "\"}";
        };
    }

    public static void main(String[] args) {
        printToolInventory();
        System.out.println("\n---测试查用户信息 1001---");
        System.out.println(mockQueryUser("1001"));

        System.out.println("\n---测试校验密码---");
        System.out.println(mockCheckPasswordFormat("Abc123456"));
    }
}