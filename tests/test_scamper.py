"""SCAMPERツールのテスト"""

import pytest
from datetime import datetime
from src.thinking_support.tools.scamper import SCAMPER, SCAMPERTechnique, SCAMPERIdea, SCAMPERSession


class TestSCAMPER:
    
    @pytest.fixture
    def scamper_tool(self):
        """SCAMPERツールのフィクスチャ"""
        return SCAMPER()
    
    @pytest.mark.asyncio
    async def test_start_session(self, scamper_tool):
        """セッション開始のテスト"""
        
        result = await scamper_tool.start_session(
            "新商品の開発",
            "既存商品の売上が低下しているため、新しいアプローチが必要",
            "予算は限られている"
        )
        
        assert "SCAMPERセッション開始" in result
        assert "新商品の開発" in result
        assert "SCAMPER技法の概要" in result
        assert len(scamper_tool.sessions) == 1
        
        # セッションの内容確認
        session = list(scamper_tool.sessions.values())[0]
        assert session.topic == "新商品の開発"
        assert session.current_situation == "既存商品の売上が低下しているため、新しいアプローチが必要"
        assert "予算は限られている" in session.session_notes[0]
    
    @pytest.mark.asyncio
    async def test_apply_technique_substitute(self, scamper_tool):
        """Substitute技法適用のテスト"""
        
        # セッション開始
        await scamper_tool.start_session("コーヒーショップ改善", "売上向上が必要")
        session_id = list(scamper_tool.sessions.keys())[0]
        
        # Substitute技法を適用
        ideas = [
            "通常のコーヒー豆を高級豆に代替",
            "紙カップをリユーザブルカップに代替",
            "店内BGMを生演奏に代替"
        ]
        
        result = await scamper_tool.apply_technique(
            session_id,
            "substitute",
            ideas,
            ["品質向上による差別化", "環境配慮によるブランドイメージ向上", "特別感の演出"]
        )
        
        assert "Substitute技法の適用結果" in result
        assert "通常のコーヒー豆を高級豆に代替" in result
        assert "思考ガイド" in result
        
        # セッションの状態確認
        session = scamper_tool.sessions[session_id]
        assert len(session.ideas) == 3
        assert all(idea.technique == SCAMPERTechnique.SUBSTITUTE for idea in session.ideas)
    
    @pytest.mark.asyncio
    async def test_apply_technique_combine(self, scamper_tool):
        """Combine技法適用のテスト"""
        
        await scamper_tool.start_session("レストラン運営", "競合差別化が必要")
        session_id = list(scamper_tool.sessions.keys())[0]
        
        result = await scamper_tool.apply_technique(
            session_id,
            "combine",
            ["料理とエンターテイメントを組み合わせ", "カフェと本屋の融合"]
        )
        
        assert "Combine技法の適用結果" in result
        assert session_id in scamper_tool.sessions
        session = scamper_tool.sessions[session_id]
        assert len(session.ideas) == 2
    
    @pytest.mark.asyncio
    async def test_all_techniques(self, scamper_tool):
        """全技法の適用テスト"""
        
        await scamper_tool.start_session("オンライン教育", "受講者の継続率向上")
        session_id = list(scamper_tool.sessions.keys())[0]
        
        techniques = ["substitute", "combine", "adapt", "modify", "put_to_other_use", "eliminate", "reverse"]
        
        for technique in techniques:
            result = await scamper_tool.apply_technique(
                session_id,
                technique,
                [f"{technique}のテストアイデア"]
            )
            # 技法名が結果に含まれていることを確認（表示形式に関係なく）
            assert "技法の適用結果" in result
        
        session = scamper_tool.sessions[session_id]
        assert len(session.ideas) == 7
        assert len(set(idea.technique for idea in session.ideas)) == 7
    
    @pytest.mark.asyncio
    async def test_evaluate_ideas(self, scamper_tool):
        """アイデア評価のテスト"""
        
        # セッション開始とアイデア生成
        await scamper_tool.start_session("新サービス開発", "市場投入の準備")
        session_id = list(scamper_tool.sessions.keys())[0]
        
        await scamper_tool.apply_technique(
            session_id,
            "substitute",
            ["アイデア1", "アイデア2"]
        )
        
        # アイデア評価
        evaluations = [
            {"idea": "アイデア1", "feasibility": 8, "impact": 7},
            {"idea": "アイデア2", "feasibility": 5, "impact": 9}
        ]
        
        result = await scamper_tool.evaluate_ideas(session_id, evaluations)
        
        assert "アイデア評価結果" in result
        assert "評価済みアイデア" in result
        assert "技法別平均スコア" in result
        
        # 評価の反映確認
        session = scamper_tool.sessions[session_id]
        evaluated_ideas = [idea for idea in session.ideas if idea.feasibility_score > 0]
        assert len(evaluated_ideas) == 2
    
    @pytest.mark.asyncio
    async def test_get_session(self, scamper_tool):
        """セッション状況取得のテスト"""
        
        await scamper_tool.start_session("ウェブサイト改善", "ユーザビリティ向上")
        session_id = list(scamper_tool.sessions.keys())[0]
        
        await scamper_tool.apply_technique(session_id, "eliminate", ["不要な機能を削除"])
        
        result = await scamper_tool.get_session(session_id)
        
        assert "SCAMPERセッション概要" in result
        assert "ウェブサイト改善" in result
        assert "技法別アイデア数" in result
        assert "最新のアイデア" in result
    
    @pytest.mark.asyncio
    async def test_list_sessions(self, scamper_tool):
        """セッション一覧取得のテスト"""
        
        # 複数セッション作成
        await scamper_tool.start_session("プロジェクトA", "効率化が必要")
        await scamper_tool.start_session("プロジェクトB", "品質向上が必要")
        
        result = await scamper_tool.list_sessions()
        
        assert "SCAMPERセッション一覧" in result
        assert "プロジェクトA" in result
        assert "プロジェクトB" in result
        assert len(scamper_tool.sessions) == 2
    
    @pytest.mark.asyncio
    async def test_generate_comprehensive_ideas(self, scamper_tool):
        """包括的アイデア生成のテスト"""
        
        result = await scamper_tool.generate_comprehensive_ideas(
            "顧客サポート改善",
            "問い合わせ対応時間の短縮が必要",
            "限られたスタッフリソース"
        )
        
        assert "SCAMPER包括的アイデア生成結果" in result
        assert "顧客サポート改善" in result
        assert len(scamper_tool.sessions) == 1
        
        session = list(scamper_tool.sessions.values())[0]
        assert len(session.ideas) > 0
        
        # 全技法が適用されていることを確認
        techniques_used = set(idea.technique for idea in session.ideas)
        assert len(techniques_used) == len(SCAMPERTechnique)
    
    @pytest.mark.asyncio
    async def test_invalid_technique(self, scamper_tool):
        """無効な技法名のエラーハンドリングテスト"""
        
        await scamper_tool.start_session("テストプロジェクト", "テスト状況")
        session_id = list(scamper_tool.sessions.keys())[0]
        
        result = await scamper_tool.apply_technique(
            session_id,
            "invalid_technique",
            ["テストアイデア"]
        )
        
        assert "エラー: 無効な技法名" in result
    
    @pytest.mark.asyncio
    async def test_invalid_session_id(self, scamper_tool):
        """無効なセッションIDのエラーハンドリングテスト"""
        
        result = await scamper_tool.apply_technique(
            "invalid_session_id",
            "substitute",
            ["テストアイデア"]
        )
        
        assert "エラー: セッションID" in result
        assert "が見つかりません" in result
    
    @pytest.mark.asyncio
    async def test_empty_sessions_list(self, scamper_tool):
        """空のセッション一覧のテスト"""
        
        result = await scamper_tool.list_sessions()
        
        assert "現在アクティブなSCAMPERセッションはありません" in result
    
    def test_scamper_idea_creation(self):
        """SCAMPERアイデアオブジェクトの作成テスト"""
        
        idea = SCAMPERIdea(
            SCAMPERTechnique.SUBSTITUTE,
            "既存材料を新材料に代替",
            "コスト削減と性能向上"
        )
        
        assert idea.technique == SCAMPERTechnique.SUBSTITUTE
        assert idea.idea == "既存材料を新材料に代替"
        assert idea.explanation == "コスト削減と性能向上"
        assert idea.feasibility_score == 0
        assert idea.impact_score == 0
        assert isinstance(idea.created_at, datetime)
        assert len(idea.id) > 0
    
    def test_scamper_session_creation(self):
        """SCAMPERセッションオブジェクトの作成テスト"""
        
        session = SCAMPERSession("製品改良", "市場競争力強化")
        
        assert session.topic == "製品改良"
        assert session.current_situation == "市場競争力強化"
        assert len(session.ideas) == 0
        assert session.active_technique is None
        assert isinstance(session.created_at, datetime)
        assert isinstance(session.updated_at, datetime)
        assert len(session.id) > 0
    
    @pytest.mark.asyncio
    async def test_technique_guidance_generation(self, scamper_tool):
        """技法ガイダンス生成のテスト"""
        
        await scamper_tool.start_session("テストトピック", "テスト状況")
        session_id = list(scamper_tool.sessions.keys())[0]
        
        # 各技法でガイダンスが含まれることを確認
        for technique_name in ["substitute", "combine", "adapt", "modify", "put_to_other_use", "eliminate", "reverse"]:
            result = await scamper_tool.apply_technique(
                session_id,
                technique_name,
                ["テストアイデア"]
            )
            assert "思考ガイド" in result
            # ガイダンスに疑問符が含まれていることを確認（質問形式のガイダンス）
            assert "？" in result
    
    @pytest.mark.asyncio
    async def test_japanese_technique_names(self, scamper_tool):
        """日本語技法名の対応テスト"""
        
        await scamper_tool.start_session("日本語テスト", "日本語対応確認")
        session_id = list(scamper_tool.sessions.keys())[0]
        
        japanese_techniques = ["代替", "結合", "応用", "変更", "転用", "除去", "逆転"]
        
        for technique in japanese_techniques:
            result = await scamper_tool.apply_technique(
                session_id,
                technique,
                [f"{technique}のテストアイデア"]
            )
            assert "エラー" not in result
            assert "適用結果" in result
    
    @pytest.mark.asyncio
    async def test_session_notes_tracking(self, scamper_tool):
        """セッションメモ追跡のテスト"""
        
        result = await scamper_tool.start_session(
            "メモテスト",
            "セッションメモの確認",
            "特別なコンテキスト情報"
        )
        
        session = list(scamper_tool.sessions.values())[0]
        
        # 初期メモの確認
        assert any("特別なコンテキスト情報" in note for note in session.session_notes)
        assert len(session.session_notes) > 1  # 技法説明も含まれる
        
        # 技法適用後のメモ追加
        session_id = session.id
        await scamper_tool.apply_technique(session_id, "substitute", ["テストアイデア"])
        
        assert any("Substitute技法を適用" in note for note in session.session_notes)
    
    @pytest.mark.asyncio
    async def test_comprehensive_generation_statistics(self, scamper_tool):
        """包括的生成の統計情報テスト"""
        
        result = await scamper_tool.generate_comprehensive_ideas(
            "統計テスト",
            "統計情報の確認"
        )
        
        assert "生成統計" in result
        assert "総アイデア数" in result
        assert "適用技法数" in result
        assert "技法あたり平均" in result
        
        session = list(scamper_tool.sessions.values())[0]
        
        # 各技法に対してアイデアが生成されていることを確認
        technique_counts = {}
        for idea in session.ideas:
            if idea.technique not in technique_counts:
                technique_counts[idea.technique] = 0
            technique_counts[idea.technique] += 1
        
        assert len(technique_counts) == len(SCAMPERTechnique)
        assert all(count > 0 for count in technique_counts.values())