"""動的思考支援ツール（Sequential Thinking）"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import json
import os
import sys


@dataclass
class ThoughtData:
    """思考データを表すクラス"""
    thought: str
    thought_number: int
    total_thoughts: int
    next_thought_needed: bool
    is_revision: Optional[bool] = None
    revises_thought: Optional[int] = None
    branch_from_thought: Optional[int] = None
    branch_id: Optional[str] = None
    needs_more_thoughts: Optional[bool] = None


class SequentialThinking:
    """動的思考をサポートするクラス"""
    
    def __init__(self):
        self.thought_history: List[ThoughtData] = []
        self.branches: Dict[str, List[ThoughtData]] = {}
        self.disable_thought_logging = os.getenv("DISABLE_THOUGHT_LOGGING", "").lower() == "true"
    
    def validate_thought_data(self, input_data: Dict[str, Any]) -> ThoughtData:
        """思考データをバリデーションする"""
        
        if not input_data.get("thought") or not isinstance(input_data["thought"], str):
            raise ValueError("Invalid thought: must be a string")
        
        if not input_data.get("thought_number") or not isinstance(input_data["thought_number"], int):
            raise ValueError("Invalid thought_number: must be a number")
        
        if not input_data.get("total_thoughts") or not isinstance(input_data["total_thoughts"], int):
            raise ValueError("Invalid total_thoughts: must be a number")
        
        if not isinstance(input_data.get("next_thought_needed"), bool):
            raise ValueError("Invalid next_thought_needed: must be a boolean")
        
        return ThoughtData(
            thought=input_data["thought"],
            thought_number=input_data["thought_number"],
            total_thoughts=input_data["total_thoughts"],
            next_thought_needed=input_data["next_thought_needed"],
            is_revision=input_data.get("is_revision"),
            revises_thought=input_data.get("revises_thought"),
            branch_from_thought=input_data.get("branch_from_thought"),
            branch_id=input_data.get("branch_id"),
            needs_more_thoughts=input_data.get("needs_more_thoughts")
        )
    
    def format_thought(self, thought_data: ThoughtData) -> str:
        """思考データを視覚的にフォーマットする"""
        
        prefix = ""
        context = ""
        
        if thought_data.is_revision:
            prefix = "🔄 修正"
            context = f" (思考{thought_data.revises_thought}を修正)"
        elif thought_data.branch_from_thought:
            prefix = "🌿 分岐"
            context = f" (思考{thought_data.branch_from_thought}から分岐, ID: {thought_data.branch_id})"
        else:
            prefix = "💭 思考"
            context = ""
        
        header = f"{prefix} {thought_data.thought_number}/{thought_data.total_thoughts}{context}"
        border_length = max(len(header), len(thought_data.thought)) + 4
        border = "─" * border_length
        
        return f"""
┌{border}┐
│ {header.ljust(border_length - 2)} │
├{border}┤
│ {thought_data.thought.ljust(border_length - 2)} │
└{border}┘"""
    
    async def process_thought(self, input_data: Dict[str, Any]) -> str:
        """思考を処理し、履歴に記録する"""
        
        try:
            validated_input = self.validate_thought_data(input_data)
            
            # 思考数が総思考数を超える場合、総思考数を調整
            if validated_input.thought_number > validated_input.total_thoughts:
                validated_input.total_thoughts = validated_input.thought_number
            
            # 思考履歴に追加
            self.thought_history.append(validated_input)
            
            # 分岐がある場合、分岐履歴に追加
            if validated_input.branch_from_thought and validated_input.branch_id:
                if validated_input.branch_id not in self.branches:
                    self.branches[validated_input.branch_id] = []
                self.branches[validated_input.branch_id].append(validated_input)
            
            # 思考ログを表示（環境変数で無効化可能）
            if not self.disable_thought_logging:
                formatted_thought = self.format_thought(validated_input)
                print(formatted_thought, file=sys.stderr)
            
            # 結果を返す
            result = {
                "thought_number": validated_input.thought_number,
                "total_thoughts": validated_input.total_thoughts,
                "next_thought_needed": validated_input.next_thought_needed,
                "branches": list(self.branches.keys()),
                "thought_history_length": len(self.thought_history),
                "status": "success"
            }
            
            return json.dumps(result, ensure_ascii=False, indent=2)
            
        except Exception as error:
            # エラー処理
            error_result = {
                "error": str(error),
                "status": "failed"
            }
            return json.dumps(error_result, ensure_ascii=False, indent=2)
    
    def get_thought_history(self) -> List[ThoughtData]:
        """思考履歴を取得する"""
        return self.thought_history.copy()
    
    def get_branches(self) -> Dict[str, List[ThoughtData]]:
        """分岐履歴を取得する"""
        return self.branches.copy()
    
    def clear_history(self) -> None:
        """履歴をクリアする"""
        self.thought_history.clear()
        self.branches.clear()