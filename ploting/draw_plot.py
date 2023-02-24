# python3 ploting/draw_plot.py

import pandas as pd
import matplotlib.pyplot as plt

def draw_one_plot(source):
  df = pd.read_csv(source)

  diagram = df.plot(x="Generation", y=["Best fitness", "Population fitness mean", "Top10 fitness mean"], ylabel="Fitness")
  # 1.3 fitness value indicates that the car parked in the specified space imprecisely(but good enough)
  plt.axhline(y=1.3, color='r', linestyle='--'),
  # Fitness value above 1.7 means the car parked ideally
  plt.axhline(y=1.7, color='b', linestyle='--')
  plt.legend(["Best", "Population mean", "Top10 mean", "Parked well", "Parked perfectly"], prop={'size': 8})
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

  # 1.3 fitness value indicates that the car parked in the specified space imprecisely(but good enough)
  plt.axhline(y=1.3, color='r', linestyle='--')
  # Fitness value above 1.7 means the car parked ideally
  plt.axhline(y=1.7, color='cyan', linestyle='--')

  # plt.legend(labels + ["Parked well", "Parked perfectly"], prop={'size': 8}, loc='lower right')
  plt.legend(labels + ["Parked well", "Parked perfectly"], prop={'size': 8})
  plt.show()

# Put here paths to csv files
sources=[
  'path1',
  'path2'
]

# Labels for each csv file
labels = [
  "Label for path1",
  "Label for path2"
]

colors =['blue', 'green', '#A2142F']

# draw_one_plot('path')
draw_multiple(sources, labels, colors)
