#!/usr/bin/env python3
"""5Why分析ツールの実装"""

from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime


class WhyAnalysis:
    """5Why分析を実行するクラス"""
    
    def __init__(self):
        self.analyses: Dict[str, Dict[str, Any]] = {}
    
    async def start_analysis(self, problem: str, context: Optional[str] = None) -> str:
        """5Why分析を開始する
        
        Args:
            problem: 分析したい問題
            context: 問題の背景情報（オプション）
            
        Returns:
            分析ID
        """
        analysis_id = str(uuid.uuid4())[:8]
        
        self.analyses[analysis_id] = {
            "id": analysis_id,
            "problem": problem,
            "context": context,
            "whys": [],
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        # 最初のWhyを問題そのものとして設定
        first_why = {
            "level": 0,
            "question": f"なぜ「{problem}」が起こったのか？",
            "answer": None,
            "timestamp": datetime.now().isoformat()
        }
        self.analyses[analysis_id]["whys"].append(first_why)
        
        result = f"📋 5Why分析を開始しました\n\n"
        result += f"**分析ID**: {analysis_id}\n"
        result += f"**問題**: {problem}\n"
        if context:
            result += f"**背景**: {context}\n"
        result += f"\n**最初の質問**: {first_why['question']}\n\n"
        result += "次のステップ: `why_analysis_add_answer` を使用して最初の質問に回答してください。"
        
        return result
    
    async def add_answer(self, analysis_id: str, level: int, answer: str) -> str:
        """Why質問に対する回答を追加し、次のWhyを生成する
        
        Args:
            analysis_id: 分析ID
            level: Whyのレベル（0から4まで）
            answer: 現在のレベルの回答
            
        Returns:
            分析結果と次のステップ
        """
        if analysis_id not in self.analyses:
            return f"❌ 分析ID '{analysis_id}' が見つかりません。"
        
        analysis = self.analyses[analysis_id]
        
        if level >= len(analysis["whys"]):
            return f"❌ レベル {level} の質問が存在しません。"
        
        if analysis["whys"][level]["answer"] is not None:
            return f"❌ レベル {level} の質問にはすでに回答済みです。"
        
        # 回答を記録
        analysis["whys"][level]["answer"] = answer
        analysis["whys"][level]["timestamp"] = datetime.now().isoformat()
        
        result = f"✅ レベル {level + 1} の回答を記録しました\n\n"
        result += f"**Q{level + 1}**: {analysis['whys'][level]['question']}\n"
        result += f"**A{level + 1}**: {answer}\n\n"
        
        # 次のWhyを生成（レベル5まで）
        if level < 4:  # レベル0-4なので、レベル4まで次の質問を生成
            next_level = level + 1
            next_question = f"なぜ「{answer}」なのか？"
            
            next_why = {
                "level": next_level,
                "question": next_question,
                "answer": None,
                "timestamp": datetime.now().isoformat()
            }
            analysis["whys"].append(next_why)
            
            result += f"**次の質問 (レベル {next_level + 1})**: {next_question}\n\n"
            result += f"次のステップ: レベル {next_level} の質問に回答してください。"
        else:
            # 5Why分析完了
            analysis["status"] = "completed"
            result += "🎉 5Why分析が完了しました！\n\n"
            result += self._generate_summary(analysis)
        
        return result
    
    async def get_analysis(self, analysis_id: str) -> str:
        """分析の現在の状態を取得する
        
        Args:
            analysis_id: 分析ID
            
        Returns:
            分析の詳細
        """
        if analysis_id not in self.analyses:
            return f"❌ 分析ID '{analysis_id}' が見つかりません。"
        
        analysis = self.analyses[analysis_id]
        
        result = f"📊 5Why分析の状況\n\n"
        result += f"**分析ID**: {analysis['id']}\n"
        result += f"**問題**: {analysis['problem']}\n"
        if analysis.get('context'):
            result += f"**背景**: {analysis['context']}\n"
        result += f"**ステータス**: {analysis['status']}\n"
        result += f"**作成日時**: {analysis['created_at']}\n\n"
        
        result += "**分析の進行状況**:\n"
        for i, why in enumerate(analysis["whys"]):
            level_num = i + 1
            result += f"\n**Q{level_num}**: {why['question']}\n"
            if why["answer"]:
                result += f"**A{level_num}**: {why['answer']}\n"
            else:
                result += f"**A{level_num}**: （未回答）\n"
        
        if analysis["status"] == "completed":
            result += "\n" + self._generate_summary(analysis)
        
        return result
    
    def _generate_summary(self, analysis: Dict[str, Any]) -> str:
        """分析の要約を生成する"""
        summary = "## 📝 分析要約\n\n"
        summary += f"**根本問題**: {analysis['problem']}\n\n"
        
        summary += "**分析経路**:\n"
        for i, why in enumerate(analysis["whys"]):
            if why["answer"]:
                level_num = i + 1
                summary += f"{level_num}. {why['answer']}\n"
        
        # 根本原因の特定
        if len(analysis["whys"]) >= 5 and analysis["whys"][4]["answer"]:
            summary += f"\n**🎯 根本原因**: {analysis['whys'][4]['answer']}\n"
        
        summary += "\n**💡 推奨アクション**:\n"
        summary += "- 根本原因に対する具体的な対策を検討してください\n"
        summary += "- 再発防止のためのシステムやプロセスの改善を検討してください\n"
        summary += "- 定期的な振り返りで効果を測定してください"
        
        return summary
    
    async def list_analyses(self) -> str:
        """すべての分析の一覧を取得する
        
        Returns:
            分析一覧
        """
        if not self.analyses:
            return "📭 作成された分析はありません。"
        
        result = "📋 5Why分析一覧\n\n"
        
        for analysis_id, analysis in self.analyses.items():
            status_icon = "✅" if analysis["status"] == "completed" else "🔄"
            answered_count = sum(1 for why in analysis["whys"] if why["answer"] is not None)
            total_count = len(analysis["whys"])
            
            result += f"{status_icon} **{analysis_id}**: {analysis['problem'][:50]}{'...' if len(analysis['problem']) > 50 else ''}\n"
            result += f"   進捗: {answered_count}/{total_count} | 作成: {analysis['created_at'][:10]}\n\n"
        
        return result