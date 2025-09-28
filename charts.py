
import matplotlib.pyplot as plt
from datetime import datetime

def plot_bmi_trend(records):
    """Plots the BMI trend for a user using matplotlib."""
    if not records:
        return

    dates = [datetime.strptime(rec[0], "%Y-%m-%d %H:%M:%S") for rec in records]
    bmis = [rec[1] for rec in records]

    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(dates, bmis, marker='o', linestyle='-', color='#4c85ff', label='BMI')

    ax.set_title('BMI Trend Over Time', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('BMI Value', fontsize=12)
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.show()
