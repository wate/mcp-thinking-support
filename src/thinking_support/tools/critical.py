"""クリティカルシンキング支援ツール"""

from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class BiasType(Enum):
    """認知バイアスの種類"""
    CONFIRMATION = "確証バイアス"
    AVAILABILITY = "利用可能性ヒューリスティック"
    ANCHORING = "アンカリング効果"
    BANDWAGON = "バンドワゴン効果" 
    AUTHORITY = "権威への訴え"
    AD_HOMINEM = "人身攻撃"
    STRAW_MAN = "わら人形論法"
    FALSE_DILEMMA = "偽の二分法"
    SLIPPERY_SLOPE = "滑りやすい坂論法"
    HASTY_GENERALIZATION = "早まった一般化"


class ReliabilityLevel(Enum):
    """信頼性レベル"""
    HIGH = "高い"
    MEDIUM = "中程度"  
    LOW = "低い"
    UNKNOWN = "不明"


class SourceType(Enum):
    """情報源の種類"""
    ACADEMIC = "学術論文"
    NEWS_MEDIA = "報道機関"
    SOCIAL_MEDIA = "ソーシャルメディア"
    PERSONAL_BLOG = "個人ブログ"
    GOVERNMENT = "政府機関"
    CORPORATE = "企業"
    UNKNOWN = "不明"


class ClaimAnalysis:
    """主張分析の結果を表すクラス"""
    
    def __init__(self, claim: str, source: Optional[str] = None):
        self.claim = claim
        self.source = source
        self.reliability_level = ReliabilityLevel.UNKNOWN
        self.source_type = SourceType.UNKNOWN
        self.strengths: List[str] = []
        self.weaknesses: List[str] = []
        self.questions_to_consider: List[str] = []
        self.supporting_evidence: List[str] = []
        self.contradicting_evidence: List[str] = []
        self.analyzed_at = datetime.now()


class BiasAnalysis:
    """偏見分析の結果を表すクラス"""
    
    def __init__(self, content: str):
        self.content = content
        self.identified_biases: List[BiasType] = []
        self.bias_explanations: Dict[BiasType, str] = {}
        self.logical_fallacies: List[str] = []
        self.recommendations: List[str] = []
        self.analyzed_at = datetime.now()


