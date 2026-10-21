import pandas as pd
import matplotlib

df = pd.read_csv("Superstore.csv",encoding="latin-1")
print("\n",df.shape)
print("\n",df.describe())
print("\n",df.info())
print("\n",df.isna().sum())

for col,val in df.isna().sum().items():
    if val == 0:
        continue
    elif val > (len(df) * 0.5):
        df = df.drop(columns=col)
    elif pd.api.types.is_numeric_dtype(df[col]):
        if abs(df[col].skew())>1:
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(df[col].mean())
    else:
        df[col] = df[col].fillna("Missing")

df = df.drop_duplicates()

total = df.groupby(["Region","Category"])["Profit"].sum()
print("\n",total.idxmax())
print("\n",total.idxmin())

total1 = df.groupby("Customer Name")["Sales"].sum()
print("\n",total1.sort_values(ascending=False).head(10))

df["Order Date"] = pd.to_datetime(df["Order Date"],format="%d-%m-%Y")
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month

monthly = df.groupby(["Year","Month"])["Sales"].sum()
print("\n",monthly.idxmax(), monthly.max())  
print(monthly.idxmin(), monthly.min()) 

correlation = df["Discount"].corr(df["Profit"])
print("\n",correlation)

sub_df = df.groupby("Sub-Category").agg({"Profit":"sum","Discount":"mean"})

unprofitable = sub_df[sub_df["Profit"]<0]
print("\nLoss-Making Sub-Categories:\n", unprofitable)

avg_disc_unprofitable = sub_df[sub_df["Profit"] < 0]["Discount"].mean()
avg_disc_profitable = sub_df[sub_df["Profit"] >= 0]["Discount"].mean()

print(f"\nAvg Discount (Loss-Making): {avg_disc_unprofitable:.2%}")
print(f"Avg Discount (Profitable):  {avg_disc_profitable:.2%}")