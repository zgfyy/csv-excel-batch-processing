import tkinter as tk
from tkinter import filedialog, messagebox
from src.data_processor import process_files
from src.utils import backup_existing_file, generate_report

def create_gui():
    """创建图形用户界面"""
    root = tk.Tk()
    root.title("CSV/Excel 批量处理工具")

    def select_input_directory():
        dir_name = filedialog.askdirectory()
        if dir_name:
            input_dir_var.set(dir_name)

    def select_output_file():
        file_name = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx *.xls")])
        if file_name:
            output_file_var.set(file_name)

    def start_processing():
        input_directory = input_dir_var.get()
        output_file = output_file_var.get()
        key_columns = key_columns_var.get().split() if key_columns_var.get() else None
        skip_errors = skip_errors_var.get()
        overwrite_output = overwrite_output_var.get()

        if not os.path.isdir(input_directory):
            messagebox.showerror("错误", "输入的路径不是有效的文件夹。")
            return

        if not Path(output_file).suffix in ['.csv', '.xlsx', '.xls']:
            messagebox.showerror("错误", "输出文件格式不正确，请输入有效的文件格式 (.csv, .xlsx, .xls)。")
            return

        try:
            process_files(input_directory, output_file, key_columns, skip_errors, overwrite_output)
            backup_existing_file(output_file)
            generate_report(output_file)
            messagebox.showinfo("成功", "处理完成！")
        except Exception as e:
            messagebox.showerror("错误", f"处理过程中出现错误: {e}")

    # 创建变量
    input_dir_var = tk.StringVar()
    output_file_var = tk.StringVar()
    key_columns_var = tk.StringVar()
    skip_errors_var = tk.BooleanVar()
    overwrite_output_var = tk.BooleanVar()

    # 创建标签和输入框
    tk.Label(root, text="输入文件夹:").grid(row=0, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=input_dir_var, width=50).grid(row=0, column=1, padx=10, pady=5)
    tk.Button(root, text="选择文件夹", command=select_input_directory).grid(row=0, column=2, padx=10, pady=5)

    tk.Label(root, text="输出文件:").grid(row=1, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=output_file_var, width=50).grid(row=1, column=1, padx=10, pady=5)
    tk.Button(root, text="选择文件", command=select_output_file).grid(row=1, column=2, padx=10, pady=5)

    tk.Label(root, text="关键列 (空格分隔):").grid(row=2, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=key_columns_var, width=50).grid(row=2, column=1, padx=10, pady=5)

    tk.Checkbutton(root, text="跳过错误文件", variable=skip_errors_var).grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)
    tk.Checkbutton(root, text="覆盖现有文件", variable=overwrite_output_var).grid(row=4, column=1, sticky=tk.W, padx=10, pady=5)

    tk.Button(root, text="开始处理", command=start_processing).grid(row=5, column=1, pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()