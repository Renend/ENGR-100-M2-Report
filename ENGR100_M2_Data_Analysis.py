import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load datasets
df_census = pd.read_csv("US Census Demographic 2024 - US Demographic 2024.csv")
df_model = pd.read_csv("ENGR 100 M2 Data Collection - Test Results.csv")

# Clean Label column
df_census["Label (Grouping)"] = df_census["Label (Grouping)"].astype(str).str.strip()

df_census.head(15)

# Census Race
row_total = df_census[df_census["Label (Grouping)"].str.strip()=="Total population"].iloc[0]

def to_int(x):
    try:
        return int(str(x).replace(",", ""))
    except:
        return None

total_pop = to_int(row_total["Total population"])
white_pop = to_int(row_total["White"])
black_pop = to_int(row_total["Black or African American"])
asian_pop = to_int(row_total["Asian"])
hispanic_pop = to_int(row_total["Hispanic or Latino "])

census_race = {
    "White": white_pop / total_pop * 100,
    "Black": black_pop / total_pop * 100,
    "Asian": asian_pop / total_pop * 100,
    "Hispanic": hispanic_pop / total_pop * 100,
    "Mixed/Other": 100 - ((white_pop + black_pop + asian_pop + hispanic_pop) / total_pop * 100)
}

# Model Race
model_race_raw = df_model["Perceived Race"].value_counts(normalize=True) * 100

model_breakdown = {
    "White": model_race_raw.get("White", 0),
    "Black": model_race_raw.get("Black", 0),
    "East Asian": model_race_raw.get("East Asian", 0),
    "South Asian": model_race_raw.get("South Asian", 0),
    "Hispanic": model_race_raw.get("Hispanic", 0),
    "Mixed/Other": model_race_raw.get("Mixed", 0) + model_race_raw.get("Other", 0)
}

# Plot
fig, ax = plt.subplots(figsize=(10,6))

bar_width = 0.35
x = np.arange(5)  # 5 race categories

# Customized colors
census_color = "#B5EAD7"     # mint pastel (Census)
model_main   = "#FFDAC1"     # peach pastel (Model default)
east_asian   = "#E2F0CB"     # light green for East Asian
south_asian  = "#F6EAC2"     # cream for South Asian

# Census bars
census_vals = [
    census_race["White"], census_race["Black"], census_race["Asian"],
    census_race["Hispanic"], census_race["Mixed/Other"]
]
bars_census = ax.bar(x - bar_width/2, census_vals,
                     width=bar_width, color=census_color, edgecolor="black", label="Census")

# Model bars
bars_model = []

# White
bars_model.append(ax.bar(x[0] + bar_width/2, model_breakdown["White"], width=bar_width,
                         color=model_main, edgecolor="black", label="Model White"))

# Black
bars_model.append(ax.bar(x[1] + bar_width/2, model_breakdown["Black"], width=bar_width,
                         color=model_main, edgecolor="black", label="Model Black"))

# Asian
bars_model.append(ax.bar(x[2] + bar_width/2, model_breakdown["East Asian"], width=bar_width,
                         color=east_asian, edgecolor="black", label="Model East Asian"))
bars_model.append(ax.bar(x[2] + bar_width/2, model_breakdown["South Asian"],
                         bottom=model_breakdown["East Asian"], width=bar_width,
                         color=south_asian, edgecolor="black", label="Model South Asian"))

# Hispanic
bars_model.append(ax.bar(x[3] + bar_width/2, model_breakdown["Hispanic"], width=bar_width,
                         color=model_main, edgecolor="black", label="Model Hispanic"))

# Mixed/Other
bars_model.append(ax.bar(x[4] + bar_width/2, model_breakdown["Mixed/Other"], width=bar_width,
                         color=model_main, edgecolor="black", label="Model Mixed/Other"))

# Percentage labels
for bar in bars_census:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
            f'{bar.get_height():.1f}%', ha='center', va='center', fontsize=9, color='black')

for container in bars_model:
    for bar in container:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_y() + height/2,
                f'{height:.1f}%', ha='center', va='center', fontsize=9, color='black')

