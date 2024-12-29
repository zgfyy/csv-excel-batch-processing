# CSV/Excel 批量处理工具

## 简介

`csv-excel-batch-processing` 是一个用于批量处理CSV和Excel文件的Python工具。它可以执行数据清洗、转换、合并等操作，并支持多线程处理以提高效率。此外，该工具还提供了图形用户界面（GUI）和命令行接口（CLI），方便用户根据需求选择合适的操作方式。

### 功能亮点
- **数据清洗**：自动检测并修复数据中的错误，如缺失值、重复行等。
- **数据转换**：支持自定义规则对数据进行转换，例如格式化日期、转换数据类型等。
- **文件合并**：可以按指定的关键列合并多个CSV或Excel文件。
- **多线程处理**：利用多线程技术加速大批量文件的处理。
- **报告生成**：处理完成后自动生成统计图表和文本报告，帮助用户分析数据。
- **错误处理**：可以选择跳过处理过程中出现错误的文件，确保其他文件的正常处理。
- **配置文件支持**：允许用户通过配置文件设置默认参数，简化操作流程。

## 安装

### 1. 克隆仓库

首先，克隆本项目的GitHub仓库到本地：

```bash
git clone https://github.com/your-username/csv-excel-batch-processing.git
cd csv-excel-batch-processing
```

### 2. 创建虚拟环境（推荐）

为了隔离项目依赖，建议创建一个Python虚拟环境：

```bash
python -m venv venv
```

激活虚拟环境：

- **Windows**:
  ```bash
  venv\Scripts\activate
  ```

- **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 3. 安装依赖

在激活的虚拟环境中，安装项目所需的依赖包：

```bash
pip install -r requirements.txt
```

### 4. 配置文件

项目支持通过 `config.ini` 文件进行配置。你可以在项目根目录下创建一个 `config.ini` 文件，或者在运行时提供配置文件路径。以下是一个示例配置文件：

```ini
[DEFAULT]
input_directory = ./data/input
output_file = ./data/output/merged_data.csv
key_columns = id name
skip_errors = True
overwrite_output = False
custom_rules = 
    column=price operation=convert_type type=float
    column=age operation=dropna
```

你可以根据需要修改这些配置项，或者在运行时通过命令行参数覆盖它们。

## 使用方法

### 命令行模式

#### 1. 运行主程序

在命令行中运行以下命令启动命令行模式：

```bash
python src/main.py
```

#### 2. 输入参数

程序会提示你输入以下信息：

- **输入文件夹路径**：包含待处理的CSV或Excel文件的文件夹路径。
- **输出文件路径**：处理后的数据将保存到此文件中（支持 `.csv`、`.xlsx`、`.xls` 格式）。
- **关键列**：用于合并文件的列名（多个列名用空格分隔）。如果不合并文件，可以留空。
- **是否跳过错误文件**：如果某些文件在处理过程中出现错误，是否继续处理其他文件。
- **是否覆盖现有文件**：如果输出文件已存在，是否覆盖它。

#### 3. 处理结果

处理完成后，程序会自动生成一份报告，包含统计图表和文本报告，帮助你分析处理后的数据。

### 图形用户界面 (GUI) 模式

#### 1. 运行GUI

在命令行中运行以下命令启动图形用户界面：

```bash
python src/gui.py
```

#### 2. 使用GUI

GUI界面提供了直观的操作方式，用户可以通过以下步骤完成批量处理：

- **选择输入文件夹**：点击“选择文件夹”按钮，选择包含待处理文件的文件夹。
- **选择输出文件**：点击“选择文件”按钮，选择保存处理后数据的文件路径。
- **设置关键列**：在“关键列”输入框中输入用于合并文件的列名（多个列名用空格分隔）。如果不合并文件，可以留空。
- **跳过错误文件**：勾选“跳过错误文件”选项，如果某些文件在处理过程中出现错误，程序将继续处理其他文件。
- **覆盖现有文件**：勾选“覆盖现有文件”选项，如果输出文件已存在，程序将覆盖它。
- **开始处理**：点击“开始处理”按钮，程序将开始批量处理文件，并在处理完成后显示成功消息。

### 自定义规则

你可以在 `config.ini` 文件中定义自定义规则，用于对数据进行特定的清洗和转换。每个规则由三部分组成：

- **column**：要操作的列名。
- **operation**：要执行的操作（如 `dropna`、`fillna`、`convert_type` 等）。
- **value/type**：根据操作的不同，可能需要提供额外的参数（如填充值或目标数据类型）。

例如：

```ini
custom_rules = 
    column=price operation=convert_type type=float
    column=age operation=dropna
    column=sales operation=fillna value=0
```

## 示例

假设你有一个包含多个CSV文件的文件夹 `./data/input`，并且希望将这些文件按 `id` 和 `name` 列合并为一个CSV文件 `./data/output/merged_data.csv`。你可以按照以下步骤操作：

### 使用命令行模式

```bash
python src/main.py
```

根据提示输入以下信息：

- 输入文件夹路径：`./data/input`
- 输出文件路径：`./data/output/merged_data.csv`
- 关键列：`id name`
- 是否跳过错误文件：`y`
- 是否覆盖现有文件：`n`

### 使用GUI模式

1. 启动GUI：
   ```bash
   python src/gui.py
   ```

2. 在GUI界面上：
   - 选择输入文件夹：`./data/input`
   - 选择输出文件：`./data/output/merged_data.csv`
   - 设置关键列：`id name`
   - 勾选“跳过错误文件”
   - 不勾选“覆盖现有文件”
   - 点击“开始处理”

## 测试

为了确保代码的正确性，项目包含了一组单元测试。你可以使用 `unittest` 或 `pytest` 来运行测试。

### 使用 `unittest` 运行测试

```bash
python -m unittest discover tests/
```

### 使用 `pytest` 运行测试

首先，确保已经安装了 `pytest`：

```bash
pip install pytest
```

然后运行以下命令：

```bash
pytest
```

## 许可证

本项目采用 GNU General Public License (GPL) 许可证。请参阅 `LICENSE` 文件以获取详细信息。
