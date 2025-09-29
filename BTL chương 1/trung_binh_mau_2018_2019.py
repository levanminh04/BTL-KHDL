import pandas as pd

file_path_all = "presemission-postissue.csv"
df_all = pd.read_csv(file_path_all)

col = "Payments-Total-Amount-Montant-total-de-paiements"
year_col = "Fiscal-Year-Année-Fiscale"
data_1819 = df_all[df_all[year_col] == "2018-2019"][col].dropna().astype(float)

mean_1819 = data_1819.mean() / 1e6 

print(f"Trung bình chi tiêu năm 2018–2019: {mean_1819:.2f} triệu CAD")
