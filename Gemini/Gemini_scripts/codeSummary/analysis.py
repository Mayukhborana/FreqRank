#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_time_vs_sample.py
读取 defense45_summary.csv 并绘制 total_time_sec 随 processed 变化的曲线（接近线性增长）。
"""

import pandas as pd
import matplotlib.pyplot as plt
import pathlib


def main() -> None:
    # ==== 1. 路径设置 ====
    csv_filename = "../draw/defense45_code_summary_g.csv"  # CSV 文件名（同目录）
    output_png   = "defense45_summary_total.png"  # 输出图像文件名

    # ==== 2. 读取数据 ====
    data_path = pathlib.Path(__file__).with_name(csv_filename)
    df = pd.read_csv(data_path)

    # ==== 3. 绘图 ====
    plt.figure(figsize=(9, 5))
    plt.plot(
        df["processed"],
        df["total_time_sec"],
        marker="o",
        linewidth=1.8,
        label="total_time_sec",
    )

    plt.xlabel("Samples processed (每 10 个为一步)")
    plt.ylabel("Total time (sec)")
    plt.title("Total processing time vs. number of samples")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.legend()

    # ==== 4. 保存和提示 ====
    save_path = pathlib.Path(__file__).with_name(output_png)
    plt.savefig(save_path, dpi=300)
    print(f"图像已保存到: {save_path.resolve()}")


if __name__ == "__main__":
    main()
