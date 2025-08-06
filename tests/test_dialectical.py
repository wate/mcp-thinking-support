"""弁証法ツールのテスト"""

import pytest
from thinking_support.tools.dialectical import DialecticalThinking


@pytest.fixture
def dialectical():
    """DialecticalThinkingインスタンスを提供"""
    return DialecticalThinking()


@pytest.mark.asyncio
async def test_start_dialectical_process(dialectical):
    """弁証法プロセス開始テスト"""
    topic = "環境保護と経済発展の関係"
    result = await dialectical.start_dialectical_process(topic)
    
    assert "弁証法的思考プロセスを開始しました" in result
    assert topic in result
    assert "テーゼ（正）の設定" in result
    assert "アンチテーゼ（反）の提示" in result
    assert "ジンテーゼ（合）の構築" in result
    assert "dialectical_set_thesis" in result
    assert len(dialectical.processes) == 1


@pytest.mark.asyncio
async def test_start_process_with_context(dialectical):
    """背景情報付きプロセス開始テスト"""
    topic = "リモートワークの是非"
    context = "COVID-19後の働き方改革"
    result = await dialectical.start_dialectical_process(topic, context)
    
    assert topic in result
    assert context in result


@pytest.mark.asyncio
async def test_set_thesis(dialectical):
    """テーゼ設定テスト"""
    topic = "AI技術の発展"
    await dialectical.start_dialectical_process(topic)
    process_id = list(dialectical.processes.keys())[0]
    
    thesis = "AI技術は人類の生活を向上させる"
    evidence = ["効率性の向上", "医療診断の精度向上", "危険作業の自動化"]
    result = await dialectical.set_thesis(process_id, thesis, evidence)
    
    assert "テーゼを設定しました" in result
    assert thesis in result
    assert "効率性の向上" in result
    assert "dialectical_set_antithesis" in result
    
    process = dialectical.processes[process_id]
    assert process.thesis is not None
    assert process.thesis.content == thesis
    assert process.thesis.evidence == evidence


@pytest.mark.asyncio
async def test_set_antithesis(dialectical):
    """アンチテーゼ設定テスト"""
    topic = "AI技術の発展"
    await dialectical.start_dialectical_process(topic)
    process_id = list(dialectical.processes.keys())[0]
    
    # まずテーゼを設定
    thesis = "AI技術は人類の生活を向上させる"
    await dialectical.set_thesis(process_id, thesis)
    
    # アンチテーゼを設定
    antithesis = "AI技術は人間の仕事を奪い社会問題を引き起こす"
    evidence = ["雇用の減少", "プライバシーの侵害", "意思決定の不透明性"]
    result = await dialectical.set_antithesis(process_id, antithesis, evidence)
    
    assert "アンチテーゼを設定しました" in result
    assert thesis in result
    assert antithesis in result
    assert "雇用の減少" in result
    assert "dialectical_create_synthesis" in result
    
    process = dialectical.processes[process_id]
    assert process.antithesis is not None
    assert process.antithesis.content == antithesis


@pytest.mark.asyncio
async def test_create_synthesis(dialectical):
    """ジンテーゼ構築テスト"""
    topic = "AI技術の発展"
    await dialectical.start_dialectical_process(topic)
    process_id = list(dialectical.processes.keys())[0]
    
    # テーゼとアンチテーゼを設定
    thesis = "AI技術は人類の生活を向上させる"
    antithesis = "AI技術は人間の仕事を奪い社会問題を引き起こす"
    await dialectical.set_thesis(process_id, thesis)
    await dialectical.set_antithesis(process_id, antithesis)
    
    # ジンテーゼを構築
    synthesis = "AI技術の適切な規制と教育により、利益を最大化し害を最小化できる"
    reasoning = "技術の進歩は避けられないが、適切な管理により負の側面を軽減可能"
    result = await dialectical.create_synthesis(process_id, synthesis, reasoning)
    
    assert "弁証法的思考プロセスが完了しました" in result
    assert thesis in result
    assert antithesis in result
    assert synthesis in result
    assert reasoning in result
    assert "弁証法的思考の成果" in result
    
    process = dialectical.processes[process_id]
    assert process.synthesis is not None
    assert process.synthesis.content == synthesis
    assert process.completed_at is not None


@pytest.mark.asyncio
async def test_set_thesis_invalid_process(dialectical):
    """無効なプロセスIDでのテーゼ設定テスト"""
    result = await dialectical.set_thesis("invalid-id", "テーゼ")
    assert "エラー: プロセスID 'invalid-id' が見つかりません" in result


@pytest.mark.asyncio
async def test_set_antithesis_without_thesis(dialectical):
    """テーゼなしでのアンチテーゼ設定テスト"""
    topic = "テストトピック"
    await dialectical.start_dialectical_process(topic)
    process_id = list(dialectical.processes.keys())[0]
    
    result = await dialectical.set_antithesis(process_id, "アンチテーゼ")
    assert "エラー: まずテーゼを設定してください" in result


