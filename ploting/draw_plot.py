# python3 ploting/draw_plot.py

import pandas as pd
import matplotlib.pyplot as plt

def draw_one_plot(source):
  df = pd.read_csv(source)

  diagram = df.plot(x="Generation", y=["Best fitness", "Population fitness mean", "Top10 fitness mean"], ylabel="Fitness")
  plt.show()

def draw_multiple(sources, labels):
  dfs = []
  for source in sources:
    df = pd.read_csv(source)
    dfs.append(df[["Generation", "Best fitness"]])

  merged_df = dfs[0]
  for i in range(1, len(dfs)):
    merged_df = merged_df.merge(dfs[i],on='Generation')

  diagram = merged_df.plot(x="Generation", ylabel="Fitness")

  # plt.legend(labels,loc='lower right')
  plt.legend(labels)
  plt.show()


# Put here paths to csv files
sources=[
  'path1',
  'path2',
]

# Labels for each csv file
labels = [
  "Label for path1",
  "Label for path2",
]

# draw_one_plot('path')
draw_multiple(sources, labels)
