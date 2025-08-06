"""MECE（Mutually Exclusive and Collectively Exhaustive）支援ツール"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class MECEViolationType(Enum):
    """MECE違反の種類"""
    OVERLAP = "重複（相互排他性違反）"
    GAP = "漏れ（網羅性違反）"
    BOTH = "重複と漏れの両方"
    NONE = "MECE原則に適合"


class MECECategory:
    """MECEカテゴリを表すクラス"""
    
    def __init__(self, name: str, description: str = ""):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.subcategories: List['MECECategory'] = []
        self.items: List[str] = []
        self.parent_id: Optional[str] = None


class MECEAnalysis:
    """MECE分析を表すクラス"""
    
    def __init__(self, topic: str, categories: List[str]):
        self.id = str(uuid.uuid4())
        self.topic = topic
        self.original_categories = categories
        self.mece_categories: List[MECECategory] = []
        self.violation_type = MECEViolationType.NONE
        self.overlaps: List[tuple] = []  # 重複しているカテゴリのペア
        self.gaps: List[str] = []  # 不足しているカテゴリ
        self.improvement_suggestions: List[str] = []
        self.analysis_notes: List[str] = []
        self.created_at = datetime.now()


class MECE:
    """MECEフレームワークをサポートするクラス"""
    
    def __init__(self):
        self.analyses: Dict[str, MECEAnalysis] = {}
    
    async def analyze_categories(self, topic: str, categories: List[str]) -> str:
        """カテゴリのMECE分析を実行する"""
        
        analysis = MECEAnalysis(topic, categories)
        
        # MECEカテゴリを構築
        self._build_mece_categories(analysis)
        
        # MECE違反を検証
        self._check_mece_violations(analysis)
        
        # 改善提案を生成
        self._generate_improvements(analysis)
        
        # 分析ノートを追加
        self._add_analysis_notes(analysis)
        
        # 分析を保存
        self.analyses[analysis.id] = analysis
        
        # 結果を整形して返す
        return self._format_analysis_result(analysis)
    
    async def create_mece_structure(self, topic: str, framework: str = "auto") -> str:
        """トピックに対するMECE構造を提案する"""
        
        analysis = MECEAnalysis(topic, [])
        
        # フレームワークに基づいて構造を生成
        suggested_categories = self._suggest_mece_structure(topic, framework)
        analysis.original_categories = suggested_categories
        
        # MECEカテゴリを構築
        self._build_mece_categories(analysis)
        
        # 分析ノートを追加
        analysis.analysis_notes.append(f"フレームワーク「{framework}」を使用して構造を提案")
        self._add_analysis_notes(analysis)
        
        # 分析を保存
        self.analyses[analysis.id] = analysis
        
        # 結果を整形して返す
        result = f"MECE構造提案 (ID: {analysis.id})\n\n"
        result += f"対象トピック: {topic}\n"
        result += f"使用フレームワーク: {framework}\n\n"
        
        result += "提案されるMECE構造:\n"
        for i, category in enumerate(analysis.mece_categories, 1):
            result += f"{i}. {category.name}\n"
            if category.description:
                result += f"   説明: {category.description}\n"
            if category.items:
                result += f"   含まれる要素: {', '.join(category.items)}\n"
            result += "\n"
        
        if analysis.analysis_notes:
            result += "分析メモ:\n"
            for note in analysis.analysis_notes:
                result += f"• {note}\n"
            result += "\n"
        
        result += "💡 MECEフレームワーク活用のポイント:\n"
        result += "• 各カテゴリが重複していないか確認する\n"
        result += "• 全体を網羅できているか検証する\n"
        result += "• カテゴリの粒度を統一する\n"
        result += "• 目的に応じて階層化を考慮する"
        
        return result
    
    def _build_mece_categories(self, analysis: MECEAnalysis):
        """MECEカテゴリを構築する"""
        
        for category_name in analysis.original_categories:
            category = MECECategory(category_name)
            
            # カテゴリの説明を自動生成
            category.description = self._generate_category_description(category_name, analysis.topic)
            
            # 関連する要素を推定
            category.items = self._estimate_category_items(category_name, analysis.topic)
            
            analysis.mece_categories.append(category)
    
    def _check_mece_violations(self, analysis: MECEAnalysis):
        """MECE違反をチェックする"""
        
        # 重複チェック（相互排他性）
        overlaps = self._find_overlaps(analysis.mece_categories)
        analysis.overlaps = overlaps
        
        # 漏れチェック（網羅性）
        gaps = self._find_gaps(analysis.topic, analysis.mece_categories)
        analysis.gaps = gaps
        
        # 違反タイプを決定
        if overlaps and gaps:
            analysis.violation_type = MECEViolationType.BOTH
        elif overlaps:
            analysis.violation_type = MECEViolationType.OVERLAP
        elif gaps:
            analysis.violation_type = MECEViolationType.GAP
        else:
            analysis.violation_type = MECEViolationType.NONE
    
    def _find_overlaps(self, categories: List[MECECategory]) -> List[tuple]:
        """カテゴリ間の重複を検出する"""
        
        overlaps = []
        
        for i, cat1 in enumerate(categories):
            for j, cat2 in enumerate(categories[i+1:], i+1):
                if self._check_category_overlap(cat1, cat2):
                    overlaps.append((cat1.name, cat2.name))
        
        return overlaps
    
    def _check_category_overlap(self, cat1: MECECategory, cat2: MECECategory) -> bool:
        """2つのカテゴリが重複するかチェックする"""
        
        # 名前の類似性チェック
        name1_lower = cat1.name.lower()
        name2_lower = cat2.name.lower()
        
        # 明確に異なる顧客カテゴリは重複しないものとする
        customer_categories = [
            ("既存顧客", "新規顧客"),
            ("既存顧客", "潜在顧客"),
            ("新規顧客", "潜在顧客")
        ]
        
        for cat_pair in customer_categories:
            if (cat_pair[0] in name1_lower and cat_pair[1] in name2_lower) or \
               (cat_pair[1] in name1_lower and cat_pair[0] in name2_lower):
                return False
        
        overlap_keywords = [
            ("技術", "テクノロジー"),
            ("人", "人材"),
            ("組織", "チーム"),
            ("財務", "金融"),
            ("マーケティング", "営業"),
            ("顧客", "クライアント")
        ]
        
        for keyword1, keyword2 in overlap_keywords:
            if (keyword1 in name1_lower and keyword2 in name2_lower) or \
               (keyword2 in name1_lower and keyword1 in name2_lower):
                return True
        
        # 共通する要素があるかチェック
        common_items = set(cat1.items) & set(cat2.items)
        return len(common_items) > 1  # 1個以上の共通要素で重複とする
    
    def _find_gaps(self, topic: str, categories: List[MECECategory]) -> List[str]:
        """網羅性の漏れを検出する"""
        
        gaps = []
        topic_lower = topic.lower()
        existing_names = [cat.name.lower() for cat in categories]
        
        # トピック別の典型的なカテゴリ
        common_frameworks = {
            "事業": ["戦略", "組織", "プロセス", "技術", "財務"],
            "マーケティング": ["製品", "価格", "流通", "プロモーション"],
            "組織": ["人材", "プロセス", "技術", "組織構造"],
            "問題": ["人", "プロセス", "技術", "環境"],
            "時間": ["過去", "現在", "未来"],
            "空間": ["内部", "外部"],
            "顧客": ["既存顧客", "新規顧客", "潜在顧客"]
        }
        
        # 適用可能なフレームワークを探す
        for framework, expected_categories in common_frameworks.items():
            if framework in topic_lower:
                for expected in expected_categories:
                    if not any(expected.lower() in existing.lower() for existing in existing_names):
                        gaps.append(expected)
                break
        
        return gaps[:3]  # 最大3つまで
    
    def _generate_improvements(self, analysis: MECEAnalysis):
        """改善提案を生成する"""
        
        if analysis.violation_type == MECEViolationType.OVERLAP:
            analysis.improvement_suggestions.append("重複するカテゴリを統合または明確に区別する")
            for cat1, cat2 in analysis.overlaps:
                analysis.improvement_suggestions.append(f"「{cat1}」と「{cat2}」の境界を明確にする")
        
        if analysis.violation_type == MECEViolationType.GAP:
            analysis.improvement_suggestions.append("不足するカテゴリを追加して網羅性を向上させる")
            for gap in analysis.gaps:
                analysis.improvement_suggestions.append(f"「{gap}」カテゴリの追加を検討する")
        
        if analysis.violation_type == MECEViolationType.BOTH:
            analysis.improvement_suggestions.extend([
                "重複の解消と漏れの補完を同時に行う",
                "カテゴリ全体を再構築することを検討する"
            ])
        
        if analysis.violation_type == MECEViolationType.NONE:
            analysis.improvement_suggestions.append("MECE原則に適合しています。細部の調整を検討してください")
    
    def _suggest_mece_structure(self, topic: str, framework: str) -> List[str]:
        """トピックに対するMECE構造を提案する"""
        
        topic_lower = topic.lower()
        
        if framework == "4P":
            return ["製品(Product)", "価格(Price)", "流通(Place)", "プロモーション(Promotion)"]
        elif framework == "3C":
            return ["顧客(Customer)", "競合(Competitor)", "自社(Company)"]
        elif framework == "SWOT":
            return ["強み(Strengths)", "弱み(Weaknesses)", "機会(Opportunities)", "脅威(Threats)"]
        elif framework == "時系列":
            return ["過去", "現在", "未来"]
        elif framework == "内外":
            return ["内部要因", "外部要因"]
        else:  # auto
            if any(word in topic_lower for word in ["事業", "ビジネス", "経営"]):
                return ["戦略", "組織", "プロセス", "技術", "財務"]
            elif any(word in topic_lower for word in ["マーケティング", "営業"]):
                return ["製品", "価格", "流通", "プロモーション"]
            elif any(word in topic_lower for word in ["組織", "チーム"]):
                return ["人材", "プロセス", "技術", "組織構造"]
            elif any(word in topic_lower for word in ["問題", "課題"]):
                return ["人的要因", "プロセス要因", "技術要因", "環境要因"]
            else:
                return ["カテゴリA", "カテゴリB", "カテゴリC", "その他"]
    
    def _generate_category_description(self, category_name: str, topic: str) -> str:
        """カテゴリの説明を生成する"""
        
        descriptions = {
            "戦略": "方針や計画に関する要素",
            "組織": "組織構造や体制に関する要素", 
            "プロセス": "業務プロセスや手順に関する要素",
            "技術": "技術やシステムに関する要素",
            "財務": "資金や収益に関する要素",
            "人材": "人的リソースに関する要素",
            "顧客": "顧客や市場に関する要素",
            "製品": "商品やサービスに関する要素"
        }
        
        for key, desc in descriptions.items():
            if key in category_name:
                return desc
        
        return f"{topic}における{category_name}の側面"
    
    def _estimate_category_items(self, category_name: str, topic: str) -> List[str]:
        """カテゴリに含まれる要素を推定する"""
        
        category_items = {
            "戦略": ["ビジョン", "目標", "計画", "方針"],
            "組織": ["組織図", "役割", "権限", "責任"],
            "プロセス": ["手順", "フロー", "ルール", "基準"],
            "技術": ["システム", "ツール", "インフラ", "技術力"],
            "財務": ["予算", "収益", "コスト", "投資"],
            "人材": ["スキル", "経験", "モチベーション", "人数"],
            "顧客": ["ニーズ", "満足度", "セグメント", "行動"]
        }
        
        for key, items in category_items.items():
            if key in category_name:
                return items[:3]  # 最初の3つを返す
        
        return []
    
    def _add_analysis_notes(self, analysis: MECEAnalysis):
        """分析ノートを追加する"""
        
        analysis.analysis_notes.append("MECE分析は論理的な構造化に有効なフレームワークです")
        
        if len(analysis.original_categories) < 3:
            analysis.analysis_notes.append("カテゴリ数が少ない可能性があります。網羅性を確認してください")
        elif len(analysis.original_categories) > 7:
            analysis.analysis_notes.append("カテゴリ数が多い可能性があります。グルーピングを検討してください")
        
        if analysis.violation_type != MECEViolationType.NONE:
            analysis.analysis_notes.append("MECE原則の改善により、より効果的な分類が可能になります")
    
    def _format_analysis_result(self, analysis: MECEAnalysis) -> str:
        """分析結果を整形する"""
        
        result = f"MECE分析結果 (ID: {analysis.id})\n\n"
        result += f"分析対象: {analysis.topic}\n\n"
        
        result += "提供されたカテゴリ:\n"
        for i, category in enumerate(analysis.original_categories, 1):
            result += f"{i}. {category}\n"
        result += "\n"
        
        # MECE違反の評価
        result += f"MECE評価: {analysis.violation_type.value}\n\n"
        
        if analysis.overlaps:
            result += "🚨 重複の検出:\n"
            for cat1, cat2 in analysis.overlaps:
                result += f"• 「{cat1}」と「{cat2}」が重複している可能性\n"
            result += "\n"
        
        if analysis.gaps:
            result += "⚠️ 網羅性の漏れ:\n"
            for gap in analysis.gaps:
                result += f"• 「{gap}」が不足している可能性\n"
            result += "\n"
        
        if analysis.improvement_suggestions:
            result += "💡 改善提案:\n"
            for suggestion in analysis.improvement_suggestions:
                result += f"• {suggestion}\n"
            result += "\n"
        
        if analysis.analysis_notes:
            result += "分析メモ:\n"
            for note in analysis.analysis_notes:
                result += f"• {note}\n"
            result += "\n"
        
        result += "🎯 MECEフレームワーク活用のポイント:\n"
        result += "• Mutually Exclusive（相互排他性）：重複をなくす\n"
        result += "• Collectively Exhaustive（網羅性）：漏れをなくす\n"
        result += "• カテゴリの粒度を統一する\n"
        result += "• 目的に応じて階層化を検討する\n"
        result += "• 定期的にカテゴリ分類を見直す"
        
        return result