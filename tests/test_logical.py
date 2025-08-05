"""ロジカルシンキングツールのテスト"""

import pytest
from thinking_support.tools.logical import LogicalThinking, ArgumentType, LogicalStructure, CausalRelationType


@pytest.fixture
def logical():
    """LogicalThinkingインスタンスを提供"""
    return LogicalThinking()


@pytest.mark.asyncio
async def test_build_deductive_argument(logical):
    """演繹的推論の論証構築テスト"""
    premises = [
        "すべての人間は死ぬ",
        "ソクラテスは人間である"
    ]
    conclusion = "ソクラテスは死ぬ"
    
    result = await logical.build_argument(premises, conclusion)
    
    assert "論理的論証分析" in result
    assert "演繹的推論" in result
    assert "三段論法" in result
    assert "妥当" in result
    assert "健全" in result
    assert len(logical.arguments) == 1


@pytest.mark.asyncio
async def test_build_inductive_argument(logical):
    """帰納的推論の論証構築テスト"""
    premises = [
        "過去の統計によると成功率は80%である",
        "同様の条件が揃っている"
    ]
    conclusion = "おそらく成功するだろう"
    
    result = await logical.build_argument(premises, conclusion)
    
    assert "帰納的推論" in result
    assert "前提から結論の蓋然性を推定" in result


@pytest.mark.asyncio
async def test_build_conditional_argument(logical):
    """条件文を含む論証のテスト"""
    premises = [
        "もし雨が降るならば試合は中止される",
        "雨が降っている"
    ]
    conclusion = "試合は中止される"
    
    result = await logical.build_argument(premises, conclusion)
    
    assert "モーダス・ポネンス" in result


@pytest.mark.asyncio
async def test_find_causality_economic(logical):
    """経済状況の因果関係分析テスト"""
    situation = "経済成長率が低下している"
    factors = ["金利上昇", "消費者信頼度低下", "輸出減少"]
    
    result = await logical.find_causality(situation, factors)
    
    assert "因果関係分析" in result
    assert "主要な原因" in result
    assert "経済状況" in result
    assert "市場環境" in result
    assert len(logical.causal_analyses) == 1


@pytest.mark.asyncio
async def test_find_causality_health(logical):
    """健康問題の因果関係分析テスト"""
    situation = "健康状態が悪化している"
    
    result = await logical.find_causality(situation)
    
    assert "生活習慣" in result
    assert "遺伝的要因" in result
    assert "環境要因" in result


@pytest.mark.asyncio
async def test_find_causality_learning(logical):
    """学習問題の因果関係分析テスト"""
    situation = "学習成果が上がらない"
    factors = ["勉強時間不足", "集中力低下"]
    
    result = await logical.find_causality(situation, factors)
    
    assert "学習時間" in result
    assert "学習方法" in result
    # 提供された要因は副次的原因として表示される場合がある
    assert ("勉強時間不足" in result or "環境" in result)


@pytest.mark.asyncio
async def test_find_causality_no_factors(logical):
    """要因なしの因果関係分析テスト"""
    situation = "一般的な問題が発生している"
    
    result = await logical.find_causality(situation)
    
    assert "追加情報が必要かもしれません" in result


def test_argument_type_analysis():
    """論証タイプ分析のテスト"""
    logical = LogicalThinking()
    
    # 演繹的推論
    deductive_type = logical._analyze_argument_type(
        ["すべての人間は死ぬ"], "ソクラテスは死ぬ"
    )
    assert deductive_type == ArgumentType.DEDUCTIVE
    
    # 帰納的推論
    inductive_type = logical._analyze_argument_type(
        ["統計によるとおそらく"], "結論が導ける"
    )
    assert inductive_type == ArgumentType.INDUCTIVE


def test_logical_structure_identification():
    """論理構造特定のテスト"""
    logical = LogicalThinking()
    
    # モーダス・ポネンス
    modus_ponens = logical._identify_logical_structure(
        ["もし雨ならば中止"], "中止される"
    )
    assert modus_ponens == LogicalStructure.MODUS_PONENS
    
    # 因果連鎖
    causal = logical._identify_logical_structure(
        ["原因があるから"], "結果が生じる"
    )
    assert causal == LogicalStructure.CAUSAL_CHAIN


def test_validity_assessment():
    """妥当性評価のテスト"""
    logical = LogicalThinking()
    
    from thinking_support.tools.logical import LogicalArgument
    
    # 妥当な論証
    valid_arg = LogicalArgument(
        ["前提1", "前提2"], "結論"
    )
    valid_arg.logical_structure = LogicalStructure.MODUS_PONENS
    
    validity = logical._assess_validity(valid_arg)
    assert validity is True
    
    # 前提が少ない論証
    invalid_arg = LogicalArgument([], "結論")
    invalid_arg.logical_structure = LogicalStructure.MODUS_PONENS
    
    validity = logical._assess_validity(invalid_arg)
    assert validity is False