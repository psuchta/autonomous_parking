import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/pawelsuchta/Projects/Studia/autonomous_parking/genetic/plots/(3)genetic_1086_float_True_0.15_0.6_tournament_10_32_0.8.csv')
# Draw plot
diagram = df.plot(x="Generation", y=["Best fitness", "Population fitness mean", "Top10 fitness mean"], ylabel="Fitness")
plt.show()