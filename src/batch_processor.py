import pandas as pd
import os
from pathlib import Path
from src.settings import settings

class BatchProcessor:
    def __init__(self, settings):
        self.settings = settings

    def run(self):
        """执行批量处理"""
        print("Starting batch processing...")

        # 读取输入文件夹中的所有 CSV 和 Excel 文件
        input_dir = Path(self.settings.input_directory)
        files = [f for f in input_dir.iterdir() if f.is_file() and f.suffix in ['.csv', '.xlsx', '.xls']]
        
        if not files:
            print("No files found in the input directory.")
            return

        # 初始化空的 DataFrame 用于合并
        merged_df = pd.DataFrame()

        for file in files:
            try:
                # 读取文件
                if file.suffix == '.csv':
                    df = pd.read_csv(file)
                elif file.suffix in ['.xlsx', '.xls']:
                    df = pd.read_excel(file)
                
                # 应用自定义规则
                for rule in self.settings.custom_rules:
                    if rule['operation'] == 'convert_type':
                        df[rule['column']] = df[rule['column']].astype(rule['params']['type'])
                    elif rule['operation'] == 'dropna':
                        df.dropna(subset=[rule['column']], inplace=True)
                    elif rule['operation'] == 'fillna':
                        df[rule['column']].fillna(rule['params']['value'], inplace=True)
                
                # 合并文件
                if self.settings.key_columns:
                    merged_df = pd.concat([merged_df, df], ignore_index=True, sort=False)
                else:
                    merged_df = pd.concat([merged_df, df], ignore_index=True, sort=False)
            
            except Exception as e:
                if self.settings.skip_errors:
                    print(f"Error processing file {file}: {e}. Skipping...")
                    continue
                else:
                    raise e
        
        # 保存结果
        output_file = Path(self.settings.output_file)
        if output_file.exists() and not self.settings.overwrite_output:
            print(f"Output file {output_file} already exists. Skipping save.")
        else:
            if output_file.suffix == '.csv':
                merged_df.to_csv(output_file, index=False)
            elif output_file.suffix in ['.xlsx', '.xls']:
                merged_df.to_excel(output_file, index=False)
            print(f"Processed data saved to {output_file}")

        print("Batch processing completed.")