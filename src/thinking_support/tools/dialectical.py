"""弁証法支援ツール"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional


class DialecticalPosition:
    """弁証法の立場（テーゼ、アンチテーゼ、ジンテーゼ）を表すクラス"""
    
    def __init__(self, type: str, content: str, evidence: Optional[List[str]] = None):
        self.type = type  # "thesis", "antithesis", "synthesis"
        self.content = content
        self.evidence = evidence or []
        self.created_at = datetime.now()


class DialecticalProcess:
    """弁証法的思考プロセスを表すクラス"""
    
    def __init__(self, topic: str, context: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.topic = topic
        self.context = context
        self.thesis: Optional[DialecticalPosition] = None
        self.antithesis: Optional[DialecticalPosition] = None
        self.synthesis: Optional[DialecticalPosition] = None
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None


class DialecticalThinking:
    """弁証法的思考をサポートするクラス"""
    
    def __init__(self):
        self.processes: Dict[str, DialecticalProcess] = {}
    
    async def start_dialectical_process(self, topic: str, context: Optional[str] = None) -> str:
        """弁証法的思考プロセスを開始する"""
        
        process = DialecticalProcess(topic, context)
        self.processes[process.id] = process
        
        result = f"弁証法的思考プロセスを開始しました (ID: {process.id})\n\n"
        result += f"対象トピック: {topic}\n"
        if context:
            result += f"背景情報: {context}\n"
        result += "\n弁証法的思考の手順:\n"
        result += "1. テーゼ（正）の設定 - 初期の主張や立場を明確化\n"
        result += "2. アンチテーゼ（反）の提示 - テーゼに対する反対意見や課題を検討\n"
        result += "3. ジンテーゼ（合）の構築 - テーゼとアンチテーゼを統合した新たな見解を形成\n\n"
        result += "まずは dialectical_set_thesis を使用してテーゼを設定してください。"
        
        return result
    
    async def set_thesis(self, process_id: str, thesis: str, evidence: Optional[List[str]] = None) -> str:
        """テーゼ（正）を設定する"""
        
        if process_id not in self.processes:
            return f"エラー: プロセスID '{process_id}' が見つかりません。"
        
        process = self.processes[process_id]
        process.thesis = DialecticalPosition("thesis", thesis, evidence)
        
        result = f"テーゼを設定しました\n\n"
        result += f"トピック: {process.topic}\n"
        result += f"テーゼ（正）: {thesis}\n"
        
        if evidence:
            result += f"\n根拠:\n"
            for i, ev in enumerate(evidence, 1):
                result += f"{i}. {ev}\n"
        
        result += f"\n次に dialectical_set_antithesis を使用してアンチテーゼを設定してください。"
        
        return result
    
    async def set_antithesis(self, process_id: str, antithesis: str, evidence: Optional[List[str]] = None) -> str:
        """アンチテーゼ（反）を設定する"""
        
        if process_id not in self.processes:
            return f"エラー: プロセスID '{process_id}' が見つかりません。"
        
        process = self.processes[process_id]
        
        if not process.thesis:
            return "エラー: まずテーゼを設定してください。"
        
        process.antithesis = DialecticalPosition("antithesis", antithesis, evidence)
        
        result = f"アンチテーゼを設定しました\n\n"
        result += f"トピック: {process.topic}\n"
        result += f"テーゼ（正）: {process.thesis.content}\n"
        result += f"アンチテーゼ（反）: {antithesis}\n"
        
        if evidence:
            result += f"\n反論の根拠:\n"
            for i, ev in enumerate(evidence, 1):
                result += f"{i}. {ev}\n"
        
        result += f"\n次に dialectical_create_synthesis を使用してジンテーゼを構築してください。"
        
        return result
    
    async def create_synthesis(self, process_id: str, synthesis: str, reasoning: Optional[str] = None) -> str:
        """ジンテーゼ（合）を構築する"""
        
        if process_id not in self.processes:
            return f"エラー: プロセスID '{process_id}' が見つかりません。"
        
        process = self.processes[process_id]
        
        if not process.thesis or not process.antithesis:
            return "エラー: テーゼとアンチテーゼの両方を設定してください。"
        
        process.synthesis = DialecticalPosition("synthesis", synthesis)
        process.completed_at = datetime.now()
        
        result = f"弁証法的思考プロセスが完了しました\n\n"
        result += f"トピック: {process.topic}\n"
        result += f"テーゼ（正）: {process.thesis.content}\n"
        result += f"アンチテーゼ（反）: {process.antithesis.content}\n"
        result += f"ジンテーゼ（合）: {synthesis}\n"
        
        if reasoning:
            result += f"\n統合の理由: {reasoning}\n"
        
        result += f"\n弁証法的思考の成果:\n"
        result += f"• 多面的な視点から問題を検討できました\n"
        result += f"• 対立する意見を統合し、より高次の理解を得ました\n"
        result += f"• 新たな視点や解決策が導き出されました\n"
        
        return result
    
    async def analyze_contradiction(self, topic: str, position_a: str, position_b: str) -> str:
        """矛盾する立場を分析し、弁証法的統合を提案する"""
        
        result = f"矛盾分析と弁証法的統合の提案\n\n"
        result += f"分析対象: {topic}\n\n"
        result += f"立場A: {position_a}\n"
        result += f"立場B: {position_b}\n\n"
        
        # 矛盾点の分析
        result += f"矛盾点の分析:\n"
        result += f"• これらの立場は表面的には対立しているように見えます\n"
        result += f"• しかし、それぞれが異なる側面や価値観を重視している可能性があります\n"
        result += f"• 両立場の根底にある前提や文脈を検討する必要があります\n\n"
        
        # 統合のヒント
        result += f"統合への指針:\n"
        result += f"1. 両立場の背景にある価値観や目的を特定する\n"
        result += f"2. 共通点や補完的な要素を見つける\n"
        result += f"3. より高次の視点から問題を再定義する\n"
        result += f"4. 時間軸や文脈によって使い分ける方法を検討する\n"
        result += f"5. 第三の道や創造的な解決策を模索する\n\n"
        
        # 推奨アプローチ
        result += f"推奨する弁証法的アプローチ:\n"
        result += f"• dialectical_start_process を使用して正式なプロセスを開始\n"
        result += f"• 立場Aをテーゼとして設定\n"
        result += f"• 立場Bをアンチテーゼとして展開\n"
        result += f"• 両者を統合した新たなジンテーゼを構築\n"
        
        return result
    
    async def get_process(self, process_id: str) -> str:
        """弁証法プロセスの現在の状況を取得する"""
        
        if process_id not in self.processes:
            return f"エラー: プロセスID '{process_id}' が見つかりません。"
        
        process = self.processes[process_id]
        
        result = f"弁証法プロセスの状況 (ID: {process_id})\n\n"
        result += f"トピック: {process.topic}\n"
        if process.context:
            result += f"背景: {process.context}\n"
        result += f"開始日時: {process.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        if process.completed_at:
            result += f"完了日時: {process.completed_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        result += "\n現在の進行状況:\n"
        
        if process.thesis:
            result += f"✓ テーゼ（正）: {process.thesis.content}\n"
        else:
            result += "⏳ テーゼ（正）: 未設定\n"
        
        if process.antithesis:
            result += f"✓ アンチテーゼ（反）: {process.antithesis.content}\n"
        else:
            result += "⏳ アンチテーゼ（反）: 未設定\n"
        
        if process.synthesis:
            result += f"✓ ジンテーゼ（合）: {process.synthesis.content}\n"
        else:
            result += "⏳ ジンテーゼ（合）: 未設定\n"
        
        # 次のステップの提案
        if not process.thesis:
            result += "\n次のステップ: dialectical_set_thesis を使用してテーゼを設定してください。"
        elif not process.antithesis:
            result += "\n次のステップ: dialectical_set_antithesis を使用してアンチテーゼを設定してください。"
        elif not process.synthesis:
            result += "\n次のステップ: dialectical_create_synthesis を使用してジンテーゼを構築してください。"
        else:
            result += "\n✅ プロセスは完了しています。"
        
        return result
    
    async def list_processes(self) -> str:
        """すべての弁証法プロセスの一覧を取得する"""
        
        if not self.processes:
            return "現在、実行中の弁証法プロセスはありません。"
        
        result = f"弁証法プロセス一覧 ({len(self.processes)}件)\n\n"
        
        for process in self.processes.values():
            status = "完了" if process.completed_at else "進行中"
            result += f"• ID: {process.id}\n"
            result += f"  トピック: {process.topic}\n"
            result += f"  状態: {status}\n"
            result += f"  開始: {process.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            if process.completed_at:
                result += f"  完了: {process.completed_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            result += "\n"
        
        return result