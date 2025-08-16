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
from .tools.why_analysis import WhyAnalysis
from .tools.mece import MECE
from .tools.dialectical import DialecticalThinking
from .tools.sequential import SequentialThinking
from .tools.scamper import SCAMPER

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# サーバーインスタンス
server = Server("thinking-support")

# 思考ツールインスタンス
stepwise = StepwiseThinking()
critical = CriticalThinking()
logical = LogicalThinking()
why_analysis = WhyAnalysis()
mece = MECE()
dialectical = DialecticalThinking()
sequential = SequentialThinking()
scamper = SCAMPER()

# ツール登録
tools = [
    # 動的思考ツール（Sequential Thinking）
    Tool(
        name="sequential_thinking",
        description="""動的で反省的な問題解決のための詳細ツール。
柔軟な思考プロセスを通じて問題を分析し、理解が深まるにつれて適応・発展させることができます。
各思考は、前の洞察に基づいて構築、質問、または修正することができます。

使用場面:
- 複雑な問題をステップに分解する
- 修正の余地がある計画と設計
- コース修正が必要になる可能性のある分析
- 最初は全体像が明確でない問題
- 複数ステップの解決が必要な問題
- 複数のステップにわたってコンテキストを維持する必要があるタスク
- 無関係な情報をフィルタリングする必要がある状況

主な機能:
- 進行に応じてtotal_thoughtsを上下に調整可能
- 前の思考に疑問を持ったり修正したりできる
- 終わりに達したと思われた後でも、さらに思考を追加できる
- 不確実性を表現し、代替アプローチを探求できる
- 思考は線形に構築する必要はない - 分岐や逆戻りが可能
- 解決仮説の生成
- 思考の連鎖ステップに基づく仮説の検証
- 満足するまでプロセスを繰り返し
- 正しい答えを提供
""",
        inputSchema={
            "type": "object",
            "properties": {
                "thought": {
                    "type": "string",
                    "description": "現在の思考ステップ"
                },
                "next_thought_needed": {
                    "type": "boolean",
                    "description": "さらなる思考ステップが必要かどうか"
                },
                "thought_number": {
                    "type": "integer",
                    "description": "現在の思考番号",
                    "minimum": 1
                },
                "total_thoughts": {
                    "type": "integer",
                    "description": "推定される必要な思考の総数",
                    "minimum": 1
                },
                "is_revision": {
                    "type": "boolean",
                    "description": "これが前の思考を修正するものかどうか"
                },
                "revises_thought": {
                    "type": "integer",
                    "description": "再考されている思考の番号",
                    "minimum": 1
                },
                "branch_from_thought": {
                    "type": "integer",
                    "description": "分岐点となる思考番号",
                    "minimum": 1
                },
                "branch_id": {
                    "type": "string",
                    "description": "分岐識別子"
                },
                "needs_more_thoughts": {
                    "type": "boolean",
                    "description": "さらに思考が必要かどうか"
                }
            },
            "required": ["thought", "next_thought_needed", "thought_number", "total_thoughts"]
        }
    ),
    
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
    ),
    
    # 5Why分析ツール
    Tool(
        name="why_analysis_start",
        description="5Why分析を開始して根本原因を特定する",
        inputSchema={
            "type": "object",
            "properties": {
                "problem": {
                    "type": "string",
                    "description": "分析したい問題や現象"
                },
                "context": {
                    "type": "string", 
                    "description": "問題の背景情報（オプション）"
                }
            },
            "required": ["problem"]
        }
    ),
    Tool(
        name="why_analysis_add_answer",
        description="5Why分析の質問に回答し、次のWhyを生成する",
        inputSchema={
            "type": "object",
            "properties": {
                "analysis_id": {
                    "type": "string",
                    "description": "分析ID"
                },
                "level": {
                    "type": "integer",
                    "description": "回答するWhyのレベル（0から4）"
                },
                "answer": {
                    "type": "string",
                    "description": "質問への回答"
                }
            },
            "required": ["analysis_id", "level", "answer"]
        }
    ),
    Tool(
        name="why_analysis_get",
        description="5Why分析の現在の状況を取得する",
        inputSchema={
            "type": "object",
            "properties": {
                "analysis_id": {
                    "type": "string",
                    "description": "分析ID"
                }
            },
            "required": ["analysis_id"]
        }
    ),
    Tool(
        name="why_analysis_list",
        description="すべての5Why分析の一覧を取得する",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    
    # MECEツール
    Tool(
        name="mece_analyze_categories",
        description="カテゴリのMECE分析を実行して重複や漏れを検証する",
        inputSchema={
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "分析対象のトピック"
                },
                "categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "分析するカテゴリのリスト"
                }
            },
            "required": ["topic", "categories"]
        }
    ),
    Tool(
        name="mece_create_structure",
        description="トピックに対するMECE構造を提案する",
        inputSchema={
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "構造を作成したいトピック"
                },
                "framework": {
                    "type": "string",
                    "description": "使用するフレームワーク（auto, 4P, 3C, SWOT, 時系列, 内外など）",
                    "default": "auto"
                }
            },
            "required": ["topic"]
        }
    ),
    
    # 弁証法ツール
    Tool(
        name="dialectical_start_process",
        description="弁証法的思考プロセスを開始する",
        inputSchema={
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "弁証法的思考を適用したいトピックや問題"
                },
                "context": {
                    "type": "string",
                    "description": "背景情報や制約条件（オプション）"
                }
            },
            "required": ["topic"]
        }
    ),
    Tool(
        name="dialectical_set_thesis",
        description="弁証法プロセスのテーゼ（正）を設定する",
        inputSchema={
            "type": "object",
            "properties": {
                "process_id": {
                    "type": "string",
                    "description": "弁証法プロセスのID"
                },
                "thesis": {
                    "type": "string",
                    "description": "テーゼ（初期の主張や立場）"
                },
                "evidence": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "テーゼを支持する根拠（オプション）"
                }
            },
            "required": ["process_id", "thesis"]
        }
    ),
    Tool(
        name="dialectical_set_antithesis",
        description="弁証法プロセスのアンチテーゼ（反）を設定する",
        inputSchema={
            "type": "object",
            "properties": {
                "process_id": {
                    "type": "string",
                    "description": "弁証法プロセスのID"
                },
                "antithesis": {
                    "type": "string",
                    "description": "アンチテーゼ（テーゼに対する反対意見や課題）"
                },
                "evidence": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "アンチテーゼを支持する根拠（オプション）"
                }
            },
            "required": ["process_id", "antithesis"]
        }
    ),
    Tool(
        name="dialectical_create_synthesis",
        description="弁証法プロセスのジンテーゼ（合）を構築する",
        inputSchema={
            "type": "object",
            "properties": {
                "process_id": {
                    "type": "string",
                    "description": "弁証法プロセスのID"
                },
                "synthesis": {
                    "type": "string",
                    "description": "ジンテーゼ（テーゼとアンチテーゼを統合した新たな見解）"
                },
                "reasoning": {
                    "type": "string",
                    "description": "統合の理由や論理（オプション）"
                }
            },
            "required": ["process_id", "synthesis"]
        }
    ),
    Tool(
        name="dialectical_analyze_contradiction",
        description="矛盾する立場を分析し、弁証法的統合を提案する",
        inputSchema={
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "分析対象のトピック"
                },
                "position_a": {
                    "type": "string",
                    "description": "立場A"
                },
                "position_b": {
                    "type": "string",
                    "description": "立場B（Aと矛盾する立場）"
                }
            },
            "required": ["topic", "position_a", "position_b"]
        }
    ),
    Tool(
        name="dialectical_get_process",
        description="弁証法プロセスの現在の状況を取得する",
        inputSchema={
            "type": "object",
            "properties": {
                "process_id": {
                    "type": "string",
                    "description": "弁証法プロセスのID"
                }
            },
            "required": ["process_id"]
        }
    ),
    Tool(
        name="dialectical_list_processes",
        description="すべての弁証法プロセスの一覧を取得する",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    
    # SCAMPERツール
    Tool(
        name="scamper_start_session",
        description="SCAMPER創造的思考セッションを開始する",
        inputSchema={
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "創造的思考を適用したいトピックや課題"
                },
                "current_situation": {
                    "type": "string",
                    "description": "現在の状況や問題の詳細"
                },
                "context": {
                    "type": "string",
                    "description": "背景情報や制約条件（オプション）"
                }
            },
            "required": ["topic", "current_situation"]
        }
    ),
    Tool(
        name="scamper_apply_technique",
        description="指定されたSCAMPER技法でアイデアを生成する",
        inputSchema={
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "string",
                    "description": "SCAMPERセッションのID"
                },
                "technique": {
                    "type": "string",
                    "description": "適用するSCAMPER技法（substitute/combine/adapt/modify/put_to_other_use/eliminate/reverse）"
                },
                "ideas": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "生成したアイデアのリスト"
                },
                "explanations": {
                    "type": "array", 
                    "items": {"type": "string"},
                    "description": "各アイデアの説明（オプション）"
                }
            },
            "required": ["session_id", "technique", "ideas"]
        }
    ),
    Tool(
        name="scamper_evaluate_ideas",
        description="生成されたアイデアを実現可能性とインパクトで評価する",
        inputSchema={
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "string",
                    "description": "SCAMPERセッションのID"
                },
                "idea_evaluations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "idea": {"type": "string"},
                            "feasibility": {"type": "integer", "minimum": 0, "maximum": 10},
                            "impact": {"type": "integer", "minimum": 0, "maximum": 10}
                        },
                        "required": ["idea", "feasibility", "impact"]
                    },
                    "description": "アイデア評価のリスト"
                }
            },
            "required": ["session_id", "idea_evaluations"]
        }
    ),
    Tool(
        name="scamper_get_session",
        description="SCAMPERセッションの現在の状況を取得する",
        inputSchema={
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "string",
                    "description": "SCAMPERセッションのID"
                }
            },
            "required": ["session_id"]
        }
    ),
    Tool(
        name="scamper_list_sessions", 
        description="すべてのSCAMPERセッションの一覧を取得する",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    Tool(
        name="scamper_generate_comprehensive",
        description="全てのSCAMPER技法を適用して包括的なアイデアを生成する",
        inputSchema={
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "創造的思考を適用したいトピックや課題"
                },
                "current_situation": {
                    "type": "string",
                    "description": "現在の状況や問題の詳細"
                },
                "context": {
                    "type": "string",
                    "description": "背景情報や制約条件（オプション）"
                }
            },
            "required": ["topic", "current_situation"]
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
        elif name == "why_analysis_start":
            result = await why_analysis.start_analysis(
                arguments["problem"],
                arguments.get("context")
            )
        elif name == "why_analysis_add_answer":
            result = await why_analysis.add_answer(
                arguments["analysis_id"],
                arguments["level"],
                arguments["answer"]
            )
        elif name == "why_analysis_get":
            result = await why_analysis.get_analysis(arguments["analysis_id"])
        elif name == "why_analysis_list":
            result = await why_analysis.list_analyses()
        elif name == "mece_analyze_categories":
            result = await mece.analyze_categories(
                arguments["topic"],
                arguments["categories"]
            )
        elif name == "mece_create_structure":
            result = await mece.create_mece_structure(
                arguments["topic"],
                arguments.get("framework", "auto")
            )
        elif name == "dialectical_start_process":
            result = await dialectical.start_dialectical_process(
                arguments["topic"],
                arguments.get("context")
            )
        elif name == "dialectical_set_thesis":
            result = await dialectical.set_thesis(
                arguments["process_id"],
                arguments["thesis"],
                arguments.get("evidence")
            )
        elif name == "dialectical_set_antithesis":
            result = await dialectical.set_antithesis(
                arguments["process_id"],
                arguments["antithesis"],
                arguments.get("evidence")
            )
        elif name == "dialectical_create_synthesis":
            result = await dialectical.create_synthesis(
                arguments["process_id"],
                arguments["synthesis"],
                arguments.get("reasoning")
            )
        elif name == "dialectical_analyze_contradiction":
            result = await dialectical.analyze_contradiction(
                arguments["topic"],
                arguments["position_a"],
                arguments["position_b"]
            )
        elif name == "dialectical_get_process":
            result = await dialectical.get_process(arguments["process_id"])
        elif name == "dialectical_list_processes":
            result = await dialectical.list_processes()
        elif name == "sequential_thinking":
            result = await sequential.process_thought(arguments)
        elif name == "scamper_start_session":
            result = await scamper.start_session(
                arguments["topic"],
                arguments["current_situation"],
                arguments.get("context")
            )
        elif name == "scamper_apply_technique":
            result = await scamper.apply_technique(
                arguments["session_id"],
                arguments["technique"],
                arguments["ideas"],
                arguments.get("explanations")
            )
        elif name == "scamper_evaluate_ideas":
            result = await scamper.evaluate_ideas(
                arguments["session_id"],
                arguments["idea_evaluations"]
            )
        elif name == "scamper_get_session":
            result = await scamper.get_session(arguments["session_id"])
        elif name == "scamper_list_sessions":
            result = await scamper.list_sessions()
        elif name == "scamper_generate_comprehensive":
            result = await scamper.generate_comprehensive_ideas(
                arguments["topic"],
                arguments["current_situation"],
                arguments.get("context")
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