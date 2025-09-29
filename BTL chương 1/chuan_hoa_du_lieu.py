# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("pspc_2020_2021_by_department_enriched.csv")

cols_focus = [
    "Payments-Total-Volume-Volume-total-de-paiements",
    "Payments-Total-Amount-Montant-total-de-paiements"
]

df_focus = df[cols_focus].copy()

df_log = df_focus.apply(np.log1p)

def zscore_custom(series, ddof=0):
    return (series - series.mean()) / series.std(ddof=ddof)

z_scores = {}
for col in cols_focus:
    z_scores[col] = {
        "ddof0": zscore_custom(df_log[col], ddof=0),
        "ddof1": zscore_custom(df_log[col], ddof=1)
    }

dept_col = df.columns[0] 
print("Tên cột bộ/ngành trong file:", dept_col)

df_out = df[[dept_col] + cols_focus].copy()
df_out_log = df_log.add_suffix("_log1p")

for col in cols_focus:
    df_out[f"{col}_z_ddof0"] = z_scores[col]["ddof0"]
    df_out[f"{col}_z_ddof1"] = z_scores[col]["ddof1"]

    df_out[f"{col}_outlier_ddof0"] = np.abs(df_out[f"{col}_z_ddof0"]) > 3
    df_out[f"{col}_outlier_ddof1"] = np.abs(df_out[f"{col}_z_ddof1"]) > 3


print("Tổng số dòng:", len(df_out))
for col in cols_focus:
    print(f"\n--- {col} ---")
    print("Outlier (ddof=0):", df_out[f"{col}_outlier_ddof0"].sum())
    print("Outlier (ddof=1):", df_out[f"{col}_outlier_ddof1"].sum())

    
    for mode in ["ddof0", "ddof1"]:
        mask = df_out[f"{col}_outlier_{mode}"]
        if mask.any():
            print(f" {col} - Outlier ({mode}):")
            print(df_out.loc[mask, [dept_col, col, f"{col}_z_{mode}"]])


for col in cols_focus:
    plt.figure(figsize=(8, 5))
    df_focus[[col]].boxplot()
    plt.title(f"{col} - Dữ liệu Gốc")
    plt.show()

    plt.figure(figsize=(8, 5))
    df_log[[col]].boxplot()
    plt.title(f"{col} - Sau log1p")
    plt.show()

    plt.figure(figsize=(8, 5))
    df_out[[f"{col}_z_ddof0"]].boxplot()
    plt.title(f"{col} - Z-score (ddof=0)")
    plt.show()

    plt.figure(figsize=(8, 5))
    df_out[[f"{col}_z_ddof1"]].boxplot()
    plt.title(f"{col} - Z-score (ddof=1)")
    plt.show()

df_final = pd.concat([df_out, df_out_log], axis=1)
df_final.to_csv("pspc_zscore_ddof_compare.csv", index=False)
print("Xuất file pspc_zscore_ddof_compare.csv thành công!")
