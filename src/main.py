from src.batch_processor import BatchProcessor
from src.settings import settings
import sys

def generate_config_template():
    template_path = Path("config/config_template.ini")
    with open(template_path, 'w') as f:
        f.write("[DEFAULT]\n")
        f.write("input_directory = \n")
        f.write("output_file = \n")
        f.write("key_columns = \n")
        f.write("skip_errors = \n")
        f.write("overwrite_output = \n\n")
        f.write("[CustomRules]\n")
        f.write("# 自定义规则示例\n")
        f.write("# column=<列名> operation=<操作> [type/value=<参数>]\n")
    print(f"Config template generated at {template_path}")

def main():
    print("CSV/Excel 批量处理工具 - 命令行模式")
    
    # 创建批量处理器并运行
    processor = BatchProcessor(settings)
    processor.run()

if __name__ == "__main__":
    # 检查是否需要生成配置文件模板
    if len(sys.argv) > 1 and sys.argv[1] == "--generate-config":
        generate_config_template()
    else:
        main()