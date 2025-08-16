思考支援MCPサーバー
=========================

> **注記**: このリポジトリのすべてのコードはClaude Codeによって生成されました。

8つの思考方法をサポートするMCPサーバーです

- 動的思考: 柔軟で反省的な問題解決プロセス（修正・分岐機能付き）
- 段階的思考: 複雑な問題を段階的なステップに分解
- クリティカルシンキング: 情報を批判的に分析・評価  
- ロジカルシンキング: 論理的な論証構築と因果関係分析
- 5Why分析: 根本原因を特定するための5回の「なぜ」の繰り返し
- MECE分析: 相互排他性と網羅性の原則による論理的分類・整理
- 弁証法: テーゼ、アンチテーゼ、ジンテーゼの三段階思考で矛盾を統合
- SCAMPER法: 7つの技法による創造的アイデア発想とイノベーション支援

インストール
-------------------------

```bash
uv sync
```

使用方法
-------------------------

### MCPサーバーとして起動

```bash
uv run thinking-support
```

### 利用可能なツール

#### 動的思考（Sequential Thinking）

- `sequential_thinking`: 柔軟で反省的な問題解決プロセス
    - 思考の修正・リビジョン機能
    - 思考の分岐処理（複数アプローチの並行探索）
    - 動的な思考数調整
    - リアルタイムな視覚的フォーマット表示

#### 段階的思考（Stepwise Thinking）

- `stepwise_create_plan`: 問題を段階的なステップに分解
- `stepwise_execute_step`: 各ステップの実行と記録

#### クリティカルシンキング  

- `critical_analyze_claim`: 主張や情報の信頼性を評価
- `critical_identify_bias`: 偏見や論理的誤謬を特定

#### ロジカルシンキング

- `logical_build_argument`: 論理的な論証を構築
- `logical_find_causality`: 原因と結果の関係を分析

#### 5Why分析

- `why_analysis_start`: 5Why分析を開始して問題を設定
- `why_analysis_add_answer`: Why質問に回答して次の質問を生成
- `why_analysis_get`: 分析の現在の状況を確認
- `why_analysis_list`: すべての分析の一覧を表示

#### MECE分析

- `mece_analyze_categories`: カテゴリのMECE原則適合性を分析
- `mece_create_structure`: トピックに対するMECE構造を提案

#### 弁証法

- `dialectical_start_process`: 弁証法プロセスを開始
- `dialectical_set_thesis`: テーゼ（正）の主張を設定
- `dialectical_set_antithesis`: アンチテーゼ（反）の反対意見を設定
- `dialectical_create_synthesis`: ジンテーゼ（合）の統合見解を構築
- `dialectical_analyze_contradiction`: 矛盾する立場の分析と統合提案
- `dialectical_get_process`: プロセス状況の確認
- `dialectical_list_processes`: 全プロセスの一覧表示

#### SCAMPER法

- `scamper_start_session`: SCAMPERセッションの開始
- `scamper_apply_technique`: 指定技法（Substitute/Combine/Adapt/Modify/Put to other use/Eliminate/Reverse）でのアイデア生成
- `scamper_evaluate_ideas`: アイデアの実現可能性・インパクト評価
- `scamper_get_session`: セッション状況の確認
- `scamper_list_sessions`: 全セッションの一覧表示
- `scamper_generate_comprehensive`: 全技法を適用した包括的アイデア生成

設定方法
-------------------------

### VSCode設定

VSCodeでMCPサーバーとして使用するには、`.vscode/mcp.json`ファイルを作成：

```json
{
  "servers": {
    "thinking-support": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "thinking-support"
      ],
      "cwd": "/path/to/mcp-thinking-support"
    }
  }
}
```

### Claude Desktop設定

Claude Desktopで使用するには、設定ファイルに以下を追加：

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "thinking-support": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/mcp-thinking-support",
        "thinking-support",
      ],
    }
  }
}
```

**注意**: `cwd`のパスは実際のプロジェクトディレクトリに変更してください。

開発
-------------------------

```bash
# 依存関係のインストール
uv sync

# 開発モードで実行
uv run python -m thinking_support.server
```
