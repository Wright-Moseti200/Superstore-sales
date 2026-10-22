import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

df = pd.read_csv("Superstore.csv", encoding="latin-1")
print("\n", df.shape)
print("\n", df.describe())
print("\n", df.info())
print("\n", df.isna().sum())

for col, val in df.isna().sum().items():
    if val == 0:
        continue
    elif val > (len(df) * 0.5):
        df = df.drop(columns=col)
    elif pd.api.types.is_numeric_dtype(df[col]):
        if abs(df[col].skew()) > 1:
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(df[col].mean())
    else:
        df[col] = df[col].fillna("Missing")

df = df.drop_duplicates()

# Q1: profit by region and category
total = df.groupby(["Region", "Category"])["Profit"].sum()
print("\n", total.idxmax())
print("\n", total.idxmin())

total.unstack().plot(kind="bar", title="Profit by Region and Category")
plt.ylabel("Total Profit")
plt.tight_layout()
plt.show()

# Q2: top 10 customers by sales
total1 = df.groupby("Customer Name")["Sales"].sum()
top10 = total1.sort_values(ascending=False).head(10)
print("\n", top10)

top10.sort_values().plot(kind="barh", title="Top 10 Customers by Sales")
plt.xlabel("Total Sales")
plt.tight_layout()
plt.show()

# Q3: sales over time
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y")
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month

monthly = df.groupby(["Year", "Month"])["Sales"].sum()
print("\n", monthly.idxmax(), monthly.max())
print(monthly.idxmin(), monthly.min())

df.groupby("Year")["Sales"].sum().plot(kind="bar", title="Total Sales by Year")
plt.ylabel("Total Sales")
plt.show()

df.groupby("Month")["Sales"].sum().plot(kind="line", marker="o", title="Total Sales by Month (all years)")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.show()

# Q4: discount vs profit
correlation = df["Discount"].corr(df["Profit"])
print("\n", correlation)

df.plot(kind="scatter", x="Discount", y="Profit", alpha=0.3, title=f"Discount vs Profit (corr={correlation:.2f})")
plt.xlabel("Discount")
plt.ylabel("Profit")
plt.show()

# Q5: unprofitable sub-categories
sub_df = df.groupby("Sub-Category").agg({"Profit": "sum", "Discount": "mean"})

unprofitable = sub_df[sub_df["Profit"] < 0]
print("\nLoss-Making Sub-Categories:\n", unprofitable)

avg_disc_unprofitable = sub_df[sub_df["Profit"] < 0]["Discount"].mean()
avg_disc_profitable = sub_df[sub_df["Profit"] >= 0]["Discount"].mean()

print(f"\nAvg Discount (Loss-Making): {avg_disc_unprofitable:.2%}")
print(f"Avg Discount (Profitable):  {avg_disc_profitable:.2%}")

sub_df["Profit"].sort_values().plot(kind="barh", title="Profit by Sub-Category")
plt.xlabel("Total Profit")
plt.axvline(0, color="red", linestyle="--")
plt.tight_layout()
plt.show()

sub_df["Discount"].sort_values().plot(kind="barh", title="Average Discount by Sub-Category")
plt.xlabel("Average Discount")
plt.tight_layout()
plt.show()