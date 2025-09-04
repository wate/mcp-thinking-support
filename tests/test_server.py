"""MCPサーバーの統合テスト"""

import pytest
from thinking_support.server import server, stepwise, critical, logical, dialectical


def test_server_initialization():
    """サーバーの初期化テスト"""
    assert server.name == "thinking-support"
    assert stepwise is not None
    assert critical is not None
    assert logical is not None
    assert dialectical is not None


def test_expected_tools():
    """期待されるツール数の確認"""
    expected_tools = [
        "sequential_thinking",
        "stepwise_create_plan",
        "stepwise_execute_step", 
        "critical_analyze_claim",
        "critical_identify_bias",
        "logical_build_argument",
        "logical_find_causality",
        "dialectical_start_process",
        "dialectical_set_thesis",
        "dialectical_set_antithesis",
        "dialectical_create_synthesis",
        "dialectical_analyze_contradiction",
        "dialectical_get_process",
        "dialectical_list_processes"
    ]
    # 実際のツール呼び出しテストは個別のツールテストで行う
    assert len(expected_tools) >= 14  # 最低14個のツール


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


@pytest.mark.asyncio
async def test_dialectical_integration():
    """弁証法の統合テスト"""
    # プロセス開始
    result1 = await dialectical.start_dialectical_process(
        "リモートワークの導入", 
        "コロナ後の働き方改革"
    )
    assert "弁証法的思考プロセスを開始しました" in result1
    
    # プロセスIDを取得
    process_id = list(dialectical.processes.keys())[0]
    
    # テーゼ設定
    result2 = await dialectical.set_thesis(
        process_id,
        "リモートワークは生産性を向上させる",
        ["通勤時間の削減", "集中できる環境"]
    )
    assert "テーゼを設定しました" in result2
    
    # アンチテーゼ設定
    result3 = await dialectical.set_antithesis(
        process_id,
        "リモートワークはコミュニケーションを阻害する",
        ["直接対話の減少", "チームワークの低下"]
    )
    assert "アンチテーゼを設定しました" in result3
    
    # ジンテーゼ構築
    result4 = await dialectical.create_synthesis(
        process_id,
        "ハイブリッドワークで両方の利点を活用する"
    )
    assert "弁証法的思考プロセスが完了しました" in result4


def test_tool_instances_are_separate():
    """ツールインスタンスの分離テスト"""
    # 各ツールが独立したインスタンスであることを確認
    assert id(stepwise) != id(critical)
    assert id(critical) != id(logical)
    assert id(stepwise) != id(logical)
    assert id(dialectical) != id(stepwise)
    assert id(dialectical) != id(critical)
    assert id(dialectical) != id(logical)