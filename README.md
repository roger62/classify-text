<center>Salam</center>

## Text Classification with python

Second Work Assignment for MAP-I KDD class.

### Dataset

The dataset used was the  ["Reuters Newsire"](http://www.daviddlewis.com/resources/testcollections/reuters21578/) dataset. 


When you run `main.py` it asks you for the root of the dataset. You can supply your own dataset assuming it has a similar directory structure.

#### UTF-8 incompatibility

Some of the supplied text files had incompatibility with utf-8!

Even textedit.app can't open those files. And they created problem in the code. So I'll delete them as part of the preprocessing.

### Requirements

* python 2.7

* python modules:

  * scikit-learn (v 0.11)
  * scipy (v 0.10.1)
  * colorama
  * termcolor
  * matplotlib (for use in `plot.py`)

### The code

The code is pretty straight forward and well documented.

#### Running the code

	python main.py

### Experiments

For experiments I used the subset of the dataset (as described above), 
coffe and interest on the folder reuters_test.

The report with the results is available in the repository on
the pdf report.pdf