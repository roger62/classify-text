import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns.set_style("whitegrid")
tips = pd.read_csv("results.csv")

ax = sns.barplot(x="classifier", y="value", data=tips)
plt.show()