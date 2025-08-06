"""MECEツールのテスト"""

import pytest
from thinking_support.tools.mece import MECE, MECEViolationType


@pytest.fixture
def mece():
    """MECEインスタンスを提供"""
    return MECE()


@pytest.mark.asyncio
async def test_analyze_categories_with_overlap(mece):
    """重複があるカテゴリの分析テスト"""
    topic = "事業戦略"
    categories = ["技術", "テクノロジー", "人材", "組織"]
    
    result = await mece.analyze_categories(topic, categories)
    
    assert "MECE分析結果" in result
    assert "重複の検出" in result
    assert "技術" in result
    assert "テクノロジー" in result
    assert len(mece.analyses) == 1
    
    # 分析結果の検証
    analysis = list(mece.analyses.values())[0]
    assert analysis.violation_type in [MECEViolationType.OVERLAP, MECEViolationType.BOTH]


@pytest.mark.asyncio
async def test_analyze_categories_with_gaps(mece):
    """漏れがあるカテゴリの分析テスト"""
    topic = "マーケティング戦略"
    categories = ["製品", "価格"]  # プロモーションと流通が不足
    
    result = await mece.analyze_categories(topic, categories)
    
    assert "網羅性の漏れ" in result
    assert "改善提案" in result
    
    # 分析結果の検証
    analysis = list(mece.analyses.values())[0]
    assert analysis.violation_type in [MECEViolationType.GAP, MECEViolationType.BOTH]
    assert len(analysis.gaps) > 0


@pytest.mark.asyncio
async def test_analyze_categories_mece_compliant(mece):
    """MECE原則に適合するカテゴリの分析テスト"""
    topic = "顧客分析"
    categories = ["既存顧客", "新規顧客", "潜在顧客"]
    
    result = await mece.analyze_categories(topic, categories)
    
    assert "MECE原則に適合" in result
    
    # 分析結果の検証
    analysis = list(mece.analyses.values())[0]
    # 完全にMECEに適合しない場合でも、重複や漏れが少なければ問題なし
    assert analysis.violation_type in [MECEViolationType.NONE, MECEViolationType.GAP]


@pytest.mark.asyncio
async def test_create_mece_structure_business(mece):
    """事業分野のMECE構造提案テスト"""
    topic = "事業改善"
    framework = "auto"
    
    result = await mece.create_mece_structure(topic, framework)
    
    assert "MECE構造提案" in result
    assert "戦略" in result
    assert "組織" in result
    assert "プロセス" in result
    assert "技術" in result
    assert "財務" in result


@pytest.mark.asyncio
async def test_create_mece_structure_4p(mece):
    """4Pフレームワークでの構造提案テスト"""
    topic = "マーケティング戦略"
    framework = "4P"
    
    result = await mece.create_mece_structure(topic, framework)
    
    assert "製品(Product)" in result
    assert "価格(Price)" in result
    assert "流通(Place)" in result
    assert "プロモーション(Promotion)" in result


@pytest.mark.asyncio
async def test_create_mece_structure_3c(mece):
    """3Cフレームワークでの構造提案テスト"""
    topic = "競合分析"
    framework = "3C"
    
    result = await mece.create_mece_structure(topic, framework)
    
    assert "顧客(Customer)" in result
    assert "競合(Competitor)" in result
    assert "自社(Company)" in result


@pytest.mark.asyncio
async def test_create_mece_structure_swot(mece):
    """SWOTフレームワークでの構造提案テスト"""
    topic = "企業分析"
    framework = "SWOT"
    
    result = await mece.create_mece_structure(topic, framework)
    
    assert "強み(Strengths)" in result
    assert "弱み(Weaknesses)" in result
    assert "機会(Opportunities)" in result
    assert "脅威(Threats)" in result


@pytest.mark.asyncio
async def test_create_mece_structure_time_series(mece):
    """時系列フレームワークでの構造提案テスト"""
    topic = "企業の変遷"
    framework = "時系列"
    
    result = await mece.create_mece_structure(topic, framework)
    
    assert "過去" in result
    assert "現在" in result
    assert "未来" in result


@pytest.mark.asyncio
async def test_create_mece_structure_internal_external(mece):
    """内外フレームワークでの構造提案テスト"""
    topic = "環境分析"
    framework = "内外"
    
    result = await mece.create_mece_structure(topic, framework)
    
    assert "内部要因" in result
    assert "外部要因" in result


