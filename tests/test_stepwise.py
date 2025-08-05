"""段階的思考ツールのテスト"""

import pytest
from thinking_support.tools.stepwise import StepwiseThinking


@pytest.fixture
def stepwise():
    """StepwiseThinkingインスタンスを提供"""
    return StepwiseThinking()


@pytest.mark.asyncio
async def test_create_plan_programming(stepwise):
    """プログラミング問題の計画作成テスト"""
    problem = "Webアプリケーションを開発したい"
    result = await stepwise.create_plan(problem)
    
    assert "段階的実行計画を作成しました" in result
    assert "要件の明確化と分析" in result
    assert "設計とアーキテクチャの検討" in result
    assert "stepwise_execute_step" in result
    assert len(stepwise.plans) == 1


@pytest.mark.asyncio
async def test_create_plan_learning(stepwise):
    """学習問題の計画作成テスト"""
    problem = "Python言語を学習したい"
    context = "プログラミング初心者です"
    result = await stepwise.create_plan(problem, context)
    
    assert "学習目標の設定" in result
    assert "基礎知識の習得" in result
    assert "実践的な練習" in result
    assert context in result


@pytest.mark.asyncio
async def test_execute_step(stepwise):
    """ステップ実行テスト"""
    # まず計画を作成
    problem = "テスト問題を解決する"
    await stepwise.create_plan(problem)
    
    plan_id = list(stepwise.plans.keys())[0]
    result = await stepwise.execute_step(plan_id, 1, "第1ステップを完了しました")
    
    assert "ステップ 1 を完了しました" in result
    assert "進捗: 1/" in result
    assert "次のステップ" in result
    
    # 計画の状態を確認
    plan = stepwise.plans[plan_id]
    assert plan.steps[0].status == "completed"
    assert plan.steps[0].result == "第1ステップを完了しました"


@pytest.mark.asyncio
async def test_execute_step_invalid_plan(stepwise):
    """無効な計画IDでのステップ実行テスト"""
    result = await stepwise.execute_step("invalid-id", 1, "結果")
    assert "エラー: 計画ID 'invalid-id' が見つかりません" in result


@pytest.mark.asyncio
async def test_execute_step_invalid_step(stepwise):
    """無効なステップ番号でのテスト"""
    problem = "テスト問題"
    await stepwise.create_plan(problem)
    plan_id = list(stepwise.plans.keys())[0]
    
    result = await stepwise.execute_step(plan_id, 999, "結果")
    assert "エラー: ステップ 999 が見つかりません" in result


@pytest.mark.asyncio
async def test_complete_all_steps(stepwise):
    """全ステップ完了テスト"""
    problem = "テスト問題"
    await stepwise.create_plan(problem)
    plan_id = list(stepwise.plans.keys())[0]
    plan = stepwise.plans[plan_id]
    
    # 全ステップを実行
    for i in range(len(plan.steps)):
        result = await stepwise.execute_step(plan_id, i + 1, f"ステップ{i + 1}完了")
    
    assert "🎉 すべてのステップが完了しました" in result
    assert "実行サマリー" in result
    assert plan.completed_at is not None


def test_step_types():
    """異なる問題タイプでのステップ生成テスト"""
    stepwise = StepwiseThinking()
    
    # プログラミング問題
    prog_steps = stepwise._create_programming_steps("アプリ開発")
    assert any("要件" in step.description for step in prog_steps)
    
    # 学習問題
    learn_steps = stepwise._create_learning_steps("言語学習")
    assert any("学習目標" in step.description for step in learn_steps)
    
    # 問題解決
    solve_steps = stepwise._create_problem_solving_steps("課題解決")
    assert any("問題の明確化" in step.description for step in solve_steps)