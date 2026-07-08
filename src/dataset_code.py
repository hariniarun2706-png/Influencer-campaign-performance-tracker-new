import pandas as pd
import numpy as np

np.random.seed(42)

n = 1000000

campaigns = ["Summer Sale", "Festive Offer", "New Launch", "Flash Sale", "Brand Awareness"]
platforms = ["Instagram", "YouTube", "Facebook", "TikTok", "Twitter"]
categories = ["Fashion", "Beauty", "Tech", "Fitness", "Food"]
audience = ["18-24", "25-34", "35-44", "45+"]
genders = ["Male", "Female", "Mixed"]

# -----------------------------------
# Create Basic Dataset
# -----------------------------------

df = pd.DataFrame({
    "Campaign_ID": ["CMP" + str(i).zfill(6) for i in range(1, n + 1)],
    "Campaign_Name": np.random.choice(campaigns, n),
    "Influencer_ID": ["INF" + str(i).zfill(3) for i in np.random.randint(1, 51, n)],
    "Influencer_Name": np.random.choice([
        "Aarav","Diya","Rahul","Priya","Kavin",
        "Meera","Arjun","Sneha","Riya","Vikram"
    ], n),
    "Platform": np.random.choice(
        platforms,
        n,
        p=[0.30,0.25,0.18,0.17,0.10]
    ),
    "Category": np.random.choice(categories, n),
    "Followers": np.random.randint(5000,2000000,n),
    "Audience_Group": np.random.choice(audience,n),
    "Gender": np.random.choice(genders,n),
    "Campaign_Date": pd.date_range("2025-01-01",periods=n,freq="D")
})

# -----------------------------------
# Reach (Followers based)
# -----------------------------------

df["Reach"] = (
    df["Followers"] *
    np.random.uniform(0.35,0.80,n)
).astype(int)

# -----------------------------------
# Impressions (Reach based)
# -----------------------------------

df["Impressions"] = (
    df["Reach"] *
    np.random.uniform(1.5,2.5,n)
).astype(int)

# -----------------------------------
# Platform Performance
# -----------------------------------

platform_factor = {
    "Instagram":1.30,
    "YouTube":1.15,
    "Facebook":0.90,
    "TikTok":1.05,
    "Twitter":0.75
}

platform_factor_values = df["Platform"].map(platform_factor)

# -----------------------------------
# Engagement Metrics
# -----------------------------------

df["Likes"] = (
    df["Reach"] *
    0.08 *
    platform_factor_values *
    np.random.uniform(0.9,1.1,n)
).astype(int)

df["Comments"] = (
    df["Reach"] *
    0.012 *
    platform_factor_values *
    np.random.uniform(0.9,1.1,n)
).astype(int)

df["Shares"] = (
    df["Reach"] *
    0.006 *
    platform_factor_values *
    np.random.uniform(0.9,1.1,n)
).astype(int)

# -----------------------------------
# Clicks
# -----------------------------------

df["Clicks"] = (
    df["Reach"] *
    np.random.uniform(0.05,0.15,n)
).astype(int)

# -----------------------------------
# Conversions
# -----------------------------------

df["Conversions"] = (
    df["Clicks"] *
    np.random.uniform(0.10,0.30,n)
).astype(int)

# -----------------------------------
# Campaign Spend
# -----------------------------------

df["Campaign_Spend"] = (
    df["Followers"] * 0.15 +
    np.random.randint(10000, 50000, n)
).astype(int)

# -----------------------------------
# Influencer Performance Factor
# -----------------------------------

influencer_factor = {
    "Aarav": 1.40,
    "Diya": 1.30,
    "Rahul": 1.20,
    "Priya": 1.15,
    "Kavin": 1.10,
    "Meera": 1.00,
    "Arjun": 0.95,
    "Sneha": 0.90,
    "Riya": 0.85,
    "Vikram": 0.80
}

influencer_factor_values = df["Influencer_Name"].map(influencer_factor)


# -----------------------------------
# Derived Features
# -----------------------------------

# Engagement
df["Engagement"] = (
    df["Likes"] +
    df["Comments"] +
    df["Shares"]
)

df["Revenue"] = (
    df["Campaign_Spend"] * 0.6 +
    influencer_factor_values * 300000 +
    df["Conversions"] * 500 +
    df["Engagement"] * 5
).astype(int)

# Engagement Rate
df["Engagement_Rate"] = (
    (df["Engagement"] / df["Reach"]) * 100
).round(2)

# Conversion Rate
df["Conversion_Rate"] = (
    (df["Conversions"] / df["Clicks"]) * 100
).round(2)

# ROI
df["ROI"] = (
    ((df["Revenue"] - df["Campaign_Spend"]) /
     df["Campaign_Spend"]) * 100
).round(2)

# Cost Per Engagement
df["Cost_Per_Engagement"] = (
    df["Campaign_Spend"] /
    df["Engagement"]
).round(2)
# -----------------------------------
# Influencer Type
# -----------------------------------

conditions = [
    df["Followers"] < 100000,
    (df["Followers"] >= 100000) &
    (df["Followers"] < 1000000),
    df["Followers"] >= 1000000
]

choices = [
    "Micro Influencer",
    "Macro Influencer",
    "Mega Influencer"
]

df["Influencer_Type"] = np.select(
    conditions,
    choices,
    default="Micro Influencer"
)

# -----------------------------------
# ROI Category
# -----------------------------------

df["ROI_Category"] = np.where(
    df["ROI"] >= 100,
    "High ROI",
    "Low ROI"
)

# -----------------------------------
# Engagement Category
# -----------------------------------

df["Engagement_Category"] = np.where(
    df["Engagement_Rate"] >= 10,
    "High Engagement",
    "Low Engagement"
)

# -----------------------------------
# Save Dataset
# -----------------------------------

df.to_csv(
    "Influencer_Campaign_Dataset.csv",
    index=False
)

print(df.head())
print("\nDataset Shape :",df.shape)