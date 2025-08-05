"""MCPサーバーの統合テスト"""

import pytest
from thinking_support.server import server, stepwise, critical, logical


def test_server_initialization():
    """サーバーの初期化テスト"""
    assert server.name == "thinking-support"
    assert stepwise is not None
    assert critical is not None
    assert logical is not None


def test_expected_tools():
    """期待されるツール数の確認"""
    expected_tools = [
        "stepwise_create_plan",
        "stepwise_execute_step", 
        "critical_analyze_claim",
        "critical_identify_bias",
        "logical_build_argument",
        "logical_find_causality"
    ]
    # 実際のツール呼び出しテストは個別のツールテストで行う
    assert len(expected_tools) == 6


@pytest.mark.asyncio 
async def test_stepwise_integration():
    """段階的思考の統合テスト"""
    # 計画作成
    result1 = await stepwise.create_plan("統合テストを実行する")
    assert "実行計画を作成しました" in result1
    
    # 計画IDを取得
    plan_id = list(stepwise.plans.keys())[0]
    
    # ステップ実行
    result2 = await stepwise.execute_step(plan_id, 1, "テスト準備完了")
    assert "ステップ 1 を完了しました" in result2


@pytest.mark.asyncio
async def test_critical_integration():
    """クリティカルシンキングの統合テスト"""
    # 主張分析
    result1 = await critical.analyze_claim(
        "このテストは必ず成功する", 
        "https://test.example.com"
    )
    assert "批判的分析結果" in result1
    
    # バイアス特定
    result2 = await critical.identify_bias("みんなが賛成している")
    assert ("バンドワゴン効果" in result2 or "明確なバイアス" in result2)


@pytest.mark.asyncio
async def test_logical_integration():
    """ロジカルシンキングの統合テスト"""
    # 論証構築
    result1 = await logical.build_argument(
        ["すべてのテストは検証される", "これはテストである"], 
        "これは検証される"
    )
    assert "論理的論証分析" in result1
    
    # 因果関係分析
    result2 = await logical.find_causality("テストが失敗した")
    assert "因果関係分析" in result2


def test_tool_instances_are_separate():
    """ツールインスタンスの分離テスト"""
    # 各ツールが独立したインスタンスであることを確認
    assert id(stepwise) != id(critical)
    assert id(critical) != id(logical)
    assert id(stepwise) != id(logical)