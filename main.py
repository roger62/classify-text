import util
import sklearn.datasets
import sklearn.metrics
import sklearn.cross_validation
import sklearn.svm
import sklearn.naive_bayes
import sklearn.neighbors
from sklearn.tree import DecisionTreeClassifier
from colorama import init
from termcolor import colored
import sys
import os
import glob


def main():
    init()

    # get the dataset
    print colored("Where is the dataset?", 'cyan', attrs=['bold'])
    print colored('warning: files might get deleted if they are incompatible with utf8', 'yellow')
    ans = sys.stdin.readline()
    # remove any newlines or spaces at the end of the input
    path = ans.strip('\n')
    if path.endswith(' '):
        path = path.rstrip(' ')

    # preprocess data into two folders instead of 6
    print colored("Reorganizing folders, into two classes", 'cyan', attrs=['bold'])
    reorganize_dataset(path)

    print '\n\n'

    # do the main test
    main_test(path)


def reorganize_dataset(path):
    likes = ['rec.sport.hockey', 'sci.crypt', 'sci.electronics']
    dislikes = ['sci.space', 'rec.motorcycles', 'misc.forsale']

    folders = glob.glob(os.path.join(path, '*'))
    if len(folders) == 2:
        return
    else:
        # create `likes` and `dislikes` directories
        if not os.path.exists(os.path.join(path, 'likes')):
            os.makedirs(os.path.join(path, 'likes'))
        if not os.path.exists(os.path.join(path, 'dislikes')):
            os.makedirs(os.path.join(path, 'dislikes'))

        for like in likes:
            files = glob.glob(os.path.join(path, like, '*'))
            for f in files:
                parts = f.split(os.sep)
                name = parts[len(parts) - 1]
                newname = like + '_' + name
                os.rename(f, os.path.join(path, 'likes', newname))
            os.rmdir(os.path.join(path, like))

        for like in dislikes:
            files = glob.glob(os.path.join(path, like, '*'))
            for f in files:
                parts = f.split(os.sep)
                name = parts[len(parts) - 1]
                newname = like + '_' + name
                os.rename(f, os.path.join(path, 'dislikes', newname))
            os.rmdir(os.path.join(path, like))


def store_results(path, score, percentage, classifier_name, wfilter, values):

    #print values
    f = open(path,'arw')
    for val in values:
        #print val
        line = "{},{},{},{},{}".format(classifier_name, percentage, wfilter, score, val)
        f.write(line)
        f.write("\n")
    f.close()

def benchmark_clasifier(path, percentage, wfilter, classifier_name, n_tests, document_term_matrix, data, clf, 
                        test_size, y_names, confusion=False):
    
    results = []
    for _ in range(0, n_tests):

        res = test_classifier(document_term_matrix, data, clf, 
                    test_size=0.8, y_names=y_names, confusion=False)
        results.append(res)


    for i in range(0, len(y_names)):
        precision = []
        recall = []
        f1_score = []

        for (prec, rec, f1) in results:
            precision.append(prec[i])
            recall.append(rec[i])
            f1_score.append(f1[i])

        prec_file_path = "{}/prec_{}.txt".format(path, y_names[i])
        recall_file_path = "{}/recall_{}.txt".format(path, y_names[i])
        f1_file_path = "{}/f1_{}.txt".format(path, y_names[i])

        store_results(path, "precision", percentage, classifier_name, wfilter, precision)
        store_results(path, "recall", percentage, classifier_name, wfilter, recall)
        store_results(path, "f1_score", percentage, classifier_name, wfilter, f1_score)


def main_test(path=None):
    dir_path = path or 'reuters_test'
    remove_incompatible_files(dir_path)

    print '\n\n'

    # load data
    print colored('Loading files into memory', 'green', attrs=['bold'])
    files = sklearn.datasets.load_files(dir_path)

    # refine all emails
    print colored('Refining all files', 'green', attrs=['bold'])
    #util.refine_all_documents(files.data)

    # calculate the BOW representation
    print colored('Calculating BOW', 'green', attrs=['bold'])
    word_counts = util.bagOfWords(files.data)
    #print "bag"
    #print word_counts
    # TFIDF
    print colored('Calculating TFIDF', 'green', attrs=['bold'])
    tf_transformer = sklearn.feature_extraction.text.TfidfTransformer(use_idf=True).fit(word_counts)
    document_term_matrix = tf_transformer.transform(word_counts)
    
    #print(document_term_matrix)
    
    print colored('Testing classifier with train-test split', 'magenta', attrs=['bold'])

    print files.target_names
    classifiers = ["bayes", "svc", "knn", "dtree"]
    percentage = [0.2, 0.4, 0.6, 0.8]

    for classifier in classifiers:

        clf = None

        if classifier is "bayes":
            clf = sklearn.naive_bayes.MultinomialNB()
        elif classifier is "svc":
            clf = sklearn.svm.LinearSVC()
        elif classifier is "knn":
            n_neighbors = 11
            weights = 'uniform'
            weights = 'distance'
            clf = sklearn.neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
        elif classifier is "dtree":
            clf  = DecisionTreeClassifier(random_state=0)
        
        for perc in percentage:
            path = "results.txt"

            #os.makedirs(path)
            benchmark_clasifier(path, perc, True, classifier, 100, document_term_matrix, files.target, clf, 
                        test_size=0.8, y_names=files.target_names, confusion=False)


def remove_incompatible_files(dir_path):
    # find incompatible files
    print colored('Finding files incompatible with utf8: ', 'green', attrs=['bold'])
    incompatible_files = util.find_incompatible_files(dir_path)
    print colored(len(incompatible_files), 'yellow'), 'files found'

    # delete them
    if(len(incompatible_files) > 0):
        print colored('Deleting incompatible files', 'red', attrs=['bold'])
        util.delete_incompatible_files(incompatible_files)


def test_classifier(X, y, clf, test_size=0.4, y_names=None, confusion=False):
    # train-test split
    #print 'test size is: %2.0f%%' % (test_size * 100)
    X_train, X_test, y_train, y_test = sklearn.cross_validation.train_test_split(X, y, test_size=test_size)

    clf.fit(X_train, y_train)
    y_predicted = clf.predict(X_test)
    
    if not confusion:
        #print colored('Classification report:', 'magenta', attrs=['bold'])
        metrics =  sklearn.metrics.classification_report(y_test, y_predicted, target_names=y_names)
        #print metrics
        precision =  sklearn.metrics.precision_score(y_test, y_predicted, average=None)
        recall =  sklearn.metrics.recall_score(y_test, y_predicted, average=None)
        f1_score =  sklearn.metrics.f1_score(y_test, y_predicted, average=None)

        return (precision, recall, f1_score)
    else:
        print colored('Confusion Matrix:', 'magenta', attrs=['bold'])
        print sklearn.metrics.confusion_matrix(y_test, y_predicted)

if __name__ == '__main__':
    main_test()
