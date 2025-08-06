思考支援MCPサーバー
=========================

> **注記**: このリポジトリのすべてのコードはClaude Codeによって生成されました。

3つの思考方法をサポートするMCPサーバーです：

- 段階的思考: 複雑な問題を段階的なステップに分解
- クリティカルシンキング: 情報を批判的に分析・評価  
- ロジカルシンキング: 論理的な論証構築と因果関係分析

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

#### 段階的思考

- `stepwise_create_plan`: 問題を段階的なステップに分解
- `stepwise_execute_step`: 各ステップの実行と記録

#### クリティカルシンキング  

- `critical_analyze_claim`: 主張や情報の信頼性を評価
- `critical_identify_bias`: 偏見や論理的誤謬を特定

#### ロジカルシンキング

- `logical_build_argument`: 論理的な論証を構築
- `logical_find_causality`: 原因と結果の関係を分析

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
