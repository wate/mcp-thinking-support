"""動的思考ツール（Sequential Thinking）のテスト"""

import pytest
import json
from thinking_support.tools.sequential import SequentialThinking, ThoughtData


@pytest.fixture
def sequential():
    """SequentialThinkingインスタンスを提供"""
    return SequentialThinking()


@pytest.mark.asyncio
async def test_basic_thought_processing(sequential):
    """基本的な思考処理テスト"""
    input_data = {
        "thought": "問題を整理する必要がある",
        "thought_number": 1,
        "total_thoughts": 3,
        "next_thought_needed": True
    }
    
    result = await sequential.process_thought(input_data)
    result_data = json.loads(result)
    
    assert result_data["thought_number"] == 1
    assert result_data["total_thoughts"] == 3
    assert result_data["next_thought_needed"] is True
    assert result_data["status"] == "success"
    assert len(sequential.thought_history) == 1


@pytest.mark.asyncio
async def test_thought_revision(sequential):
    """思考の修正機能テスト"""
    # 最初の思考
    first_thought = {
        "thought": "これが最初のアプローチだ",
        "thought_number": 1,
        "total_thoughts": 2,
        "next_thought_needed": True
    }
    await sequential.process_thought(first_thought)
    
    # 思考を修正
    revision = {
        "thought": "よく考えたら、別のアプローチの方が良い",
        "thought_number": 2,
        "total_thoughts": 3,
        "next_thought_needed": True,
        "is_revision": True,
        "revises_thought": 1
    }
    result = await sequential.process_thought(revision)
    result_data = json.loads(result)
    
    assert result_data["status"] == "success"
    assert len(sequential.thought_history) == 2
    assert sequential.thought_history[1].is_revision is True
    assert sequential.thought_history[1].revises_thought == 1


@pytest.mark.asyncio
async def test_thought_branching(sequential):
    """思考の分岐機能テスト"""
    # 最初の思考
    first_thought = {
        "thought": "分岐点となる思考",
        "thought_number": 1,
        "total_thoughts": 3,
        "next_thought_needed": True
    }
    await sequential.process_thought(first_thought)
    
    # 分岐した思考
    branch = {
        "thought": "別の方向で考えてみよう",
        "thought_number": 2,
        "total_thoughts": 4,
        "next_thought_needed": True,
        "branch_from_thought": 1,
        "branch_id": "alternative-approach"
    }
    result = await sequential.process_thought(branch)
    result_data = json.loads(result)
    
    assert result_data["status"] == "success"
    assert "alternative-approach" in result_data["branches"]
    assert len(sequential.branches["alternative-approach"]) == 1


@pytest.mark.asyncio
async def test_dynamic_thought_adjustment(sequential):
    """動的な思考数調整テスト"""
    # 思考数を超える場合
    input_data = {
        "thought": "予想より複雑だった",
        "thought_number": 5,
        "total_thoughts": 3,  # 思考数より大きい
        "next_thought_needed": True
    }
    
    result = await sequential.process_thought(input_data)
    result_data = json.loads(result)
    
    # 総思考数が自動調整されることを確認
    assert result_data["total_thoughts"] == 5
    assert result_data["status"] == "success"


@pytest.mark.asyncio
async def test_invalid_input_handling(sequential):
    """不正な入力のハンドリングテスト"""
    invalid_inputs = [
        {"thought_number": 1, "total_thoughts": 3, "next_thought_needed": True},  # thoughtが無い
        {"thought": "test", "total_thoughts": 3, "next_thought_needed": True},   # thought_numberが無い
        {"thought": "test", "thought_number": 1, "next_thought_needed": True},   # total_thoughtsが無い
        {"thought": "test", "thought_number": 1, "total_thoughts": 3},           # next_thought_neededが無い
    ]
    
    for invalid_input in invalid_inputs:
        result = await sequential.process_thought(invalid_input)
        result_data = json.loads(result)
        assert result_data["status"] == "failed"
        assert "error" in result_data


@pytest.mark.asyncio
async def test_thought_history_tracking(sequential):
    """思考履歴の追跡テスト"""
    thoughts = [
        {
            "thought": "最初の思考",
            "thought_number": 1,
            "total_thoughts": 3,
            "next_thought_needed": True
        },
        {
            "thought": "続きの思考",
            "thought_number": 2,
            "total_thoughts": 3,
            "next_thought_needed": True
        },
        {
            "thought": "最後の思考",
            "thought_number": 3,
            "total_thoughts": 3,
            "next_thought_needed": False
        }
    ]
    
    for thought in thoughts:
        await sequential.process_thought(thought)
    
    assert len(sequential.thought_history) == 3
    assert sequential.thought_history[0].thought == "最初の思考"
    assert sequential.thought_history[1].thought == "続きの思考"
    assert sequential.thought_history[2].thought == "最後の思考"
    assert sequential.thought_history[2].next_thought_needed is False


