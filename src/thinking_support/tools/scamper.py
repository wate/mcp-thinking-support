"""SCAMPER（創造的思考法）支援ツール"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class SCAMPERTechnique(Enum):
    """SCAMPER技法の種類"""
    SUBSTITUTE = "Substitute"  # 代替
    COMBINE = "Combine"      # 結合
    ADAPT = "Adapt"         # 応用
    MODIFY = "Modify"       # 変更
    PUT_TO_OTHER_USE = "Put to other use"  # 転用
    ELIMINATE = "Eliminate"  # 除去
    REVERSE = "Reverse"     # 逆転


class SCAMPERIdea:
    """SCAMPERで生成されたアイデアを表すクラス"""
    
    def __init__(self, technique: SCAMPERTechnique, idea: str, explanation: str = ""):
        self.id = str(uuid.uuid4())
        self.technique = technique
        self.idea = idea
        self.explanation = explanation
        self.feasibility_score = 0  # 実現可能性スコア（0-10）
        self.impact_score = 0      # インパクトスコア（0-10）
        self.created_at = datetime.now()


class SCAMPERSession:
    """SCAMPERセッションを表すクラス"""
    
    def __init__(self, topic: str, current_situation: str):
        self.id = str(uuid.uuid4())
        self.topic = topic
        self.current_situation = current_situation
        self.ideas: List[SCAMPERIdea] = []
        self.active_technique: Optional[SCAMPERTechnique] = None
        self.session_notes: List[str] = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


class SCAMPER:
    """SCAMPERフレームワークをサポートするクラス"""
    
    def __init__(self):
        self.sessions: Dict[str, SCAMPERSession] = {}
    
    async def start_session(self, topic: str, current_situation: str, context: Optional[str] = None) -> str:
        """SCAMPERセッションを開始する"""
        
        session = SCAMPERSession(topic, current_situation)
        
        if context:
            session.session_notes.append(f"背景情報: {context}")
        
        # 各技法の概要説明を追加
        self._add_technique_explanations(session)
        
        # セッションを保存
        self.sessions[session.id] = session
        
        # セッション開始の案内を生成
        result = self._format_session_start(session)
        
        return result
    
    async def apply_technique(self, session_id: str, technique: str, 
                            ideas: List[str], explanations: Optional[List[str]] = None) -> str:
        """指定されたSCAMPER技法でアイデアを生成する"""
        
        if session_id not in self.sessions:
            return f"エラー: セッションID '{session_id}' が見つかりません。"
        
        session = self.sessions[session_id]
        
        # 技法名を enum に変換
        try:
            scamper_technique = self._get_technique_enum(technique)
        except ValueError:
            return f"エラー: 無効な技法名 '{technique}' です。有効な技法: {', '.join([t.value for t in SCAMPERTechnique])}"
        
        session.active_technique = scamper_technique
        
        # アイデアを追加
        for i, idea in enumerate(ideas):
            explanation = explanations[i] if explanations and i < len(explanations) else ""
            scamper_idea = SCAMPERIdea(scamper_technique, idea, explanation)
            session.ideas.append(scamper_idea)
        
        session.updated_at = datetime.now()
        
        # 技法固有の質問とガイダンスを追加
        guidance = self._get_technique_guidance(scamper_technique, session.topic)
        session.session_notes.append(f"{scamper_technique.value}技法を適用: {len(ideas)}個のアイデアを生成")
        
        # 結果を整形して返す
        result = self._format_technique_result(session, scamper_technique, ideas, guidance)
        
        return result
    
    async def evaluate_ideas(self, session_id: str, idea_evaluations: List[Dict]) -> str:
        """生成されたアイデアを評価する"""
        
        if session_id not in self.sessions:
            return f"エラー: セッションID '{session_id}' が見つかりません。"
        
        session = self.sessions[session_id]
        
        for evaluation in idea_evaluations:
            idea_text = evaluation.get("idea", "")
            feasibility = evaluation.get("feasibility", 0)
            impact = evaluation.get("impact", 0)
            
            # 該当するアイデアを探して評価を追加
            for idea in session.ideas:
                if idea.idea == idea_text:
                    idea.feasibility_score = feasibility
                    idea.impact_score = impact
                    break
        
        session.updated_at = datetime.now()
        session.session_notes.append(f"アイデア評価を完了: {len(idea_evaluations)}個のアイデアを評価")
        
        # 評価結果を整形して返す
        result = self._format_evaluation_result(session)
        
        return result
    
    async def get_session(self, session_id: str) -> str:
        """SCAMPERセッションの現在の状況を取得する"""
        
        if session_id not in self.sessions:
            return f"エラー: セッションID '{session_id}' が見つかりません。"
        
        session = self.sessions[session_id]
        
        return self._format_session_summary(session)
    
    async def list_sessions(self) -> str:
        """すべてのSCAMPERセッションの一覧を取得する"""
        
        if not self.sessions:
            return "現在アクティブなSCAMPERセッションはありません。"
        
        result = "SCAMPERセッション一覧:\n\n"
        
        for session in sorted(self.sessions.values(), key=lambda x: x.updated_at, reverse=True):
            result += f"セッションID: {session.id}\n"
            result += f"トピック: {session.topic}\n"
            result += f"アイデア数: {len(session.ideas)}\n"
            result += f"作成日時: {session.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            result += f"更新日時: {session.updated_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            result += "─" * 50 + "\n"
        
        return result
    
    async def generate_comprehensive_ideas(self, topic: str, current_situation: str, 
                                         context: Optional[str] = None) -> str:
        """全てのSCAMPER技法を適用して包括的なアイデアを生成する"""
        
        session = SCAMPERSession(topic, current_situation)
        
        if context:
            session.session_notes.append(f"背景情報: {context}")
        
        # 各技法でアイデア生成
        for technique in SCAMPERTechnique:
            ideas = self._generate_ideas_for_technique(technique, topic, current_situation)
            for idea in ideas:
                scamper_idea = SCAMPERIdea(technique, idea["text"], idea["explanation"])
                session.ideas.append(scamper_idea)
        
        session.session_notes.append("全SCAMPER技法を適用した包括的アイデア生成を完了")
        
        # セッションを保存
        self.sessions[session.id] = session
        
        # 結果を整形して返す
        result = self._format_comprehensive_result(session)
        
        return result
    
    def _get_technique_enum(self, technique: str) -> SCAMPERTechnique:
        """技法名文字列をenumに変換する"""
        
        technique_map = {
            "substitute": SCAMPERTechnique.SUBSTITUTE,
            "代替": SCAMPERTechnique.SUBSTITUTE,
            "combine": SCAMPERTechnique.COMBINE,
            "結合": SCAMPERTechnique.COMBINE,
            "adapt": SCAMPERTechnique.ADAPT,
            "応用": SCAMPERTechnique.ADAPT,
            "modify": SCAMPERTechnique.MODIFY,
            "変更": SCAMPERTechnique.MODIFY,
            "put_to_other_use": SCAMPERTechnique.PUT_TO_OTHER_USE,
            "転用": SCAMPERTechnique.PUT_TO_OTHER_USE,
            "eliminate": SCAMPERTechnique.ELIMINATE,
            "除去": SCAMPERTechnique.ELIMINATE,
            "reverse": SCAMPERTechnique.REVERSE,
            "逆転": SCAMPERTechnique.REVERSE
        }
        
        technique_lower = technique.lower()
        if technique_lower in technique_map:
            return technique_map[technique_lower]
        
        raise ValueError(f"無効な技法名: {technique}")
    
    def _get_technique_guidance(self, technique: SCAMPERTechnique, topic: str) -> str:
        """技法固有のガイダンスを生成する"""
        
        guidance_map = {
            SCAMPERTechnique.SUBSTITUTE: [
                "何を他のもので置き換えることができるか？",
                "材料、プロセス、人、場所を変えるとどうなるか？",
                "類似した問題はどのように解決されているか？"
            ],
            SCAMPERTechnique.COMBINE: [
                "何と何を組み合わせることができるか？",
                "異なる要素やアイデアを統合できるか？",
                "複数の機能を一つにまとめられるか？"
            ],
            SCAMPERTechnique.ADAPT: [
                "他の分野のアイデアを適用できるか？",
                "過去の経験から学べることはあるか？",
                "自然界の仕組みを模倣できるか？"
            ],
            SCAMPERTechnique.MODIFY: [
                "何を拡大・縮小できるか？",
                "何を強調・弱化できるか？",
                "形、色、音、匂いを変えられるか？"
            ],
            SCAMPERTechnique.PUT_TO_OTHER_USE: [
                "他の用途に使えないか？",
                "異なる市場や顧客層に適用できるか？",
                "副産物や派生的な使い方はあるか？"
            ],
            SCAMPERTechnique.ELIMINATE: [
                "何を取り除くことができるか？",
                "何を簡素化できるか？",
                "何が本当に必要不可欠か？"
            ],
            SCAMPERTechnique.REVERSE: [
                "順序を逆にするとどうなるか？",
                "役割を入れ替えるとどうなるか？",
                "正反対のアプローチは可能か？"
            ]
        }
        
        questions = guidance_map.get(technique, [])
        return "\n".join(f"• {question}" for question in questions)
    
    def _generate_ideas_for_technique(self, technique: SCAMPERTechnique, 
                                    topic: str, current_situation: str) -> List[Dict]:
        """指定された技法でアイデアを自動生成する"""
        
        ideas = []
        
        if technique == SCAMPERTechnique.SUBSTITUTE:
            ideas = [
                {"text": f"{topic}の主要要素を代替品で置き換える", "explanation": "コストや効率を改善できる可能性"},
                {"text": f"従来の方法を新しいアプローチで代替する", "explanation": "イノベーションの機会を探る"},
                {"text": f"人手による作業を自動化で代替する", "explanation": "効率化と品質向上を図る"}
            ]
        elif technique == SCAMPERTechnique.COMBINE:
            ideas = [
                {"text": f"{topic}を関連する他のサービスと統合する", "explanation": "ワンストップソリューションの提供"},
                {"text": f"複数の機能を一つのプラットフォームに組み合わせる", "explanation": "利便性の向上とコスト削減"},
                {"text": f"異なる専門知識を組み合わせる", "explanation": "シナジー効果による価値創造"}
            ]
        elif technique == SCAMPERTechnique.ADAPT:
            ideas = [
                {"text": f"他業界の成功事例を{topic}に適用する", "explanation": "実績のあるモデルの応用"},
                {"text": f"自然界の仕組みを模倣したアプローチ", "explanation": "バイオミメティクスの活用"},
                {"text": f"過去の経験や知識を現在の課題に適用する", "explanation": "学習効果の活用"}
            ]
        elif technique == SCAMPERTechnique.MODIFY:
            ideas = [
                {"text": f"{topic}の規模を大幅に拡大する", "explanation": "スケールメリットの追求"},
                {"text": f"プロセスの速度を大幅に向上させる", "explanation": "効率性の劇的改善"},
                {"text": f"品質レベルを段階的に向上させる", "explanation": "継続的改善アプローチ"}
            ]
        elif technique == SCAMPERTechnique.PUT_TO_OTHER_USE:
            ideas = [
                {"text": f"{topic}を全く異なる分野に応用する", "explanation": "新市場の開拓機会"},
                {"text": f"副産物や廃棄物を有効活用する", "explanation": "サステナビリティの向上"},
                {"text": f"既存のスキルを新しい領域で活用する", "explanation": "リソースの最適活用"}
            ]
        elif technique == SCAMPERTechnique.ELIMINATE:
            ideas = [
                {"text": f"{topic}から不要なプロセスを除去する", "explanation": "シンプル化による効率向上"},
                {"text": f"コストのかかる要素を削減する", "explanation": "経済性の改善"},
                {"text": f"複雑さを排除してユーザビリティを向上する", "explanation": "使いやすさの追求"}
            ]
        elif technique == SCAMPERTechnique.REVERSE:
            ideas = [
                {"text": f"{topic}のプロセスを逆順で実行する", "explanation": "新しい視点からの問題解決"},
                {"text": f"従来の役割を逆転させる", "explanation": "権限委譲や責任の再配分"},
                {"text": f"顧客の期待と正反対のアプローチを試す", "explanation": "差別化戦略の創出"}
            ]
        
        return ideas[:3]  # 各技法につき3つのアイデア
    
    def _add_technique_explanations(self, session: SCAMPERSession):
        """技法の説明をセッションに追加する"""
        
        explanations = {
            "S - Substitute（代替）": "何かを別のもので置き換えることで新しいアイデアを生み出す",
            "C - Combine（結合）": "2つ以上の要素を組み合わせて新しい価値を創造する", 
            "A - Adapt（応用）": "他の分野やアイデアを現在の課題に適用する",
            "M - Modify（変更）": "既存のものを変更・拡大・縮小して改善する",
            "P - Put to other use（転用）": "他の用途や目的に使用する方法を考える",
            "E - Eliminate（除去）": "不要な要素を取り除いて簡素化する",
            "R - Reverse（逆転）": "順序や役割を逆にして新しい可能性を探る"
        }
        
        for technique, explanation in explanations.items():
            session.session_notes.append(f"{technique}: {explanation}")
    
    def _format_session_start(self, session: SCAMPERSession) -> str:
        """セッション開始時の案内を整形する"""
        
        result = f"🎯 SCAMPERセッション開始 (ID: {session.id})\n\n"
        result += f"対象トピック: {session.topic}\n"
        result += f"現在の状況: {session.current_situation}\n\n"
        
        result += "🔧 SCAMPER技法の概要:\n"
        result += "• S - Substitute（代替）: 何かを別のもので置き換える\n"
        result += "• C - Combine（結合）: 複数の要素を組み合わせる\n" 
        result += "• A - Adapt（応用）: 他のアイデアを適用する\n"
        result += "• M - Modify（変更）: 既存のものを変更・改善する\n"
        result += "• P - Put to other use（転用）: 他の用途に使う\n"
        result += "• E - Eliminate（除去）: 不要な要素を取り除く\n"
        result += "• R - Reverse（逆転）: 順序や役割を逆にする\n\n"
        
        result += "💡 使い方:\n"
        result += "• scamper_apply_technique でお好みの技法を選んで適用\n"
        result += "• scamper_generate_comprehensive で全技法を一度に適用\n"
        result += "• scamper_evaluate_ideas でアイデアを評価\n\n"
        
        result += "各技法を活用して創造的なアイデアを発見しましょう！"
        
        return result
    
    def _format_technique_result(self, session: SCAMPERSession, technique: SCAMPERTechnique,
                               ideas: List[str], guidance: str) -> str:
        """技法適用結果を整形する"""
        
        result = f"🔧 {technique.value}技法の適用結果\n\n"
        result += f"セッション: {session.topic}\n\n"
        
        result += "💡 生成されたアイデア:\n"
        for i, idea in enumerate(ideas, 1):
            result += f"{i}. {idea}\n"
        result += "\n"
        
        result += f"❓ {technique.value}技法の思考ガイド:\n"
        result += f"{guidance}\n\n"
        
        result += f"📊 セッション統計:\n"
        result += f"• 総アイデア数: {len(session.ideas)}\n"
        result += f"• 適用済み技法数: {len(set(idea.technique for idea in session.ideas))}\n"
        
        return result
    
    def _format_evaluation_result(self, session: SCAMPERSession) -> str:
        """評価結果を整形する"""
        
        result = f"📊 アイデア評価結果\n\n"
        result += f"セッション: {session.topic}\n\n"
        
        # スコア順にソート
        sorted_ideas = sorted([idea for idea in session.ideas if idea.feasibility_score > 0], 
                            key=lambda x: (x.feasibility_score + x.impact_score), reverse=True)
        
        result += "🏆 評価済みアイデア (実現可能性 + インパクトの合計順):\n"
        for i, idea in enumerate(sorted_ideas[:10], 1):  # 上位10個
            total_score = idea.feasibility_score + idea.impact_score
            result += f"{i}. {idea.idea}\n"
            result += f"   技法: {idea.technique.value}\n"
            result += f"   実現可能性: {idea.feasibility_score}/10, インパクト: {idea.impact_score}/10\n"
            result += f"   総合スコア: {total_score}/20\n"
            if idea.explanation:
                result += f"   説明: {idea.explanation}\n"
            result += "\n"
        
        # 技法別統計
        technique_stats: Dict[SCAMPERTechnique, List[int]] = {}
        for idea in session.ideas:
            if idea.feasibility_score > 0:
                if idea.technique not in technique_stats:
                    technique_stats[idea.technique] = []
                technique_stats[idea.technique].append(idea.feasibility_score + idea.impact_score)
        
        result += "📈 技法別平均スコア:\n"
        for technique, scores in technique_stats.items():
            avg_score = sum(scores) / len(scores)
            result += f"• {technique.value}: {avg_score:.1f}/20\n"
        
        return result
    
    def _format_session_summary(self, session: SCAMPERSession) -> str:
        """セッション概要を整形する"""
        
        result = f"📋 SCAMPERセッション概要 (ID: {session.id})\n\n"
        result += f"トピック: {session.topic}\n"
        result += f"現在の状況: {session.current_situation}\n"
        result += f"作成日時: {session.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        result += f"更新日時: {session.updated_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # 技法別アイデア統計
        technique_counts = {}
        for idea in session.ideas:
            if idea.technique not in technique_counts:
                technique_counts[idea.technique] = 0
            technique_counts[idea.technique] += 1
        
        result += "🔧 技法別アイデア数:\n"
        for technique, count in technique_counts.items():
            result += f"• {technique.value}: {count}個\n"
        result += f"\n総アイデア数: {len(session.ideas)}個\n\n"
        
        # 最新のアイデア表示
        if session.ideas:
            latest_ideas = sorted(session.ideas, key=lambda x: x.created_at, reverse=True)[:5]
            result += "💡 最新のアイデア（上位5個）:\n"
            for i, idea in enumerate(latest_ideas, 1):
                result += f"{i}. {idea.idea} ({idea.technique.value})\n"
                if idea.explanation:
                    result += f"   説明: {idea.explanation}\n"
        
        if session.session_notes:
            result += "\n📝 セッションメモ:\n"
            for note in session.session_notes[-3:]:  # 最新3つ
                result += f"• {note}\n"
        
        return result
    
    def _format_comprehensive_result(self, session: SCAMPERSession) -> str:
        """包括的アイデア生成結果を整形する"""
        
        result = f"🎯 SCAMPER包括的アイデア生成結果 (ID: {session.id})\n\n"
        result += f"対象トピック: {session.topic}\n"
        result += f"現在の状況: {session.current_situation}\n\n"
        
        # 技法別にアイデアを表示
        for technique in SCAMPERTechnique:
            technique_ideas = [idea for idea in session.ideas if idea.technique == technique]
            if technique_ideas:
                result += f"🔧 {technique.value}技法のアイデア:\n"
                for i, idea in enumerate(technique_ideas, 1):
                    result += f"   {i}. {idea.idea}\n"
                    if idea.explanation:
                        result += f"      説明: {idea.explanation}\n"
                result += "\n"
        
        result += f"📊 生成統計:\n"
        result += f"• 総アイデア数: {len(session.ideas)}個\n"
        result += f"• 適用技法数: {len(SCAMPERTechnique)}技法\n"
        result += f"• 技法あたり平均: {len(session.ideas)/len(SCAMPERTechnique):.1f}個\n\n"
        
        result += "💡 次のステップ:\n"
        result += "• scamper_evaluate_ideas でアイデアを評価する\n"
        result += "• 有望なアイデアを詳細検討する\n"
        result += "• 複数のアイデアを組み合わせてより良いソリューションを作る"
        
        return result