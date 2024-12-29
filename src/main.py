import logging
from src.config import get_user_input_with_config
from src.data_processor import process_files
from src.utils import backup_existing_file, generate_report

def main():
    print("欢迎使用CSV/Excel批量处理工具")
    print("请按照提示输入相关信息")

    # 获取用户输入
    input_directory, output_file, key_columns, skip_errors, overwrite_output = get_user_input_with_config()

    # 执行批量处理
    try:
        process_files(input_directory, output_file, key_columns, skip_errors, overwrite_output)
        backup_existing_file(output_file)
        generate_report(output_file)
        print("处理完成！")
    except Exception as e:
        logging.error(f"处理过程中出现错误: {e}")

if __name__ == "__main__":
    main()