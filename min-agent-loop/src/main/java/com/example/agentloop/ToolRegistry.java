package com.example.agentloop;

import java.util.List;

public class ToolRegistry {
    public record ToolParam(String paraName,String type,boolean required){}

    public record ToolDefinition(
            String name,
            String description,
            List<ToolParam> params
    ){}

    public static final List<ToolDefinition> TOOL_LIST=List.of(
            new ToolDefinition("查用户信息",
                    "根据用户 ID 查询用户的基本信息",
                    List.of(new ToolParam("userId","string",true))
            ),
            new ToolDefinition(
                    "校验密码格式",
                    "校验密码是否符合要求",
                    List.of(new ToolParam("password","string",true))
            )
    );

    public static void printToolInventory(){
        System.out.println("可用工具：");
        for (int i=0;i<TOOL_LIST.size();i++){
            ToolDefinition tool=TOOL_LIST.get(i);
            System.out.printf(" %d. %s —— %s%n",i+1,tool.name(),tool.description());
            StringBuilder paraLine=new StringBuilder("     参数：");
            for(int j=0;j<tool.params().size();j++){
                ToolParam param=tool.params().get(j);
                if (j>0){
                    paraLine.append(", ");
                }
                paraLine.append(param.paraName())
                        .append("(").append(param.type())
                        .append(", ").append(param.required() ? "必填":"选填")
                        .append(")");
            }
            System.out.println(paraLine);
        }
    }
}
