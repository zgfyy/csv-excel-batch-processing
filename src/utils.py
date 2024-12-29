import os
import shutil
import datetime
import matplotlib.pyplot as plt
from src.config import get_custom_rules_from_config

def clean_and_transform_with_rules(df, custom_rules=None):
    """执行数据清洗和转换操作，应用自定义规则"""
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    if 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce')

    if custom_rules:
        for rule in custom_rules:
            if 'column' in rule and 'operation' in rule:
                column = rule['column']
                operation = rule['operation']

                if operation == 'dropna':
                    df.dropna(subset=[column], inplace=True)
                elif operation == 'fillna':
                    value = rule.get('value', 0)
                    df[column].fillna(value, inplace=True)
                elif operation == 'convert_type':
                    target_type = rule.get('type', 'float')
                    df[column] = pd.to_numeric(df[column], errors='coerce') if target_type == 'float' else df[column].astype(target_type)

    return df

def merge_dataframes(dfs, key_columns=None):
    """合并多个DataFrame，如果提供了key_columns，则按这些列进行合并"""
    if not dfs:
        return None

    if key_columns is None:
        # 如果没有指定关键列，则直接连接所有数据框
        merged_df = pd.concat(dfs, ignore_index=True)
    else:
        # 按关键列合并数据框
        merged_df = dfs[0]
        for df in dfs[1:]:
            merged_df = pd.merge(merged_df, df, on=key_columns, how='outer')

    return merged_df

def backup_existing_file(output_file):
    """自动备份现有的输出文件"""
    if Path(output_file).exists():
        backup_file = f"{output_file}.backup.{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy(output_file, backup_file)
        logging.info(f"备份了现有文件到 {backup_file}")

def generate_report(merged_df, output_file):
    """生成简单的统计图表或报告"""
    # 例如，生成每列的数据分布图
    for column in merged_df.columns:
        if pd.api.types.is_numeric_dtype(merged_df[column]):
            plt.figure(figsize=(10, 6))
            plt.hist(merged_df[column].dropna(), bins=30, alpha=0.7, color='blue')
            plt.title(f"Data Distribution of {column}")
            plt.xlabel(column)
            plt.ylabel("Frequency")
            plt.savefig(f"{output_file}_{column}_histogram.png")
            plt.close()

    # 生成一份简单的文本报告
    with open(f"{output_file}_report.txt", "w") as f:
        f.write("Data Processing Report\n")
        f.write("======================\n\n")
        f.write(f"Total number of rows: {len(merged_df)}\n")
        f.write(f"Number of columns: {len(merged_df.columns)}\n\n")
        f.write("Column Statistics:\n")
        for column in merged_df.columns:
            f.write(f"- {column}: {merged_df[column].describe()}\n")

    logging.info("生成了统计图表和报告。")