# Formatting
ax.set_xticks(x)
ax.set_xticklabels(["White", "Black", "Asian", "Hispanic", "Mixed/Other"])
ax.set_ylabel("Percentage (%)")
ax.set_xlabel("Race Categories")
ax.set_title("Census vs Model: Race Distribution")  
ax.legend(loc="upper right", frameon=True)          
plt.tight_layout()
plt.show()

# Census Gender
census_gender = {
    "Male": 49.5,
    "Female": 50.5
}

# Model Gender
model_gender = df_model["Perceived Gender"].value_counts(normalize=True) * 100
model_gender = {
    "Male": model_gender.get("Male", 0),
    "Female": model_gender.get("Female", 0),
    "Ambiguous": model_gender.get("Ambiguous", 0)
}

# Plot
fig, ax = plt.subplots(figsize=(8,6))
x = np.arange(len(census_gender))  # 2 categories
bar_width = 0.35

# Colors
census_color = "#B5EAD7"
model_colors = ["#FFDAC1", "#FFB7B2", "#C7CEEA"]

bars_census = ax.bar(x - bar_width/2, census_gender.values(), width=bar_width,
                     color=census_color, edgecolor="black", label="Census")
bars_model = ax.bar(x + bar_width/2, [model_gender["Male"], model_gender["Female"]],
                    width=bar_width, color=model_colors[:1], edgecolor="black", label="Model")
bar_amb = ax.bar(len(x), model_gender["Ambiguous"], width=bar_width,
                 color=model_colors[2], edgecolor="black", label="Model Ambiguous")

# Percentage labels
for bar in bars_census:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
            f'{bar.get_height():.1f}%', ha='center', va='center', fontsize=9, color='black')
for bar in bars_model:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
            f'{bar.get_height():.1f}%', ha='center', va='center', fontsize=9, color='black')
for bar in bar_amb:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
            f'{bar.get_height():.1f}%', ha='center', va='center', fontsize=9, color='black')

# Formatting
ax.set_xticks(list(x) + [len(x)])
ax.set_xticklabels(list(census_gender.keys()) + ["Ambiguous"])
ax.set_ylabel("Percentage (%)")
ax.set_xlabel("Gender Categories")   
ax.set_title("Census vs Model: Gender Distribution") 
ax.legend(loc="upper right", frameon=True)            
plt.tight_layout()
plt.show()

# Census Age Groups
census_age = {
    "Child": 5.4,                         # under 5 years
    "Teen": 16.0,                         # 5–17 years
    "Young Adult": 9.2 + 13.6,            # 18–34 years
    "Middle-Aged": 13.5 + 12.0,           # 35–54 years
    "Elderly": 12.3 + 10.5 + 7.5          # 55+ years
}

# Model Age
model_age = df_model["Perceived Age"].value_counts(normalize=True) * 100

# Map categories
model_age_mapped = {
    "Child": model_age.get("Child", 0),
    "Teen": model_age.get("Teen", 0),
    "Young Adult": model_age.get("Young Adult", 0),
    "Middle-Aged": model_age.get("Middle", 0),   # “Middle” from model = “Middle-Aged”
    "Elderly": model_age.get("Elderly", 0)
}

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(census_age))
bar_width = 0.35

bars_census = ax.bar(
    x - bar_width/2, census_age.values(),
    width=bar_width, color="#B5EAD7", edgecolor="black", label="Census"
)
bars_model = ax.bar(
    x + bar_width/2, model_age_mapped.values(),
    width=bar_width, color="#FFDAC1", edgecolor="black", label="Model"
)

# Percentage labels
for bar in bars_census:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
            f'{bar.get_height():.1f}%', ha='center', va='center', fontsize=9)
for bar in bars_model:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
            f'{bar.get_height():.1f}%', ha='center', va='center', fontsize=9)

# Formatting
ax.set_xticks(x)
ax.set_xticklabels(census_age.keys())       # horizontal labels
ax.set_ylabel("Percentage (%)")
ax.set_xlabel("Age Categories")
ax.set_title("Census vs Model: Age Category Distribution")
ax.legend(loc="upper right", frameon=True)
plt.tight_layout()
plt.show()