class CriticalThinking:
    """クリティカルシンキングをサポートするクラス"""
    
    def __init__(self):
        self.analyses: Dict[str, ClaimAnalysis] = {}
        self.bias_analyses: Dict[str, BiasAnalysis] = {}
    
    async def analyze_claim(self, claim: str, source: Optional[str] = None) -> str:
        """主張や情報を批判的に分析し、信頼性を評価する"""
        
        analysis = ClaimAnalysis(claim, source)
        
        # 情報源の種類を推定
        analysis.source_type = self._classify_source(source)
        
        # 主張を分析
        self._analyze_claim_content(analysis)
        
        # 信頼性レベルを判定
        analysis.reliability_level = self._assess_reliability(analysis)
        
        # 分析結果を保存
        analysis_id = str(len(self.analyses) + 1)
        self.analyses[analysis_id] = analysis
        
        # 結果を整形して返す
        result = f"批判的分析結果 (ID: {analysis_id})\n\n"
        result += f"分析対象: {claim}\n"
        if source:
            result += f"情報源: {source}\n"
        result += f"情報源タイプ: {analysis.source_type.value}\n"
        result += f"信頼性レベル: {analysis.reliability_level.value}\n\n"
        
        if analysis.strengths:
            result += "強み・根拠:\n"
            for strength in analysis.strengths:
                result += f"• {strength}\n"
            result += "\n"
        
        if analysis.weaknesses:
            result += "弱点・疑問点:\n"
            for weakness in analysis.weaknesses:
                result += f"• {weakness}\n"
            result += "\n"
        
        if analysis.questions_to_consider:
            result += "検討すべき質問:\n"
            for question in analysis.questions_to_consider:
                result += f"❓ {question}\n"
            result += "\n"
        
        result += "💡 批判的思考のポイント:\n"
        result += "• 複数の情報源から情報を収集する\n"
        result += "• 反対意見も探して検討する\n"  
        result += "• 主張の根拠となるデータや証拠を確認する\n"
        result += "• 情報提供者の動機や利害関係を考慮する"
        
        return result
    
    async def identify_bias(self, content: str) -> str:
        """情報や議論における偏見や論理的誤謬を特定する"""
        
        analysis = BiasAnalysis(content)
        
        # バイアスと論理的誤謬を特定
        self._identify_biases(analysis)
        self._identify_logical_fallacies(analysis)
        
        # 改善提案を生成
        self._generate_recommendations(analysis)
        
        # 分析結果を保存
        analysis_id = str(len(self.bias_analyses) + 1)
        self.bias_analyses[analysis_id] = analysis
        
        # 結果を整形して返す
        result = f"バイアス・誤謬分析結果 (ID: {analysis_id})\n\n"
        
        if analysis.identified_biases:
            result += "特定されたバイアス:\n"
            for bias in analysis.identified_biases:
                result += f"🧠 {bias.value}\n"
                if bias in analysis.bias_explanations:
                    result += f"   説明: {analysis.bias_explanations[bias]}\n"
            result += "\n"
        
        if analysis.logical_fallacies:
            result += "論理的誤謬:\n"
            for fallacy in analysis.logical_fallacies:
                result += f"⚠️ {fallacy}\n" 
            result += "\n"
        
        if analysis.recommendations:
            result += "改善提案:\n"
            for rec in analysis.recommendations:
                result += f"💡 {rec}\n"
            result += "\n"
        
        if not analysis.identified_biases and not analysis.logical_fallacies:
            result += "✅ 明確なバイアスや論理的誤謬は検出されませんでした。\n\n"
        
        result += "📚 批判的思考のチェックポイント:\n"
        result += "• 感情的な言葉遣いに注意する\n"
        result += "• 一般化や極端な表現を避ける\n"
        result += "• 多角的な視点から物事を考える\n"
        result += "• 根拠のない推測と事実を区別する"
        
        return result
    
    def _classify_source(self, source: Optional[str]) -> SourceType:
        """情報源の種類を分類する"""
        if not source:
            return SourceType.UNKNOWN
        
        source_lower = source.lower()
        
        if any(domain in source_lower for domain in ['ac.jp', 'edu', 'arxiv', 'pubmed']):
            return SourceType.ACADEMIC
        elif any(domain in source_lower for domain in ['twitter', 'facebook', 'instagram']):
            return SourceType.SOCIAL_MEDIA
        elif any(domain in source_lower for domain in ['gov', '省', '庁']):
            return SourceType.GOVERNMENT
        elif any(word in source_lower for word in ['news', 'times', 'post', '新聞']):
            return SourceType.NEWS_MEDIA
        elif any(word in source_lower for word in ['blog', 'note', 'qiita']):
            return SourceType.PERSONAL_BLOG
        else:
            return SourceType.CORPORATE
    
    def _analyze_claim_content(self, analysis: ClaimAnalysis):
        """主張の内容を分析する"""
        claim = analysis.claim.lower()
        
        # 強み・根拠を特定
        if "研究" in claim or "データ" in claim or "統計" in claim:
            analysis.strengths.append("研究やデータに基づいている可能性")
        if "専門家" in claim or "教授" in claim:
            analysis.strengths.append("専門家の意見として提示されている")
        
        # 弱点・疑問点を特定  
        if "みんな" in claim or "誰でも" in claim or "常に" in claim:
            analysis.weaknesses.append("過度な一般化の可能性")
        if "絶対" in claim or "間違いなく" in claim:
            analysis.weaknesses.append("断定的すぎる表現")
        if "と思う" in claim or "と感じる" in claim:
            analysis.weaknesses.append("主観的な意見に基づいている")
        
        # 検討すべき質問を生成
        analysis.questions_to_consider.extend([
            "この主張の根拠となるデータや証拠は何か？",
            "反対意見や異なる解釈は存在するか？", 
            "主張者にはどのような背景や利害関係があるか？",
            "この主張は他の信頼できる情報源でも確認できるか？"
        ])
    
    def _assess_reliability(self, analysis: ClaimAnalysis) -> ReliabilityLevel:
        """信頼性レベルを評価する"""
        score = 0
        
        # 情報源による評価
        if analysis.source_type == SourceType.ACADEMIC:
            score += 3
        elif analysis.source_type == SourceType.GOVERNMENT:
            score += 2
        elif analysis.source_type == SourceType.NEWS_MEDIA:
            score += 1
        elif analysis.source_type == SourceType.SOCIAL_MEDIA:
            score -= 1
        
        # 強み・弱点による評価
        score += len(analysis.strengths)
        score -= len(analysis.weaknesses)
        
        if score >= 3:
            return ReliabilityLevel.HIGH
        elif score >= 1:
            return ReliabilityLevel.MEDIUM
        else:
            return ReliabilityLevel.LOW
    
    def _identify_biases(self, analysis: BiasAnalysis):
        """バイアスを特定する"""
        content = analysis.content.lower()
        
        # 確証バイアス
        if "やっぱり" in content or "当然" in content:
            analysis.identified_biases.append(BiasType.CONFIRMATION)
            analysis.bias_explanations[BiasType.CONFIRMATION] = "自分の信念を支持する情報のみを重視している"
        
        # 権威への訴え
        if "専門家が言うから" in content or "有名人が" in content:
            analysis.identified_biases.append(BiasType.AUTHORITY)
            analysis.bias_explanations[BiasType.AUTHORITY] = "権威者の意見を無批判に受け入れている"
        
        # バンドワゴン効果
        if "みんなが" in content or "流行り" in content:
            analysis.identified_biases.append(BiasType.BANDWAGON)
            analysis.bias_explanations[BiasType.BANDWAGON] = "多数派の意見に同調している"
    
    def _identify_logical_fallacies(self, analysis: BiasAnalysis):
        """論理的誤謬を特定する"""
        content = analysis.content.lower()
        
        if "aかbかしかない" in content or "白か黒か" in content:
            analysis.logical_fallacies.append("偽の二分法: 実際にはより多くの選択肢が存在する")
        
        if "だから" in content and "すべて" in content:
            analysis.logical_fallacies.append("早まった一般化: 限られた事例から全体を判断している")
    
    def _generate_recommendations(self, analysis: BiasAnalysis):
        """改善提案を生成する"""
        if analysis.identified_biases or analysis.logical_fallacies:
            analysis.recommendations.extend([
                "反対意見も積極的に探して検討する",
                "複数の情報源から情報を収集する",
                "感情的になっている時は判断を保留する",
                "統計データや客観的証拠を重視する"
            ])
        else:
            analysis.recommendations.append("現在の分析は比較的バランスが取れています")