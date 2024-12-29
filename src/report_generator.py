import matplotlib.pyplot as plt

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

    print("生成了统计图表和报告。")