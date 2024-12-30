import tkinter as tk
from tkinter import filedialog, messagebox
from src.settings import settings
from src.batch_processor import BatchProcessor

class SettingsGUI:
    def __init__(self, root):
        self.root = root
        
        # 创建输入文件夹选择按钮
        self.input_dir_label = tk.Label(root, text="输入文件夹:")
        self.input_dir_label.pack()
        self.input_dir_var = tk.StringVar(value=settings.input_directory)
        self.input_dir_entry = tk.Entry(root, textvariable=self.input_dir_var, width=50)
        self.input_dir_entry.pack()
        self.input_dir_button = tk.Button(root, text="选择文件夹", command=self.select_input_directory)
        self.input_dir_button.pack()
        
        # 创建输出文件选择按钮
        self.output_file_label = tk.Label(root, text="输出文件:")
        self.output_file_label.pack()
        self.output_file_var = tk.StringVar(value=settings.output_file)
        self.output_file_entry = tk.Entry(root, textvariable=self.output_file_var, width=50)
        self.output_file_entry.pack()
        self.output_file_button = tk.Button(root, text="选择文件", command=self.select_output_file)
        self.output_file_button.pack()
        
        # 创建关键列输入框
        self.key_columns_label = tk.Label(root, text="关键列 (多个列名用空格分隔):")
        self.key_columns_label.pack()
        self.key_columns_var = tk.StringVar(value=" ".join(settings.key_columns))
        self.key_columns_entry = tk.Entry(root, textvariable=self.key_columns_var, width=50)
        self.key_columns_entry.pack()
        
        # 创建跳过错误复选框
        self.skip_errors_var = tk.BooleanVar(value=settings.skip_errors)
        self.skip_errors_check = tk.Checkbutton(root, text="跳过错误文件", variable=self.skip_errors_var)
        self.skip_errors_check.pack()
        
        # 创建覆盖输出复选框
        self.overwrite_output_var = tk.BooleanVar(value=settings.overwrite_output)
        self.overwrite_output_check = tk.Checkbutton(root, text="覆盖现有文件", variable=self.overwrite_output_var)
        self.overwrite_output_check.pack()
        
        # 创建开始处理按钮
        self.start_button = tk.Button(root, text="开始处理", command=self.start_processing)
        self.start_button.pack()

    def select_input_directory(self):
        """选择输入文件夹"""
        directory = filedialog.askdirectory()
        if directory:
            self.input_dir_var.set(directory)
            settings.set_setting('DEFAULT', 'input_directory', directory)

    def select_output_file(self):
        """选择输出文件"""
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx *.xls")])
        if file:
            self.output_file_var.set(file)
            settings.set_setting('DEFAULT', 'output_file', file)

    def start_processing(self):
        """开始处理"""
        # 更新设置
        settings.update_settings({
            'input_directory': self.input_dir_var.get(),
            'output_file': self.output_file_var.get(),
            'key_columns': self.key_columns_var.get().split(),
            'skip_errors': self.skip_errors_var.get(),
            'overwrite_output': self.overwrite_output_var.get()
        })
        
        # 创建批量处理器并运行
        processor = BatchProcessor(settings)
        processor.run()
        
        messagebox.showinfo("提示", "处理完成！")

def main():
    # 创建主窗口
    root = tk.Tk()
    root.title("CSV/Excel 批量处理工具 - 设置")
    
    # 创建设置界面
    app = SettingsGUI(root)
    
    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()