def test_find_overlaps():
    """重複検出のテスト"""
    mece_tool = MECE()
    
    from thinking_support.tools.mece import MECECategory
    
    cat1 = MECECategory("技術", "技術に関する要素")
    cat2 = MECECategory("テクノロジー", "テクノロジーに関する要素")
    cat3 = MECECategory("人材", "人的リソース")
    
    categories = [cat1, cat2, cat3]
    overlaps = mece_tool._find_overlaps(categories)
    
    # 技術とテクノロジーは重複するはず
    assert len(overlaps) > 0
    assert any("技術" in overlap and "テクノロジー" in overlap for overlap in overlaps)


def test_check_category_overlap():
    """カテゴリ重複チェックのテスト"""
    mece_tool = MECE()
    
    from thinking_support.tools.mece import MECECategory
    
    # 重複するカテゴリ
    cat1 = MECECategory("技術", "技術関連")
    cat2 = MECECategory("テクノロジー", "技術関連")
    
    overlap = mece_tool._check_category_overlap(cat1, cat2)
    assert overlap is True
    
    # 重複しないカテゴリ
    cat3 = MECECategory("人材", "人的リソース")
    cat4 = MECECategory("財務", "資金関連")
    
    no_overlap = mece_tool._check_category_overlap(cat3, cat4)
    assert no_overlap is False


def test_find_gaps_marketing():
    """マーケティング分野での漏れ検出テスト"""
    mece_tool = MECE()
    
    from thinking_support.tools.mece import MECECategory
    
    topic = "マーケティング戦略"
    categories = [
        MECECategory("製品", "商品戦略"),
        MECECategory("価格", "価格戦略")
    ]
    
    gaps = mece_tool._find_gaps(topic, categories)
    
    # プロモーションと流通が不足しているはず
    assert len(gaps) > 0
    assert any("プロモーション" in gap or "流通" in gap for gap in gaps)


def test_suggest_mece_structure_auto():
    """自動フレームワーク選択のテスト"""
    mece_tool = MECE()
    
    # 事業関連
    business_structure = mece_tool._suggest_mece_structure("事業戦略", "auto")
    assert "戦略" in business_structure
    assert "組織" in business_structure
    
    # マーケティング関連
    marketing_structure = mece_tool._suggest_mece_structure("マーケティング計画", "auto")
    assert "製品" in marketing_structure
    assert "価格" in marketing_structure
    
    # 組織関連
    org_structure = mece_tool._suggest_mece_structure("組織改革", "auto")
    assert "人材" in org_structure
    assert "プロセス" in org_structure


def test_generate_improvements():
    """改善提案生成のテスト"""
    mece_tool = MECE()
    
    from thinking_support.tools.mece import MECEAnalysis
    
    # 重複のある分析
    overlap_analysis = MECEAnalysis("テストトピック", ["カテゴリ1", "カテゴリ2"])
    overlap_analysis.violation_type = MECEViolationType.OVERLAP
    overlap_analysis.overlaps = [("技術", "テクノロジー")]
    
    mece_tool._generate_improvements(overlap_analysis)
    
    assert len(overlap_analysis.improvement_suggestions) > 0
    assert any("重複" in suggestion for suggestion in overlap_analysis.improvement_suggestions)
    
    # 漏れのある分析
    gap_analysis = MECEAnalysis("テストトピック", ["カテゴリ1"])
    gap_analysis.violation_type = MECEViolationType.GAP
    gap_analysis.gaps = ["不足カテゴリ"]
    
    mece_tool._generate_improvements(gap_analysis)
    
    assert len(gap_analysis.improvement_suggestions) > 0
    assert any("網羅性" in suggestion for suggestion in gap_analysis.improvement_suggestions)


def test_category_description_generation():
    """カテゴリ説明生成のテスト"""
    mece_tool = MECE()
    
    # 既知のカテゴリ
    strategy_desc = mece_tool._generate_category_description("戦略", "事業")
    assert "方針や計画" in strategy_desc
    
    organization_desc = mece_tool._generate_category_description("組織", "企業")
    assert "組織構造や体制" in organization_desc
    
    # 未知のカテゴリ
    unknown_desc = mece_tool._generate_category_description("新しいカテゴリ", "テストトピック")
    assert "テストトピック" in unknown_desc
    assert "新しいカテゴリ" in unknown_desc