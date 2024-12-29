import os
import configparser
from pathlib import Path

def load_config(config_file='config.ini'):
    """加载配置文件"""
    config = configparser.ConfigParser()
    if os.path.exists(config_file):
        config.read(config_file)
        return config
    else:
        print(f"配置文件 {config_file} 不存在，将使用默认设置。")
        return None

def get_user_input_with_config():
    """获取用户输入的路径和其他选项，优先使用配置文件中的设置"""
    config = load_config()

    # 从配置文件中读取默认值
    default_input_directory = config.get('DEFAULT', 'input_directory', fallback=None)
    default_output_file = config.get('DEFAULT', 'output_file', fallback=None)
    default_key_columns = config.get('DEFAULT', 'key_columns', fallback='').split() or None
    default_skip_errors = config.getboolean('DEFAULT', 'skip_errors', fallback=False)
    default_overwrite_output = config.getboolean('DEFAULT', 'overwrite_output', fallback=False)

    # 获取用户输入，允许用户覆盖配置文件中的默认值
    input_directory = input(f"请输入包含待处理CSV/Excel文件的文件夹路径 (默认: {default_input_directory}): ").strip() or default_input_directory
    output_file = input(f"请输入输出文件的路径 (支持.csv, .xlsx, .xls) (默认: {default_output_file}): ").strip() or default_output_file

    # 验证输入路径
    while not os.path.isdir(input_directory):
        print("输入的路径不是有效的文件夹，请重新输入。")
        input_directory = input("请输入包含待处理CSV/Excel文件的文件夹路径: ").strip()

    while not Path(output_file).suffix in ['.csv', '.xlsx', '.xls']:
        print("输出文件格式不正确，请输入有效的文件格式 (.csv, .xlsx, .xls)。")
        output_file = input("请输入输出文件的路径 (支持.csv, .xlsx, .xls): ").strip()

    key_columns_input = input(f"请输入用于合并的关键列名 (如果不需要合并，请留空) (默认: {' '.join(default_key_columns) if default_key_columns else ''}): ").strip()
    key_columns = key_columns_input.split() if key_columns_input else default_key_columns

    skip_errors_input = input(f"是否跳过处理过程中出现错误的文件? (y/n, 默认: {'y' if default_skip_errors else 'n'}): ").strip().lower() or ('y' if default_skip_errors else 'n')
    skip_errors = skip_errors_input == 'y'

    overwrite_output_input = input(f"如果输出文件已存在，是否覆盖? (y/n, 默认: {'y' if default_overwrite_output else 'n'}): ").strip().lower() or ('y' if default_overwrite_output else 'n')
    overwrite_output = overwrite_output_input == 'y'

    return input_directory, output_file, key_columns, skip_errors, overwrite_output