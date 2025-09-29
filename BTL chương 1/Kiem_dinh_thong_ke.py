import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from matplotlib.ticker import FuncFormatter

file_path = "pspc_2020_2021_by_department_enriched.csv"
df = pd.read_csv(file_path)
col = "Payments-Total-Amount-Montant-total-de-paiements"
data = df[col].dropna().astype(float)
df_all = pd.read_csv("presemission-postissue.csv")
col_all = "Payments-Total-Amount-Montant-total-de-paiements"
mu0 = df_all[df_all["Fiscal-Year-Année-Fiscale"] == "2018-2019"][col_all].mean()
alpha = 0.05
sample_mean = np.mean(data)
sample_std = np.std(data, ddof=1)
n = len(data)
mu0_million = mu0 / 1e6
mean_million = sample_mean / 1e6
t_stat, p_value_two_tailed = stats.ttest_1samp(data, mu0)
if sample_mean > mu0:
    p_value = p_value_two_tailed / 2
else:
    p_value = 1 - (p_value_two_tailed / 2)
print(f"Cỡ mẫu (n): {n}")
print(f"Giá trị trung bình mẫu (x̄, 2020–2021): {mean_million:.2f} (triệu CAD)")
print(f"Độ lệch chuẩn mẫu (s): {sample_std/1e6:.2f} (triệu CAD)")
print(f"Giá trị giả thuyết μ0 (2018–2019): {mu0_million:.2f} (triệu CAD)")
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value (1 phía): {p_value:.4f}")

if p_value < alpha:
    print(f"Kết luận: Vì p = {p_value:.4f} < α = {alpha}, bác bỏ giả thuyết H₀.")
    print("Có đủ bằng chứng thống kê để khẳng định: "
          "Chi tiêu trung bình năm 2020–2021 cao hơn đáng kể so với năm 2018–2019 (trước COVID).")
else:
    print(f"Kết luận: Vì p = {p_value:.4f} ≥ α = {alpha}, chưa đủ bằng chứng để bác bỏ H₀.")
    print("Không thể khẳng định chi tiêu trung bình năm 2020–2021 cao hơn năm 2018–2019.")

plt.figure(figsize=(12,5))
sns.histplot(data/1e6, bins=30, kde=True, color="skyblue")
y_pos = plt.ylim()[1] * 0.8
plt.axvline(mu0_million, color="red", linestyle="--", linewidth=2,
            label=f"μ0 = {mu0_million:.1f} triệu (2018–2019)")
plt.text(mu0_million + 200, y_pos, f"{mu0_million:.1f}",
         color="red", ha="left", va="bottom", fontsize=10, rotation=90)

plt.axvline(mean_million, color="green", linestyle="-", linewidth=2,
            label=f"Mean 2020–2021 = {mean_million:.1f}")
plt.text(mean_million - 200, y_pos, f"{mean_million:.1f}",
         color="green", ha="right", va="bottom", fontsize=10, rotation=90)

main_ticks = np.arange(0, 50001, 10000)
plt.xticks(main_ticks)
plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.title("Kiểm định chi tiêu trung bình 2020–2021 so với 2018–2019", fontsize=14)
plt.xlabel("Giá trị thanh toán (triệu CAD)")
plt.ylabel("Tần suất")
plt.xlim(0, 50000)
plt.legend()
plt.show()

