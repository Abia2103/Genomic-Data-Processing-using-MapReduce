import pandas as pd
import matplotlib.pyplot as plt

f = "base_comp_counts.txt"   # your downloaded reducer output

# Load space-separated values
df = pd.read_csv(f, sep=r"\s+", header=None,
                 names=["pos", "A", "T", "G", "C"])

# Normalize to percentages
df["total"] = df[["A", "T", "G", "C"]].sum(axis=1)
for base in ["A", "T", "G", "C"]:
    df[base + "_pct"] = df[base] / df["total"] * 100

# PLOT
plt.figure(figsize=(14,6))
for base, color in zip(["A","T","G","C"], ["blue","red","green","orange"]):
    plt.plot(df["pos"], df[base + "_pct"], label=base, linewidth=1.3)

plt.title("Per-Base Nucleotide Composition")
plt.xlabel("Read Position")
plt.ylabel("Percentage")
plt.legend()
plt.tight_layout()
plt.show()


# ---- BIAS ANALYSIS ----

def flag(msg):
    print("⚠", msg)

print("\n### BASE COMPOSITION QC ###\n")

# 1. Priming Bias at first 15 bases
first = df.loc[df.pos < 15, ["A_pct","T_pct","G_pct","C_pct"]]
spread = (first.max(axis=1) - first.min(axis=1)).mean()

if spread > 20:
    flag("Strong priming bias detected in first ~15 bases")
else:
    print("✓ No significant priming bias")

# 2. End-of-read degradation (check last 10 bases)
last = df.tail(10)[["A_pct","T_pct","G_pct","C_pct"]]
end_spread = (last.max(axis=1) - last.min(axis=1)).mean()

if end_spread > 18:
    flag("End-of-read degradation detected")
else:
    print("✓ No major end-of-read bias")

# 3. GC imbalance across read
avg_GC = (df["G"] + df["C"]).sum() / df["total"].sum() * 100

if avg_GC < 35 or avg_GC > 65:
    flag(f"GC/AT imbalance detected — GC = {avg_GC:.1f}%")
else:
    print(f"✓ GC balance normal (GC = {avg_GC:.1f}%)")