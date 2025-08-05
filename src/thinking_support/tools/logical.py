"""ロジカルシンキング支援ツール"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum


class ArgumentType(Enum):
    """論証の種類"""
    DEDUCTIVE = "演繹的推論"
    INDUCTIVE = "帰納的推論"
    ABDUCTIVE = "仮説的推論"


class LogicalStructure(Enum):
    """論理構造の種類"""
    MODUS_PONENS = "モーダス・ポネンス"
    MODUS_TOLLENS = "モーダス・トレンス"
    SYLLOGISM = "三段論法"
    CAUSAL_CHAIN = "因果連鎖"


class CausalRelationType(Enum):
    """因果関係の種類"""
    DIRECT = "直接的因果関係"
    INDIRECT = "間接的因果関係"
    CORRELATION = "相関関係"
    SPURIOUS = "偽の相関"
    UNKNOWN = "関係不明"


class LogicalArgument:
    """論理的論証を表すクラス"""
    
    def __init__(self, premises: List[str], conclusion: str):
        self.id = str(uuid.uuid4())
        self.premises = premises
        self.conclusion = conclusion
        self.argument_type = ArgumentType.DEDUCTIVE
        self.logical_structure = LogicalStructure.SYLLOGISM
        self.validity: Optional[bool] = None  # True: 妥当, False: 不妥当, None: 未評価
        self.soundness: Optional[bool] = None  # True: 健全, False: 不健全, None: 未評価
        self.analysis_notes: List[str] = []
        self.created_at = datetime.now()


class CausalAnalysis:
    """因果関係分析を表すクラス"""
    
    def __init__(self, situation: str, factors: List[str]):
        self.id = str(uuid.uuid4())
        self.situation = situation
        self.factors = factors
        self.causal_relationships: List[Tuple[str, str, CausalRelationType]] = []
        self.primary_causes: List[str] = []
        self.secondary_causes: List[str] = []
        self.intervening_variables: List[str] = []
        self.analysis_notes: List[str] = []
        self.created_at = datetime.now()


class LogicalThinking:
    """ロジカルシンキングをサポートするクラス"""
    
    def __init__(self):
        self.arguments: Dict[str, LogicalArgument] = {}
        self.causal_analyses: Dict[str, CausalAnalysis] = {}
    
    async def build_argument(self, premises: List[str], conclusion: str) -> str:
        """前提から結論まで論理的な論証を構築する"""
        
        argument = LogicalArgument(premises, conclusion)
        
        # 論証タイプを分析
        argument.argument_type = self._analyze_argument_type(premises, conclusion)
        
        # 論理構造を特定
        argument.logical_structure = self._identify_logical_structure(premises, conclusion)
        
        # 妥当性を評価
        argument.validity = self._assess_validity(argument)
        
        # 健全性を評価（前提の真偽は仮定）
        argument.soundness = self._assess_soundness(argument)
        
        # 分析ノートを追加
        self._add_analysis_notes(argument)
        
        # 論証を保存
        self.arguments[argument.id] = argument
        
        # 結果を整形して返す
        result = f"論理的論証分析 (ID: {argument.id})\n\n"
        result += f"論証タイプ: {argument.argument_type.value}\n"
        result += f"論理構造: {argument.logical_structure.value}\n\n"
        
        result += "前提:\n"
        for i, premise in enumerate(premises, 1):
            result += f"  {i}. {premise}\n"
        
        result += f"\n結論: {conclusion}\n\n"
        
        # 妥当性評価
        validity_text = "妥当" if argument.validity else "不妥当" if argument.validity is False else "評価困難"
        result += f"妥当性: {validity_text}\n"
        
        # 健全性評価
        soundness_text = "健全" if argument.soundness else "不健全" if argument.soundness is False else "評価困難"
        result += f"健全性: {soundness_text}\n\n"
        
        if argument.analysis_notes:
            result += "分析メモ:\n"
            for note in argument.analysis_notes:
                result += f"• {note}\n"
            result += "\n"
        
        result += "💡 論理的思考のポイント:\n"
        result += "• 前提の真偽を慎重に検証する\n"
        result += "• 論理の飛躍がないか確認する\n"
        result += "• 反例がないか考える\n"
        result += "• 隠れた前提がないか検討する"
        
        return result
    
    async def find_causality(self, situation: str, factors: Optional[List[str]] = None) -> str:
        """原因と結果の関係を分析し、因果関係を特定する"""
        
        if factors is None:
            factors = []
        
        analysis = CausalAnalysis(situation, factors)
        
        # 因果関係を分析
        self._analyze_causal_relationships(analysis)
        
        # 主要因と副次的要因を特定
        self._identify_primary_and_secondary_causes(analysis)
        
        # 介入変数を特定
        self._identify_intervening_variables(analysis)
        
        # 分析ノートを追加
        self._add_causal_analysis_notes(analysis)
        
        # 分析を保存
        self.causal_analyses[analysis.id] = analysis
        
        # 結果を整形して返す
        result = f"因果関係分析 (ID: {analysis.id})\n\n"
        result += f"分析対象: {situation}\n\n"
        
        if analysis.primary_causes:
            result += "主要な原因:\n"
            for cause in analysis.primary_causes:
                result += f"🎯 {cause}\n"
            result += "\n"
        
        if analysis.secondary_causes:
            result += "副次的な原因:\n"
            for cause in analysis.secondary_causes:
                result += f"📍 {cause}\n" 
            result += "\n"
        
        if analysis.intervening_variables:
            result += "介入変数（媒介要因）:\n"
            for var in analysis.intervening_variables:
                result += f"🔗 {var}\n"
            result += "\n"
        
        if analysis.causal_relationships:
            result += "特定された因果関係:\n"
            for cause, effect, relation_type in analysis.causal_relationships:
                result += f"• {cause} → {effect} ({relation_type.value})\n"
            result += "\n"
        
        if analysis.analysis_notes:
            result += "分析メモ:\n"
            for note in analysis.analysis_notes:
                result += f"• {note}\n"
            result += "\n"
        
        result += "🔍 因果関係分析のポイント:\n"
        result += "• 相関関係と因果関係を区別する\n"
        result += "• 時間的順序を確認する（原因は結果より先行）\n"
        result += "• 第三の変数の影響を考慮する\n" 
        result += "• 複数の原因が複合的に作用する可能性を検討する\n"
        result += "• 逆因果（結果が原因に影響）の可能性も考える"
        
        return result
    
    def _analyze_argument_type(self, premises: List[str], conclusion: str) -> ArgumentType:
        """論証タイプを分析する"""
        
        # キーワードベースの簡易判定
        all_text = " ".join(premises + [conclusion]).lower()
        
        if any(word in all_text for word in ["すべて", "必ず", "常に", "もし...ならば"]):
            return ArgumentType.DEDUCTIVE
        elif any(word in all_text for word in ["おそらく", "たぶん", "可能性", "統計"]):
            return ArgumentType.INDUCTIVE
        elif any(word in all_text for word in ["最も良い説明", "仮説", "推測"]):
            return ArgumentType.ABDUCTIVE
        else:
            return ArgumentType.DEDUCTIVE  # デフォルト
    
    def _identify_logical_structure(self, premises: List[str], conclusion: str) -> LogicalStructure:
        """論理構造を特定する"""
        
        all_text = " ".join(premises + [conclusion]).lower()
        
        if "もし" in all_text and "ならば" in all_text:
            if "ない" in conclusion.lower():
                return LogicalStructure.MODUS_TOLLENS
            else:
                return LogicalStructure.MODUS_PONENS
        elif "原因" in all_text or "結果" in all_text or "なぜなら" in all_text:
            return LogicalStructure.CAUSAL_CHAIN
        else:
            return LogicalStructure.SYLLOGISM
    
    def _assess_validity(self, argument: LogicalArgument) -> Optional[bool]:
        """論証の妥当性を評価する"""
        
        # 簡易的な妥当性チェック
        if argument.logical_structure == LogicalStructure.MODUS_PONENS:
            # モーダス・ポネンスの形式チェック
            return self._check_modus_ponens_validity(argument)
        elif argument.logical_structure == LogicalStructure.SYLLOGISM:
            # 三段論法の形式チェック
            return self._check_syllogism_validity(argument)
        else:
            return None  # 評価困難
    
    def _assess_soundness(self, argument: LogicalArgument) -> Optional[bool]:
        """論証の健全性を評価する（前提の真偽は仮定）"""
        
        if argument.validity is False:
            return False  # 妥当でない論証は健全ではない
        elif argument.validity is True:
            # 前提の真偽は実際には検証困難なので、形式的に健全とする
            return True
        else:
            return None  # 評価困難
    
    def _check_modus_ponens_validity(self, argument: LogicalArgument) -> bool:
        """モーダス・ポネンスの妥当性をチェック"""
        # 簡易的な実装：実際にはより複雑な論理解析が必要
        return len(argument.premises) >= 2
    
    def _check_syllogism_validity(self, argument: LogicalArgument) -> bool:
        """三段論法の妥当性をチェック"""
        # 簡易的な実装：実際にはより複雑な論理解析が必要
        return len(argument.premises) >= 2
    
    def _add_analysis_notes(self, argument: LogicalArgument):
        """分析ノートを追加する"""
        
        if argument.argument_type == ArgumentType.DEDUCTIVE:
            argument.analysis_notes.append("演繹的推論：前提が真なら結論も必然的に真")
        elif argument.argument_type == ArgumentType.INDUCTIVE:
            argument.analysis_notes.append("帰納的推論：前提から結論の蓋然性を推定")
        
        if not argument.validity:
            argument.analysis_notes.append("論理構造に問題がある可能性があります")
        
        if len(argument.premises) == 1:
            argument.analysis_notes.append("前提が少ない可能性があります。隠れた前提がないか確認してください")
    
    def _analyze_causal_relationships(self, analysis: CausalAnalysis):
        """因果関係を分析する"""
        
        situation_lower = analysis.situation.lower()
        
        # 基本的な因果関係パターンを探す
        if "ため" in situation_lower or "による" in situation_lower:
            analysis.causal_relationships.append(
                ("特定の要因", analysis.situation, CausalRelationType.DIRECT)
            )
        
        # 提供された要因がある場合、それらを分析
        for factor in analysis.factors:
            if "増加" in factor or "減少" in factor:
                analysis.causal_relationships.append(
                    (factor, analysis.situation, CausalRelationType.CORRELATION)
                )
    
    def _identify_primary_and_secondary_causes(self, analysis: CausalAnalysis):
        """主要因と副次的要因を特定する"""
        
        situation_lower = analysis.situation.lower()
        
        # キーワードベースの簡易分析
        if "経済" in situation_lower:
            analysis.primary_causes.extend(["経済状況", "市場環境"])
            analysis.secondary_causes.extend(["政策変更", "技術革新"])
        elif "健康" in situation_lower:
            analysis.primary_causes.extend(["生活習慣", "遺伝的要因"])
            analysis.secondary_causes.extend(["環境要因", "ストレス"])
        elif "教育" in situation_lower or "学習" in situation_lower:
            analysis.primary_causes.extend(["学習時間", "学習方法"])
            analysis.secondary_causes.extend(["環境", "動機"])
        else:
            # 一般的な分析
            if analysis.factors:
                analysis.primary_causes.extend(analysis.factors[:2])  # 最初の2つを主要因とする
                analysis.secondary_causes.extend(analysis.factors[2:])  # 残りを副次的要因とする
    
    def _identify_intervening_variables(self, analysis: CausalAnalysis):
        """介入変数を特定する"""
        
        situation_lower = analysis.situation.lower()
        
        # 一般的な介入変数
        common_intervening = ["時間", "努力", "リソース", "機会", "外部環境"]
        
        if "成果" in situation_lower or "結果" in situation_lower:
            analysis.intervening_variables.extend(["実行力", "継続性"])
        
        analysis.intervening_variables.extend(common_intervening[:2])  # 最初の2つを追加
    
    def _add_causal_analysis_notes(self, analysis: CausalAnalysis):
        """因果分析のノートを追加する"""
        
        analysis.analysis_notes.append("因果関係の特定には十分なデータと慎重な分析が必要です")
        
        if not analysis.factors:
            analysis.analysis_notes.append("より多くの要因を考慮することで分析精度が向上します")
        
        if len(analysis.causal_relationships) == 0:
            analysis.analysis_notes.append("明確な因果関係を特定するには追加情報が必要かもしれません")