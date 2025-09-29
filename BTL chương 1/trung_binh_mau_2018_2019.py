import pandas as pd

# Đọc dữ liệu gốc nhiều năm
file_path_all = "presemission-postissue.csv"
df_all = pd.read_csv(file_path_all)

# Chọn cột thanh toán
col = "Payments-Total-Amount-Montant-total-de-paiements"
year_col = "Fiscal-Year-Année-Fiscale"

# Lọc riêng năm 2018–2019
data_1819 = df_all[df_all[year_col] == "2018-2019"][col].dropna().astype(float)

# Tính trung bình
mean_1819 = data_1819.mean() / 1e6  # đổi sang triệu CAD

print("=============================================")
print(f"Trung bình chi tiêu năm 2018–2019: {mean_1819:.2f} triệu CAD")
print("=============================================")