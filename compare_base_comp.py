import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def analyze_dataset(file_path, label="Dataset"):
    print(f"\n================ {label} REPORT ================\n")

    df = pd.read_csv(file_path, sep=r"\s+", header=None,
                     names=["pos", "A", "T", "G", "C"])

    df["total"] = df[["A", "T", "G", "C"]].sum(axis=1)

    # Percentages
    for base in ["A", "T", "G", "C"]:
        df[base + "_pct"] = df[base] / df["total"] * 100


    plt.figure(figsize=(14,6))
    colors = ["blue","red","green","orange"]
    for base, color in zip(["A","T","G","C"], colors):
        plt.plot(df["pos"], df[base + "_pct"], label=base, linewidth=1.3, color=color)

    plt.title(f"{label}: Per-Base Nucleotide Composition")
    plt.xlabel("Read Position")
    plt.ylabel("Percentage")
    plt.legend()
    plt.tight_layout()
    plt.show()


    def flag(msg): print("⚠", msg)

    print("\n### BASE COMPOSITION QC ###\n")

    # 1. Priming bias (first 15 bases)
    first = df.loc[df.pos < 15, ["A_pct","T_pct","G_pct","C_pct"]]
    spread_first = (first.max(axis=1) - first.min(axis=1)).mean()

    if spread_first > 20:
        flag("Strong priming bias detected in first ~15 bases")
    else:
        print("✓ No significant priming bias")

    # 2. End-of-read degradation (last 10 bases)
    last = df.tail(10)[["A_pct","T_pct","G_pct","C_pct"]]
    spread_last = (last.max(axis=1) - last.min(axis=1)).mean()

    if spread_last > 18:
        flag("End-of-read degradation detected")
    else:
        print("✓ No major end-of-read bias")

    # 3. GC imbalance
    avg_GC = (df["G"] + df["C"]).sum() / df["total"].sum() * 100

    if avg_GC < 35 or avg_GC > 65:
        flag(f"GC/AT imbalance detected — GC = {avg_GC:.1f}%")
    else:
        print(f"✓ GC balance normal (GC = {avg_GC:.1f}%)")

    # ---------- SINGLE OVERALL BIAS PERCENT ----------
    expected = 25
    avg_abs_dev = (
        df[["A_pct","T_pct","G_pct","C_pct"]] - expected
    ).abs().mean().mean()

    print(f"\n {label} Overall Base Bias = {avg_abs_dev:.2f}%\n")

    return avg_abs_dev, avg_GC



file2 = "/Users/abiamaimun/Desktop/uni/BigDataAnalytics/base_comp_bias/base_comp_counts.txt"
file1 = "/Users/abiamaimun/Desktop/uni/BigDataAnalytics/base_comp_bias/base_comp_gc2.txt"

bias1, gc1 = analyze_dataset(file1, "Dataset 1")
bias2, gc2 = analyze_dataset(file2, "Dataset 2")

print("\n================ FINAL COMPARISON ================\n")
print(f"Dataset 1 Bias: {bias1:.2f}%")
print(f"Dataset 2 Bias: {bias2:.2f}%")

if bias2 > bias1:
    print("\n Dataset 2 is more biased overall.")
elif bias1 > bias2:
    print("\n Dataset 1 is more biased overall.")
else:
    print("\n Both datasets have equal bias.")