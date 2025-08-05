"""クリティカルシンキングツールのテスト"""

import pytest
from thinking_support.tools.critical import CriticalThinking, SourceType, ReliabilityLevel, BiasType


@pytest.fixture
def critical():
    """CriticalThinkingインスタンスを提供"""
    return CriticalThinking()


@pytest.mark.asyncio
async def test_analyze_claim_academic_source(critical):
    """学術的情報源の主張分析テスト"""
    claim = "研究によると、この手法は効果的である"
    source = "https://example.ac.jp/research"
    result = await critical.analyze_claim(claim, source)
    
    assert "批判的分析結果" in result
    assert "学術論文" in result
    assert "研究やデータに基づいている可能性" in result
    assert "検討すべき質問" in result
    assert len(critical.analyses) == 1


@pytest.mark.asyncio
async def test_analyze_claim_social_media_source(critical):
    """ソーシャルメディア情報源の分析テスト"""
    claim = "みんなが絶対にこれは正しいと思う"
    source = "https://twitter.com/user"
    result = await critical.analyze_claim(claim, source)
    
    assert "ソーシャルメディア" in result
    assert "過度な一般化の可能性" in result
    assert "断定的すぎる表現" in result


@pytest.mark.asyncio
async def test_analyze_claim_no_source(critical):
    """情報源なしの分析テスト"""
    claim = "データに基づくと、この結論が導ける"
    result = await critical.analyze_claim(claim)
    
    assert "情報源タイプ: 不明" in result
    assert "研究やデータに基づいている可能性" in result


@pytest.mark.asyncio
async def test_identify_bias_confirmation(critical):
    """確証バイアスの特定テスト"""
    content = "やっぱり私の考えが正しかった。当然の結果だ。"
    result = await critical.identify_bias(content)
    
    assert "確証バイアス" in result
    assert "自分の信念を支持する情報のみを重視している" in result
    assert len(critical.bias_analyses) == 1


@pytest.mark.asyncio
async def test_identify_bias_authority(critical):
    """権威への訴えの特定テスト"""
    content = "専門家が言うから間違いない。有名人も推奨している。"
    result = await critical.identify_bias(content)
    
    assert "権威への訴え" in result
    assert "権威者の意見を無批判に受け入れている" in result


@pytest.mark.asyncio
async def test_identify_bias_bandwagon(critical):
    """バンドワゴン効果の特定テスト"""
    content = "みんながやっているから正しい。今の流行りだし。"
    result = await critical.identify_bias(content)
    
    assert "バンドワゴン効果" in result
    assert "多数派の意見に同調している" in result


@pytest.mark.asyncio
async def test_identify_logical_fallacies(critical):
    """論理的誤謬の特定テスト"""
    content = "AかBかしかない。白か黒かはっきりしろ。だからすべてがダメだ。"
    result = await critical.identify_bias(content)
    
    assert "偽の二分法" in result
    assert "早まった一般化" in result


@pytest.mark.asyncio
async def test_no_bias_detected(critical):
    """バイアスが検出されない場合のテスト"""
    content = "複数の観点から検討した結果、以下の結論に至りました。"
    result = await critical.identify_bias(content)
    
    assert "明確なバイアスや論理的誤謬は検出されませんでした" in result


def test_source_classification():
    """情報源分類のテスト"""
    critical = CriticalThinking()
    
    assert critical._classify_source("https://example.ac.jp") == SourceType.ACADEMIC
    assert critical._classify_source("https://twitter.com/user") == SourceType.SOCIAL_MEDIA
    assert critical._classify_source("https://gov.example") == SourceType.GOVERNMENT
    assert critical._classify_source("https://news.example.com") == SourceType.NEWS_MEDIA
    assert critical._classify_source("https://blog.example.com") == SourceType.PERSONAL_BLOG
    assert critical._classify_source(None) == SourceType.UNKNOWN


def test_reliability_assessment():
    """信頼性評価のテスト"""
    critical = CriticalThinking()
    
    # 高い信頼性（学術的情報源 + 強み）
    from thinking_support.tools.critical import ClaimAnalysis
    analysis = ClaimAnalysis("テスト主張")
    analysis.source_type = SourceType.ACADEMIC
    analysis.strengths = ["根拠あり", "専門的"]
    analysis.weaknesses = []
    
    reliability = critical._assess_reliability(analysis)
    assert reliability == ReliabilityLevel.HIGH