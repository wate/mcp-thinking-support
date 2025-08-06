"""5Why分析ツールのテスト"""

import pytest
from thinking_support.tools.why_analysis import WhyAnalysis


@pytest.fixture
def why_analysis():
    """WhyAnalysisインスタンスを提供"""
    return WhyAnalysis()


@pytest.mark.asyncio
async def test_start_analysis(why_analysis):
    """分析開始テスト"""
    problem = "システムが頻繁にダウンする"
    result = await why_analysis.start_analysis(problem)
    
    assert "5Why分析を開始しました" in result
    assert problem in result
    assert "分析ID" in result
    assert "なぜ「システムが頻繁にダウンする」が起こったのか？" in result
    assert len(why_analysis.analyses) == 1


@pytest.mark.asyncio
async def test_start_analysis_with_context(why_analysis):
    """コンテキスト付き分析開始テスト"""
    problem = "売上が低下している"
    context = "コロナ禍の影響で外出自粛が続いている"
    result = await why_analysis.start_analysis(problem, context)
    
    assert problem in result
    assert context in result
    assert "背景" in result


@pytest.mark.asyncio
async def test_add_answer_sequence(why_analysis):
    """回答追加の連続テスト"""
    problem = "社員の離職率が高い"
    result = await why_analysis.start_analysis(problem)
    analysis_id = list(why_analysis.analyses.keys())[0]
    
    # レベル0の回答
    result = await why_analysis.add_answer(analysis_id, 0, "労働環境が悪いから")
    assert "レベル 1 の回答を記録しました" in result
    assert "なぜ「労働環境が悪いから」なのか？" in result
    
    # レベル1の回答
    result = await why_analysis.add_answer(analysis_id, 1, "長時間労働が常態化しているから")
    assert "レベル 2 の回答を記録しました" in result
    assert "なぜ「長時間労働が常態化しているから」なのか？" in result


@pytest.mark.asyncio
async def test_complete_analysis(why_analysis):
    """完全な5Why分析テスト"""
    problem = "製品の品質問題が発生している"
    result = await why_analysis.start_analysis(problem)
    analysis_id = list(why_analysis.analyses.keys())[0]
    
    answers = [
        "検査工程でのチェックが不十分だから",
        "検査員の技術レベルが低いから", 
        "十分な研修が行われていないから",
        "研修プログラムが古いから",
        "技術の進歩に研修が追いついていないから"
    ]
    
    # 5回の回答を順番に入力
    for i, answer in enumerate(answers):
        result = await why_analysis.add_answer(analysis_id, i, answer)
        if i < 4:
            assert f"次の質問 (レベル {i + 2})" in result
        else:
            assert "5Why分析が完了しました" in result
            assert "分析要約" in result
            assert "根本原因" in result
    
    # 分析のステータスが完了になっていることを確認
    analysis = why_analysis.analyses[analysis_id]
    assert analysis["status"] == "completed"


@pytest.mark.asyncio
async def test_get_analysis(why_analysis):
    """分析取得テスト"""
    problem = "顧客満足度が低い"
    await why_analysis.start_analysis(problem)
    analysis_id = list(why_analysis.analyses.keys())[0]
    
    # 最初の回答を追加
    await why_analysis.add_answer(analysis_id, 0, "サービスの質が低いから")
    
    result = await why_analysis.get_analysis(analysis_id)
    assert "5Why分析の状況" in result
    assert problem in result
    assert "サービスの質が低いから" in result
    assert "（未回答）" in result  # まだ回答していない質問があること


@pytest.mark.asyncio
async def test_list_analyses(why_analysis):
    """分析一覧テスト"""
    # 最初は空の一覧
    result = await why_analysis.list_analyses()
    assert "作成された分析はありません" in result
    
    # 複数の分析を作成
    await why_analysis.start_analysis("問題1")
    await why_analysis.start_analysis("問題2") 
    
    result = await why_analysis.list_analyses()
    assert "5Why分析一覧" in result
    assert "問題1" in result
    assert "問題2" in result
    assert "進捗" in result


@pytest.mark.asyncio
async def test_invalid_analysis_id(why_analysis):
    """無効な分析IDのテスト"""
    result = await why_analysis.add_answer("invalid-id", 0, "回答")
    assert "分析ID 'invalid-id' が見つかりません" in result
    
    result = await why_analysis.get_analysis("invalid-id")
    assert "分析ID 'invalid-id' が見つかりません" in result


@pytest.mark.asyncio
async def test_invalid_level(why_analysis):
    """無効なレベルのテスト"""
    problem = "問題"
    await why_analysis.start_analysis(problem)
    analysis_id = list(why_analysis.analyses.keys())[0]
    
    result = await why_analysis.add_answer(analysis_id, 5, "回答")
    assert "レベル 5 の質問が存在しません" in result


@pytest.mark.asyncio
async def test_duplicate_answer(why_analysis):
    """重複回答のテスト"""
    problem = "問題"
    await why_analysis.start_analysis(problem)
    analysis_id = list(why_analysis.analyses.keys())[0]
    
    # 最初の回答
    await why_analysis.add_answer(analysis_id, 0, "最初の回答")
    
    # 同じレベルに再度回答を試行
    result = await why_analysis.add_answer(analysis_id, 0, "二回目の回答")
    assert "すでに回答済みです" in result


@pytest.mark.asyncio
async def test_analysis_summary_generation(why_analysis):
    """分析要約生成のテスト"""
    problem = "テスト問題"
    await why_analysis.start_analysis(problem)
    analysis_id = list(why_analysis.analyses.keys())[0]
    
    # 全ての回答を完了
    answers = ["回答1", "回答2", "回答3", "回答4", "回答5"]
    for i, answer in enumerate(answers):
        await why_analysis.add_answer(analysis_id, i, answer)
    
    result = await why_analysis.get_analysis(analysis_id)
    assert "分析要約" in result
    assert "根本問題" in result
    assert "分析経路" in result
    assert "根本原因" in result
    assert "推奨アクション" in result
    assert answers[-1] in result  # 最後の回答が根本原因として表示される


@pytest.mark.asyncio
async def test_analysis_progress_tracking(why_analysis):
    """分析進捗追跡のテスト"""
    problem = "進捗テスト問題"
    await why_analysis.start_analysis(problem)
    analysis_id = list(why_analysis.analyses.keys())[0]
    
    # 部分的に回答
    await why_analysis.add_answer(analysis_id, 0, "回答1")
    await why_analysis.add_answer(analysis_id, 1, "回答2")
    
    result = await why_analysis.list_analyses()
    assert "2/" in result  # 進捗が表示されること
    assert "🔄" in result  # 進行中のアイコンが表示されること