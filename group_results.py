import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

sns.set_context("paper")
#plt.figure(figsize=(8, 6))

sns.set_style("ticks")
data = pd.read_csv("results.csv")


metrics = {"precision": "Precision", "recall": "Recall", "f1_score": "F1 Score"}
classifiers = {"bayes": "Multinomial Bayes", "svc": "SVC", "knn":"Nearest Neighbors", "dtree": "Decision Trees"}

fquery = 'measure=="{}"'.format("f1_score")
fdata = data.query(fquery)
print fdata
ax = sns.factorplot(x="percentage", y="value", 
					hue="wfilter", data=fdata,
               		size=2.5, aspect=1, 
               		kind="bar", palette="Blues_d",
               		col="classifier",
               		col_wrap=2)
#plt.title("{} classifier".format("bayes"))
#plt.legend(title="Preprocessing", loc='upper right')
#plt.title("Bayes classifier")
#plt.title('Center Title')
#plt.title('Center Title')
#ax.set(ylabel="", xlabel='Test percentage')

#ax.savefig("/home/roger/Documents/projects/kdd2_report/imgs/f1_score.png")
plt.show()


