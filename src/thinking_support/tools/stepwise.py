"""段階的思考支援ツール"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional


class StepwiseStep:
    """段階的思考のステップを表すクラス"""
    
    def __init__(self, number: int, description: str, expected_outcome: str):
        self.number = number
        self.description = description
        self.expected_outcome = expected_outcome
        self.status = "pending"  # pending, in_progress, completed, failed
        self.result: Optional[str] = None
        self.completed_at: Optional[datetime] = None


class StepwisePlan:
    """段階的思考の実行計画を表すクラス"""
    
    def __init__(self, problem: str, context: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.problem = problem
        self.context = context
        self.steps: List[StepwiseStep] = []
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None


class StepwiseThinking:
    """段階的思考をサポートするクラス"""
    
    def __init__(self):
        self.plans: Dict[str, StepwisePlan] = {}
    
    async def create_plan(self, problem: str, context: Optional[str] = None) -> str:
        """問題を段階的なステップに分解して実行計画を作成する"""
        
        plan = StepwisePlan(problem, context)
        
        # 問題を分析してステップを生成
        steps = self._analyze_and_create_steps(problem, context)
        plan.steps = steps
        
        self.plans[plan.id] = plan
        
        # 結果を整形して返す
        result = f"段階的実行計画を作成しました (ID: {plan.id})\n\n"
        result += f"問題: {problem}\n"
        if context:
            result += f"背景: {context}\n"
        result += f"\n実行ステップ:\n"
        
        for step in steps:
            result += f"{step.number}. {step.description}\n"
            result += f"   期待する成果: {step.expected_outcome}\n\n"
        
        result += f"各ステップを実行するには stepwise_execute_step を使用してください。"
        
        return result
    
    async def execute_step(self, plan_id: str, step_number: int, result: str) -> str:
        """計画の特定ステップを実行し、結果を記録する"""
        
        if plan_id not in self.plans:
            return f"エラー: 計画ID '{plan_id}' が見つかりません。"
        
        plan = self.plans[plan_id]
        
        # ステップを検索
        target_step = None
        for step in plan.steps:
            if step.number == step_number:
                target_step = step
                break
        
        if not target_step:
            return f"エラー: ステップ {step_number} が見つかりません。"
        
        # ステップを完了状態に更新
        target_step.result = result
        target_step.status = "completed"
        target_step.completed_at = datetime.now()
        
        # 進捗状況を計算
        completed_steps = sum(1 for s in plan.steps if s.status == "completed")
        total_steps = len(plan.steps)
        progress = f"{completed_steps}/{total_steps}"
        
        # 全ステップが完了したかチェック
        if completed_steps == total_steps:
            plan.completed_at = datetime.now()
        
        response = f"ステップ {step_number} を完了しました (進捗: {progress})\n\n"
        response += f"ステップ: {target_step.description}\n"
        response += f"実行結果: {result}\n\n"
        
        if completed_steps == total_steps:
            response += "🎉 すべてのステップが完了しました！\n\n"
            response += "実行サマリー:\n"
            for step in plan.steps:
                response += f"{step.number}. {step.description}\n"
                response += f"   結果: {step.result}\n"
        else:
            # 次のステップを提案
            next_step = None
            for step in plan.steps:
                if step.status == "pending":
                    next_step = step
                    break
            
            if next_step:
                response += f"次のステップ: {next_step.number}. {next_step.description}\n"
                response += f"期待する成果: {next_step.expected_outcome}"
        
        return response
    
    def _analyze_and_create_steps(self, problem: str, context: Optional[str]) -> List[StepwiseStep]:
        """問題を分析して段階的なステップを作成する"""
        
        # 基本的なステップ分解パターン
        if "プログラム" in problem or "コード" in problem or "開発" in problem:
            return self._create_programming_steps(problem)
        elif "学習" in problem or "勉強" in problem:
            return self._create_learning_steps(problem)
        elif "問題解決" in problem or "課題" in problem:
            return self._create_problem_solving_steps(problem)
        else:
            return self._create_generic_steps(problem)
    
    def _create_programming_steps(self, problem: str) -> List[StepwiseStep]:
        """プログラミング関連の問題に対するステップを作成"""
        return [
            StepwiseStep(1, "要件の明確化と分析", "具体的な機能要件と制約条件の特定"),
            StepwiseStep(2, "設計とアーキテクチャの検討", "システム構造と実装方針の決定"),
            StepwiseStep(3, "開発環境の準備", "必要なツールとライブラリの確認・セットアップ"),
            StepwiseStep(4, "核となる機能の実装", "最も重要な機能の実装完了"),
            StepwiseStep(5, "テストとデバッグ", "動作確認と問題の修正"),
            StepwiseStep(6, "完成度の向上と最適化", "性能改善とコードの整理")
        ]
    
    def _create_learning_steps(self, problem: str) -> List[StepwiseStep]:
        """学習関連の問題に対するステップを作成"""
        return [
            StepwiseStep(1, "学習目標の設定", "明確で測定可能な学習目標の定義"),
            StepwiseStep(2, "現在の知識レベルの把握", "既存知識と不足部分の特定"),
            StepwiseStep(3, "学習計画の作成", "効率的な学習順序とスケジュールの策定"),
            StepwiseStep(4, "基礎知識の習得", "必要な基礎概念の理解"),
            StepwiseStep(5, "実践的な練習", "知識を実際に適用する練習"),
            StepwiseStep(6, "理解度の確認と定着", "学習内容の振り返りと定着確認")
        ]
    
    def _create_problem_solving_steps(self, problem: str) -> List[StepwiseStep]:
        """一般的な問題解決に対するステップを作成"""
        return [
            StepwiseStep(1, "問題の明確化", "問題の本質と範囲の特定"),
            StepwiseStep(2, "情報収集と現状分析", "関連情報の収集と現状の詳細把握"),
            StepwiseStep(3, "原因の特定", "問題の根本原因の分析"),
            StepwiseStep(4, "解決策の検討", "複数の解決策の立案と評価"),
            StepwiseStep(5, "最適解の選択と実行", "最も適切な解決策の実行"),
            StepwiseStep(6, "結果の評価と改善", "実行結果の評価と必要に応じた改善")
        ]
    
    def _create_generic_steps(self, problem: str) -> List[StepwiseStep]:
        """汎用的なステップを作成"""
        return [
            StepwiseStep(1, "目標の設定", "達成したい目標の明確化"),
            StepwiseStep(2, "現状の把握", "現在の状況と課題の整理"),
            StepwiseStep(3, "計画の立案", "目標達成のための具体的計画"),
            StepwiseStep(4, "実行", "計画に基づいた行動の実施"),
            StepwiseStep(5, "確認と調整", "進捗確認と必要に応じた調整"),
            StepwiseStep(6, "完了と振り返り", "目標達成の確認と経験の整理")
        ]