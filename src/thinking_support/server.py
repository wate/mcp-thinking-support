#!/usr/bin/env python3
"""思考支援MCPサーバーのメインモジュール"""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool

from .tools.stepwise import StepwiseThinking
from .tools.critical import CriticalThinking  
from .tools.logical import LogicalThinking

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# サーバーインスタンス
server = Server("thinking-support")

# 思考ツールインスタンス
stepwise = StepwiseThinking()
critical = CriticalThinking()
logical = LogicalThinking()

# ツール登録
tools = [
    # 段階的思考ツール
    Tool(
        name="stepwise_create_plan",
        description="問題を段階的なステップに分解して実行計画を作成する",
        inputSchema={
            "type": "object",
            "properties": {
                "problem": {
                    "type": "string",
                    "description": "解決したい問題や課題"
                },
                "context": {
                    "type": "string",
                    "description": "問題の背景や制約条件（オプション）"
                }
            },
            "required": ["problem"]
        }
    ),
    Tool(
        name="stepwise_execute_step",
        description="計画の特定ステップを実行し、結果を記録する",
        inputSchema={
            "type": "object",
            "properties": {
                "plan_id": {
                    "type": "string",
                    "description": "実行計画のID"
                },
                "step_number": {
                    "type": "integer",
                    "description": "実行するステップ番号"
                },
                "result": {
                    "type": "string",
                    "description": "ステップの実行結果"
                }
            },
            "required": ["plan_id", "step_number", "result"]
        }
    ),
    
    # クリティカルシンキングツール
    Tool(
        name="critical_analyze_claim",
        description="主張や情報を批判的に分析し、信頼性を評価する",
        inputSchema={
            "type": "object",
            "properties": {
                "claim": {
                    "type": "string",
                    "description": "分析したい主張や情報"
                },
                "source": {
                    "type": "string",
                    "description": "情報源（オプション）"
                }
            },
            "required": ["claim"]
        }
    ),
    Tool(
        name="critical_identify_bias",
        description="情報や議論における偏見や論理的誤謬を特定する",
        inputSchema={
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "分析したい内容"
                }
            },
            "required": ["content"]
        }
    ),
    
    # ロジカルシンキングツール
    Tool(
        name="logical_build_argument",
        description="前提から結論まで論理的な論証を構築する",
        inputSchema={
            "type": "object",
            "properties": {
                "premises": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "前提条件のリスト"
                },
                "conclusion": {
                    "type": "string",
                    "description": "導きたい結論"
                }
            },
            "required": ["premises", "conclusion"]
        }
    ),
    Tool(
        name="logical_find_causality",
        description="原因と結果の関係を分析し、因果関係を特定する",
        inputSchema={
            "type": "object",
            "properties": {
                "situation": {
                    "type": "string",
                    "description": "分析したい状況や現象"
                },
                "factors": {
                    "type": "array", 
                    "items": {"type": "string"},
                    "description": "考慮すべき要因のリスト（オプション）"
                }
            },
            "required": ["situation"]
        }
    )
]

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """利用可能なツールのリストを返す"""
    return tools

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[dict[str, Any]]:
    """ツール呼び出しを処理する"""
    try:
        if name == "stepwise_create_plan":
            result = await stepwise.create_plan(
                arguments["problem"], 
                arguments.get("context")
            )
        elif name == "stepwise_execute_step":
            result = await stepwise.execute_step(
                arguments["plan_id"],
                arguments["step_number"], 
                arguments["result"]
            )
        elif name == "critical_analyze_claim":
            result = await critical.analyze_claim(
                arguments["claim"],
                arguments.get("source")
            )
        elif name == "critical_identify_bias":
            result = await critical.identify_bias(arguments["content"])
        elif name == "logical_build_argument":
            result = await logical.build_argument(
                arguments["premises"],
                arguments["conclusion"]
            )
        elif name == "logical_find_causality":
            result = await logical.find_causality(
                arguments["situation"],
                arguments.get("factors", [])
            )
        else:
            raise ValueError(f"不明なツール: {name}")
            
        return [{"type": "text", "text": result}]
        
    except Exception as e:
        logger.error(f"ツール実行エラー ({name}): {e}")
        return [{"type": "text", "text": f"エラー: {str(e)}"}]

async def async_main():
    """サーバーを開始する"""
    logger.info("思考支援MCPサーバーを開始します...")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

def main():
    """エントリーポイント"""
    asyncio.run(async_main())

if __name__ == "__main__":
    main()