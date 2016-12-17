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

def gen_plot(classifier, measure, file, fdata):
	ax = sns.factorplot(x="percentage", y="value", 
						hue="wfilter", data=fdata,
                   		size=2.5, aspect=1.5, 
                   		kind="bar", palette="Blues_d",
                   		legend=False)
	plt.title("{} classifier".format(classifier))
	plt.legend(title="Preprocessing", loc='center left', bbox_to_anchor=(1, 0.5))
	ax.set(ylabel=measure, xlabel='Test percentage')
	ax.savefig("/home/roger/Documents/projects/kdd2_report/imgs/{}.png".format(file))


query = 'classifier=="{}" and measure=="{}"'

for metric in metrics:
	for classifier in classifiers:

		fquery = query.format(classifier, metric)
		fdata = data.query(fquery)
		print fquery
		file = "{}_{}".format(classifier, metric)
		gen_plot(classifiers[classifier], metrics[metric], file, fdata)
