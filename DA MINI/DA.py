import pandas as pd
import matplotlib.pyplot as plt

# Preprocessing
def preprocess_data(df):
    df = df.copy()

    df.columns = df.columns.str.strip()

    df.dropna(inplace=True)

    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

    numeric_cols = ['Energy_Consumption_TWh', 'Coal', 'Oil', 'Gas', 'Renewables']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df.dropna(inplace=True)

    return df


# Analysis
def energy_analysis(df):
    results = {}

    results["total_by_country"] = df.groupby("Country")["Energy_Consumption_TWh"].sum()

    results["yearly_trend"] = df.groupby("Year")["Energy_Consumption_TWh"].sum()

    results["top5"] = results["total_by_country"].sort_values(ascending=False).head(5)

    sources = ['Coal', 'Oil', 'Gas', 'Renewables']
    results["source_distribution"] = df[sources].sum()

    total_energy = results["source_distribution"].sum()
    results["renewable_percentage"] = (results["source_distribution"]['Renewables'] / total_energy) * 100

    return results


def print_results(results):
    print("\nTotal Energy Consumption by Country:\n")
    print(results["total_by_country"])

    print("\nYear-wise Energy Trend:\n")
    print(results["yearly_trend"])

    print("\nTop 5 Countries:\n")
    print(results["top5"])

    print("\nEnergy Source Distribution:\n")
    print(results["source_distribution"])

    print(f"\nRenewable Energy Percentage: {results['renewable_percentage']:.2f}%")


# Visualization
def plot_energy_trend(df):
    yearly = df.groupby('Year')["Energy_Consumption_TWh"].sum()

    plt.figure(figsize=(10,5))
    plt.plot(yearly.index, yearly.values)
    plt.title("Global Energy Consumption Trend")
    plt.xlabel("Year")
    plt.ylabel("TWh")
    plt.show()


def plot_country_comparison(df):
    total = df.groupby("Country")["Energy_Consumption_TWh"].sum()

    total.plot(kind='bar', figsize=(8,5))
    plt.title("Energy Consumption by Country")
    plt.ylabel("TWh")
    plt.show()


def plot_energy_sources(df):
    sources = ['Coal', 'Oil', 'Gas', 'Renewables']
    totals = df[sources].sum()

    plt.figure()
    plt.pie(totals, labels=sources, autopct='%1.1f%%')
    plt.title("Energy Source Distribution")
    plt.show()


def plot_energy_mix(df):
    sources = ['Coal', 'Oil', 'Gas', 'Renewables']
    mix = df.groupby("Country")[sources].sum()

    mix.plot(kind='bar', stacked=True, figsize=(10,6))
    plt.title("Energy Mix by Country")
    plt.ylabel("TWh")
    plt.show()


# Flask App
app = Flask(__name__)

@app.route('/')
def home():
    return "Global Energy Dashboard Running Successfully"


# Main
if __name__ == "__main__":

    try:
        df = pd.read_csv("energy.csv")
    except FileNotFoundError:
        print("Error: energy.csv not found")
        exit()

    df = preprocess_data(df)

    results = energy_analysis(df)
    print_results(results)

    plot_energy_trend(df)
    plot_country_comparison(df)
    plot_energy_sources(df)
    plot_energy_mix(df)

    print("\nProject Executed Successfully")

    # app.run(debug=True)