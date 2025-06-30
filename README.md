# ChimeraX-PLDDTColor

A ChimeraX bundle for automatic coloring of atoms based on pLDDT values. Especially useful for visualizing AlphaFold3 predictions and other structure quality metrics.

## Overview

This bundle provides functionality to automatically color atoms and ribbons in protein structures based on pLDDT values (stored as B-factors). It visually represents the prediction confidence for each residue, making it easy to assess model quality at a glance.

## Features

- **Automatic coloring**: Colors atoms based on pLDDT values
- **Cartoon color update**: Cartoon colors are updated to match the average pLDDT values of residue atoms
- **Statistics display**: Detailed statistics for each processed model are shown as an HTML table
- **Multi-model support**: Processes all models in the session simultaneously
- **Flexible atom selection**: Color all atoms, selected atoms, or atoms in specific models

## Color Scheme

| Confidence      | pLDDT Value | Color        | Description            |
|----------------|-------------|--------------|------------------------|
| Very high      | 90-100      | Blue (#0053D6)   | Very high confidence   |
| High           | 70-89       | Cyan (#65CBE3)   | High confidence        |
| Medium         | 50-69       | Yellow (#FFDB13) | Medium confidence      |
| Low            | 0-49        | Orange (#FF7D45) | Low confidence         |

## Installation

**Note:** This bundle is not distributed via ChimeraX Toolshed. Please use the installation method below.

1. Clone this repository:

```sh
git clone https://github.com/N283T/chimerax-plddtcolor.git
cd chimerax-plddtcolor
pwd  # Note the absolute path for the next step
```

2. Start ChimeraX and run the following command in the ChimeraX command line:

```
devel install /absolute/path/to/chimerax-plddtcolor
```
(Use the path shown by `pwd` above)

3. (Optional) To remove temporary build files, run:

```
devel clean /absolute/path/to/chimerax-plddtcolor
```

## Usage

### Basic Usage

Color all atoms in all models by pLDDT value:
```
plddt
```

Color atoms in a specific model:
```
plddt #1
```
```
plddt #1,2
```

### Command Syntax

```
plddt [atoms]
```

**Arguments:**
- `atoms` (optional): Specify which atoms to color. If omitted, all atoms in all models are colored.

## Output

The bundle logs the following information:

- List of processed models
- Number of atoms colored at each pLDDT threshold
- Statistics (min, max, mean, median, standard deviation, total atom count)

Statistics are displayed as an HTML table for easy comparison across models.

**Cartoon Coloring:** Cartoon colors are automatically updated based on the average pLDDT values of all atoms in each residue. This provides a residue-level view of prediction confidence that complements the atom-level coloring.

## License

This project is licensed under the BSD 3-Clause License. See [LICENSE](LICENSE) for details.

---

# ChimeraX-PLDDTColor

pLDDT値に基づく原子の自動色分けを行うChimeraXバンドルです。AlphaFold3予測結果やその他の構造品質指標の可視化に特に有用です。

## 概要

このバンドルは、タンパク質構造の品質指標（pLDDT値）に基づいて原子とリボンを自動的に色分けする機能を提供します。B-factor値として保存されているpLDDT値を使用して、タンパク質の予測精度を視覚的に表現します。

## 機能

- **自動色分け**: pLDDT値に基づく原子の自動色分け
- **リボン(Cartoon)色更新**: リボンの色は残基内の原子のpLDDT値の平均に基づいて更新されます
- **統計情報表示**: 処理されたモデルの詳細な統計情報をHTMLテーブルで表示
- **複数モデル対応**: セッション内の複数のモデルを同時に処理
- **柔軟な原子選択**: すべての原子、選択された原子、または特定のモデルの原子を色分け

## 色分けスキーム

| 信頼度 | pLDDT値 | 色 | 説明 |
|--------|---------|-----|------|
| 非常に高い | 90-100 | 青 (#0053D6) | 非常に高い信頼度 |
| 高い | 70-89 | 水色 (#65CBE3) | 高い信頼度 |
| 中程度 | 50-69 | 黄 (#FFDB13) | 中程度の信頼度 |
| 低い | 0-49 | オレンジ (#FF7D45) | 低い信頼度 |

## インストール

**注意:** このバンドルはChimeraX Toolshedでは配布していません。以下のインストール方法をご利用ください。

1. リポジトリをクローン:

```sh
git clone https://github.com/N283T/chimerax-plddtcolor.git
cd chimerax-plddtcolor
pwd  # 次のステップで使用する絶対パスをメモしてください
```

2. ChimeraXを起動し、ChimeraXコマンドラインで以下のコマンドを実行:

```
devel install /absolute/path/to/chimerax-plddtcolor
```
（上記の`pwd`で表示されたパスを使用してください）

3. （オプション）一時的なビルドファイルを削除する場合:

```
devel clean /absolute/path/to/chimerax-plddtcolor
```

## 使用方法

### 基本的な使用方法

すべてのモデルの原子をpLDDT値で色分け:
```
plddt
```

特定のモデルの原子を色分け:
```
plddt #1
```
```
plddt #1,2
```

### コマンド構文

```
plddt [atoms]
```

**引数:**
- `atoms` (オプション): 色分けする原子を指定します。省略した場合、すべてのモデルの原子が対象になります。

## 出力

バンドルは以下の情報をログに表示します:

- 処理されたモデルのリスト
- 各pLDDT閾値で色分けされた原子数
- 統計情報（最小値、最大値、平均値、中央値、標準偏差、総原子数）

統計情報はHTMLテーブル形式で表示され、複数モデルの比較が容易です。

**リボン色分け:** リボンの色は各残基内のすべての原子のpLDDT値の平均に基づいて自動的に更新されます。これにより、原子レベルの色分けを補完する残基レベルの予測信頼度の視覚化が提供されます。

## ライセンス

このプロジェクトはBSD 3-Clause Licenseの下で公開されています。詳細は[LICENSE](LICENSE)を参照してください。