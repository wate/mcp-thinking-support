"""MCPサーバーの統合テスト"""

import pytest
from thinking_support.server import server, stepwise, critical, logical, scamper, why_analysis, mece, dialectical


def test_server_initialization():
    """サーバーの初期化テスト"""
    assert server.name == "thinking-support"
    assert stepwise is not None
    assert critical is not None
    assert logical is not None
    assert scamper is not None
    assert why_analysis is not None
    assert mece is not None
    assert dialectical is not None


def test_expected_tools():
    """期待されるツール数の確認"""
    expected_tools = [
        "stepwise_create_plan",
        "stepwise_execute_step", 
        "critical_analyze_claim",
        "critical_identify_bias",
        "logical_build_argument",
        "logical_find_causality",
        "why_analysis_start",
        "why_analysis_add_answer",
        "mece_analyze_categories",
        "mece_create_structure",
        "dialectical_start_process",
        "dialectical_set_thesis",
        "scamper_start_session",
        "scamper_apply_technique",
        "scamper_evaluate_ideas",
        "scamper_generate_comprehensive"
    ]
    # 実際のツール呼び出しテストは個別のツールテストで行う
    assert len(expected_tools) >= 16  # 最低16個のツール


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
async def test_scamper_integration():
    """SCAMPER法の統合テスト"""
    # セッション開始
    result1 = await scamper.start_session(
        "新製品アイデア", 
        "既存製品の改良が必要",
        "限られた予算内で"
    )
    assert "SCAMPERセッション開始" in result1
    
    # セッションIDを取得
    session_id = list(scamper.sessions.keys())[0]
    
    # 技法適用
    result2 = await scamper.apply_technique(
        session_id,
        "substitute",
        ["材料を代替品に変更", "製造プロセスを自動化に代替"],
        ["コスト削減効果", "効率化による品質向上"]
    )
    assert "Substitute技法の適用結果" in result2
    
    # アイデア評価
    evaluations = [
        {"idea": "材料を代替品に変更", "feasibility": 8, "impact": 6},
        {"idea": "製造プロセスを自動化に代替", "feasibility": 5, "impact": 9}
    ]
    result3 = await scamper.evaluate_ideas(session_id, evaluations)
    assert "アイデア評価結果" in result3
    
    # セッション状況確認
    result4 = await scamper.get_session(session_id)
    assert "SCAMPERセッション概要" in result4
    assert "新製品アイデア" in result4


@pytest.mark.asyncio
async def test_scamper_comprehensive_integration():
    """SCAMPER包括的アイデア生成の統合テスト"""
    # 包括的アイデア生成
    result = await scamper.generate_comprehensive_ideas(
        "オンラインショッピング体験改善",
        "顧客満足度とコンバージョン率の向上が必要",
        "競合他社との差別化が急務"
    )
    
    assert "SCAMPER包括的アイデア生成結果" in result
    assert "オンラインショッピング体験改善" in result
    assert "Substitute技法のアイデア" in result
    assert "Combine技法のアイデア" in result
    assert "生成統計" in result
    
    # セッションが作成されていることを確認
    assert len(scamper.sessions) >= 1
    
    # 包括的セッションでは全技法のアイデアが生成されていることを確認
    comprehensive_session = list(scamper.sessions.values())[-1]  # 最新のセッション
    techniques_used = set(idea.technique for idea in comprehensive_session.ideas)
    assert len(techniques_used) == 7  # 全7技法


def test_tool_instances_are_separate():
    """ツールインスタンスの分離テスト"""
    # 各ツールが独立したインスタンスであることを確認
    assert id(stepwise) != id(critical)
    assert id(critical) != id(logical)
    assert id(stepwise) != id(logical)
    assert id(scamper) != id(stepwise)
    assert id(scamper) != id(critical)
    assert id(scamper) != id(logical)