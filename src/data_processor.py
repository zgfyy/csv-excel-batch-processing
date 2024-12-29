import os
import pandas as pd
from pathlib import Path
import logging
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.utils import clean_and_transform_with_rules, merge_dataframes, backup_existing_file, generate_report

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path):
    """根据文件扩展名加载CSV或Excel文件"""
    if file_path.suffix == '.csv':
        return pd.read_csv(file_path)
    elif file_path.suffix in ['.xlsx', '.xls']:
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")

def process_file(file_path, key_columns=None, skip_errors=False, custom_rules=None):
    """处理单个文件"""
    try:
        logging.info(f"正在处理 {file_path}...")
        df = load_data(file_path)
        cleaned_df = clean_and_transform_with_rules(df, custom_rules)
        return cleaned_df
    except Exception as e:
        logging.error(f"处理文件 {file_path} 时出错: {e}")
        if not skip_errors:
            raise
        return None

def process_files_multithreaded(input_dir, output_file, key_columns=None, skip_errors=False, overwrite_output=False, max_workers=4, custom_rules=None):
    """使用多线程批量处理输入目录中的所有CSV/Excel文件，并将结果保存到输出文件"""
    input_dir = Path(input_dir)
    files = [f for f in input_dir.iterdir() if f.suffix in ['.csv', '.xlsx', '.xls']]
    if not files:
        logging.info("没有找到有效的CSV或Excel文件。")
        return

    all_dfs = []
    error_files = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_file, file_path, key_columns, skip_errors, custom_rules): file_path for file_path in files}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing files"):
            file_path = futures[future]
            try:
                df = future.result()
                if df is not None:
                    all_dfs.append(df)
            except Exception as e:
                logging.error(f"处理文件 {file_path} 时出错: {e}")
                error_files.append(file_path)

    if error_files:
        logging.warning(f"以下文件处理失败: {', '.join(str(f) for f in error_files)}")

    if not all_dfs:
        logging.info("没有有效文件可以处理。")
        return

    merged_df = merge_dataframes(all_dfs, key_columns)

    output_format = Path(output_file).suffix
    if output_format not in ['.csv', '.xlsx', '.xls']:
        logging.error(f"不支持的输出文件格式: {output_format}")
        return

    if Path(output_file).exists() and not overwrite_output:
        logging.error(f"输出文件已存在: {output_file}。请使用 --overwrite 选项覆盖现有文件。")
        return

    try:
        if output_format == '.csv':
            merged_df.to_csv(output_file, index=False)
        elif output_format in ['.xlsx', '.xls']:
            merged_df.to_excel(output_file, index=False)
        logging.info(f"合并后的数据已保存到 {output_file}")
    except Exception as e:
        logging.error(f"保存输出文件时出错: {e}")