@pytest.mark.asyncio
async def test_complex_branching_scenario(sequential):
    """複雑な分岐シナリオテスト"""
    # 基本思考
    await sequential.process_thought({
        "thought": "複雑な問題に直面している",
        "thought_number": 1,
        "total_thoughts": 5,
        "next_thought_needed": True
    })
    
    # 第一の分岐
    await sequential.process_thought({
        "thought": "技術的アプローチを考える",
        "thought_number": 2,
        "total_thoughts": 5,
        "next_thought_needed": True,
        "branch_from_thought": 1,
        "branch_id": "technical"
    })
    
    # 第二の分岐
    await sequential.process_thought({
        "thought": "ビジネス的アプローチを考える",
        "thought_number": 2,
        "total_thoughts": 5,
        "next_thought_needed": True,
        "branch_from_thought": 1,
        "branch_id": "business"
    })
    
    # 技術分岐の続き
    await sequential.process_thought({
        "thought": "具体的な技術選択を検討",
        "thought_number": 3,
        "total_thoughts": 5,
        "next_thought_needed": True,
        "branch_from_thought": 2,
        "branch_id": "technical"
    })
    
    assert len(sequential.branches) == 2
    assert "technical" in sequential.branches
    assert "business" in sequential.branches
    assert len(sequential.branches["technical"]) == 2
    assert len(sequential.branches["business"]) == 1


@pytest.mark.asyncio
async def test_thought_data_validation(sequential):
    """ThoughtDataのバリデーションテスト"""
    # 正常なデータ
    valid_data = {
        "thought": "テスト思考",
        "thought_number": 1,
        "total_thoughts": 2,
        "next_thought_needed": True,
        "is_revision": False,
        "branch_id": "test-branch"
    }
    
    thought_data = sequential.validate_thought_data(valid_data)
    
    assert isinstance(thought_data, ThoughtData)
    assert thought_data.thought == "テスト思考"
    assert thought_data.thought_number == 1
    assert thought_data.total_thoughts == 2
    assert thought_data.next_thought_needed is True
    assert thought_data.is_revision is False
    assert thought_data.branch_id == "test-branch"


def test_format_thought(sequential):
    """思考のフォーマット表示テスト"""
    thought_data = ThoughtData(
        thought="これはテスト思考です",
        thought_number=1,
        total_thoughts=3,
        next_thought_needed=True
    )
    
    formatted = sequential.format_thought(thought_data)
    
    assert "💭 思考 1/3" in formatted
    assert "これはテスト思考です" in formatted
    assert "┌" in formatted and "┐" in formatted  # ボーダー確認


def test_format_thought_revision(sequential):
    """修正思考のフォーマット表示テスト"""
    thought_data = ThoughtData(
        thought="修正された思考です",
        thought_number=2,
        total_thoughts=3,
        next_thought_needed=True,
        is_revision=True,
        revises_thought=1
    )
    
    formatted = sequential.format_thought(thought_data)
    
    assert "🔄 修正 2/3" in formatted
    assert "(思考1を修正)" in formatted
    assert "修正された思考です" in formatted


def test_format_thought_branch(sequential):
    """分岐思考のフォーマット表示テスト"""
    thought_data = ThoughtData(
        thought="分岐した思考です",
        thought_number=2,
        total_thoughts=4,
        next_thought_needed=True,
        branch_from_thought=1,
        branch_id="alternative"
    )
    
    formatted = sequential.format_thought(thought_data)
    
    assert "🌿 分岐 2/4" in formatted
    assert "(思考1から分岐, ID: alternative)" in formatted
    assert "分岐した思考です" in formatted


def test_history_management(sequential):
    """履歴管理機能テスト"""
    # 履歴追加
    thought_data = ThoughtData(
        thought="テスト思考",
        thought_number=1,
        total_thoughts=2,
        next_thought_needed=True
    )
    sequential.thought_history.append(thought_data)
    
    # 履歴取得
    history = sequential.get_thought_history()
    assert len(history) == 1
    assert history[0].thought == "テスト思考"
    
    # 分岐履歴追加
    sequential.branches["test"] = [thought_data]
    branches = sequential.get_branches()
    assert "test" in branches
    assert len(branches["test"]) == 1
    
    # 履歴クリア
    sequential.clear_history()
    assert len(sequential.thought_history) == 0
    assert len(sequential.branches) == 0