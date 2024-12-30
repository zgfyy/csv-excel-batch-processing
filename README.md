### README.md

```markdown
# CSV/Excel 批量处理工具

## 项目简介

`csv-excel-batch-processing` 是一个用于批量处理 CSV 和 Excel 文件的工具。它支持多种操作，如合并文件、转换数据类型、处理缺失值等。通过灵活的配置选项，用户可以轻松自定义处理逻辑，满足不同的需求。

## 功能亮点

- **多文件格式支持**：支持 CSV 和 Excel 文件（.csv, .xlsx, .xls）。
- **批量处理**：一次性处理多个文件，生成合并后的输出文件。
- **灵活的配置**：通过配置文件或命令行参数自定义处理规则。
- **图形界面 (GUI)**：提供简单的 GUI 界面，方便用户更改设置。
- **错误处理**：可以选择跳过错误文件，避免中断整个处理流程。
- **自定义规则**：支持用户定义复杂的处理规则，如列操作、数据转换等。
- **云存储支持**（可选）：支持从云存储（如 Google Drive、OneDrive）导入和导出文件。

## 安装指南

### 克隆仓库

首先，克隆本项目的 Git 仓库：

```bash
git clone https://github.com/zgfyy/csv-excel-batch-processing.git
cd csv-excel-batch-processing
```

### 安装依赖

我们推荐使用 Python 虚拟环境来管理依赖。你可以使用 `venv` 或 `conda` 创建虚拟环境。

#### 使用 `venv`：

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/MacOS
# 或者
venv\Scripts\activate  # Windows
```

#### 安装依赖包：

```bash
pip install -r requirements.txt
```

### 配置文件

项目默认使用 `config/config.ini` 作为配置文件。你可以根据需要修改该文件，或者通过命令行参数覆盖其中的设置。

如果你想要生成一个新的配置文件模板，可以运行以下命令：

```bash
python src/main.py --generate-config
```

这将在 `config/` 目录下生成一个 `config_template.ini` 文件，你可以根据模板创建自己的配置文件。

## 使用方法

### 命令行模式

你可以通过命令行运行工具，并传递相关参数。以下是常用的命令行选项：

```bash
python src/main.py --input-directory ./data/input --output-file ./data/output/merged_data.csv --key-columns id name --skip-errors --overwrite-output
```

| 参数               | 描述                                                         | 默认值                        |
|--------------------|--------------------------------------------------------------|-------------------------------|
| `--input-directory` | 输入文件夹路径，包含要处理的 CSV/Excel 文件。                 | `./data/input`                |
| `--output-file`    | 输出文件路径，保存合并后的结果。                             | `./data/output/merged_data.csv`|
| `--key-columns`    | 用于合并文件的关键列（多个列名用空格分隔）。                  | 空                           |
| `--skip-errors`    | 是否跳过错误文件，避免中断整个处理流程。                      | `False`                       |
| `--overwrite-output` | 是否覆盖现有输出文件。                                       | `False`                       |
| `--config`         | 指定自定义配置文件路径。                                     | `config/config.ini`           |

### 图形界面 (GUI) 模式

你也可以通过图形界面运行工具。启动 GUI 的命令如下：

```bash
python src/gui.py
```

在 GUI 中，你可以选择输入文件夹、输出文件路径、关键列等设置，并点击“开始处理”按钮执行批量处理。

### 自定义规则

你可以在 `config/config.ini` 中定义自定义规则，以实现更复杂的数据处理逻辑。例如：

```ini
[CustomRules]
column=price operation=convert_type type=float
column=age operation=dropna
column=sales operation=fillna value=0
```

每个规则由三部分组成：
- `column`：指定要操作的列名。
- `operation`：指定要执行的操作（如 `convert_type`、`dropna`、`fillna` 等）。
- `params`：操作所需的参数（如 `type`、`value` 等）。

## 测试

为了确保代码的正确性，项目包含了一组单元测试。你可以通过以下命令运行测试：

```bash
pytest tests/
```

## 许可证

本项目采用 [MIT License](LICENSE) 许可证。请参阅 `LICENSE` 文件了解详细信息。

## 贡献

欢迎贡献代码！如果你发现了问题或有改进建议，请提交 Issue 或 Pull Request。详细的贡献指南请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。