@pytest.mark.asyncio
async def test_create_synthesis_incomplete_process(dialectical):
    """テーゼまたはアンチテーゼが不完全な状態でのジンテーゼ構築テスト"""
    topic = "テストトピック"
    await dialectical.start_dialectical_process(topic)
    process_id = list(dialectical.processes.keys())[0]
    
    result = await dialectical.create_synthesis(process_id, "ジンテーゼ")
    assert "エラー: テーゼとアンチテーゼの両方を設定してください" in result


@pytest.mark.asyncio
async def test_analyze_contradiction(dialectical):
    """矛盾分析テスト"""
    topic = "働き方改革"
    position_a = "効率性を重視すべき"
    position_b = "従業員の幸福を重視すべき"
    
    result = await dialectical.analyze_contradiction(topic, position_a, position_b)
    
    assert topic in result
    assert position_a in result
    assert position_b in result
    assert "矛盾点の分析" in result
    assert "統合への指針" in result
    assert "推奨する弁証法的アプローチ" in result
    assert "dialectical_start_process" in result


@pytest.mark.asyncio
async def test_get_process(dialectical):
    """プロセス状況取得テスト"""
    topic = "テストトピック"
    await dialectical.start_dialectical_process(topic)
    process_id = list(dialectical.processes.keys())[0]
    
    result = await dialectical.get_process(process_id)
    
    assert f"弁証法プロセスの状況 (ID: {process_id})" in result
    assert topic in result
    assert "⏳ テーゼ（正）: 未設定" in result
    assert "⏳ アンチテーゼ（反）: 未設定" in result
    assert "⏳ ジンテーゼ（合）: 未設定" in result
    assert "dialectical_set_thesis" in result


@pytest.mark.asyncio
async def test_get_process_with_progress(dialectical):
    """進行中プロセスの状況取得テスト"""
    topic = "テストトピック"
    await dialectical.start_dialectical_process(topic)
    process_id = list(dialectical.processes.keys())[0]
    
    # テーゼを設定
    await dialectical.set_thesis(process_id, "テストテーゼ")
    
    result = await dialectical.get_process(process_id)
    
    assert "✓ テーゼ（正）: テストテーゼ" in result
    assert "⏳ アンチテーゼ（反）: 未設定" in result
    assert "dialectical_set_antithesis" in result


@pytest.mark.asyncio
async def test_get_process_invalid_id(dialectical):
    """無効なプロセスIDでの状況取得テスト"""
    result = await dialectical.get_process("invalid-id")
    assert "エラー: プロセスID 'invalid-id' が見つかりません" in result


@pytest.mark.asyncio
async def test_list_processes_empty(dialectical):
    """空のプロセス一覧テスト"""
    result = await dialectical.list_processes()
    assert "現在、実行中の弁証法プロセスはありません" in result


@pytest.mark.asyncio
async def test_list_processes_with_data(dialectical):
    """データありプロセス一覧テスト"""
    topic1 = "トピック1"
    topic2 = "トピック2"
    await dialectical.start_dialectical_process(topic1)
    await dialectical.start_dialectical_process(topic2)
    
    result = await dialectical.list_processes()
    
    assert "弁証法プロセス一覧 (2件)" in result
    assert topic1 in result
    assert topic2 in result
    assert "進行中" in result


@pytest.mark.asyncio
async def test_full_dialectical_process(dialectical):
    """完全な弁証法プロセステスト"""
    topic = "民主主義と効率性"
    context = "政治制度の比較検討"
    
    # プロセス開始
    await dialectical.start_dialectical_process(topic, context)
    process_id = list(dialectical.processes.keys())[0]
    
    # テーゼ設定
    thesis = "民主主義は市民参加により公正な社会を実現する"
    await dialectical.set_thesis(process_id, thesis, ["市民の意見反映", "権力の分散"])
    
    # アンチテーゼ設定
    antithesis = "民主主義は意思決定が遅く効率的ではない"
    await dialectical.set_antithesis(process_id, antithesis, ["決定プロセスの複雑さ", "専門性の不足"])
    
    # ジンテーゼ構築
    synthesis = "参加型民主主義と専門的知見を組み合わせたハイブリッド制度が最適"
    result = await dialectical.create_synthesis(process_id, synthesis)
    
    # プロセス完了確認
    process = dialectical.processes[process_id]
    assert process.completed_at is not None
    
    # 最終状況確認
    status = await dialectical.get_process(process_id)
    assert "✅ プロセスは完了しています" in status
    assert "✓ テーゼ（正）" in status
    assert "✓ アンチテーゼ（反）" in status  
    assert "✓ ジンテーゼ（合）" in status