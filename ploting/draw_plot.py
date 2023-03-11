# python3 ploting/draw_plot.py

import pandas as pd
import matplotlib.pyplot as plt

def draw_ppo(source):
  df = pd.read_csv(source)
  diagram = df.plot(
    x="Step",
    y="Value",
    ylabel="Reward",
    xlabel="Step"
  )
  plt.legend(["Mean episodic reward"])
  plt.show()


def draw_one_plot(source, colors=None):
  df = pd.read_csv(source)

  diagram = df.plot(
    x="Generation",
    y=["Best fitness", "Population fitness mean", "Top10 fitness mean"],
    ylabel="Fitness",
    color=colors
  )
  # Fitness value above 1.7 means the car parked ideally
  plt.axhline(y=1.7, color='black', linestyle='--')
  # 1.3 fitness value indicates that the car parked in the specified space imprecisely(but good enough)
  plt.axhline(y=1.3, color='blue', linestyle='--'),
  plt.legend(["Best", "Population mean", "Top10 mean", "Parked perfectly", "Parked well"], prop={'size': 9})
  plt.show()

def draw_multiple(sources, labels, colors=None):
  dfs = []
  for source in sources:
    df = pd.read_csv(source)
    dfs.append(df[["Generation", "Best fitness"]])

  merged_df = dfs[0]
  for i in range(1, len(dfs)):
    merged_df = merged_df.merge(dfs[i],on='Generation')

  diagram = merged_df.plot(x="Generation", ylabel="Fitness", color=colors)

  # Fitness value above 1.7 means the car parked ideally
  plt.axhline(y=1.7, color='black', linestyle='--')
  # 1.3 fitness value indicates that the car parked in the specified space imprecisely(but good enough)
  plt.axhline(y=1.3, color='blue', linestyle='--')

  plt.legend(labels + ["Parked perfectly", "Parked well"], prop={'size': 9})
  plt.show()

# Put here paths to csv files
sources=[
  '',
  '',
]

# Labels for each csv file
labels = [
  "",
]
colors =['red', 'green', '#9A0EEA']

draw_one_plot('', colors)
# draw_multiple(sources, labels)
