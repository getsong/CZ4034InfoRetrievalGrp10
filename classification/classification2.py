import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.feature_selection import chi2

from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics.pairwise import cosine_similarity


import numpy as np
import time
np.set_printoptions(threshold=np.nan)


def model():
    #read json into df
    df = pd.read_json('amazon_Stemmed.json', orient='values')
    #print(df)


    # encode cat to integers
    print("\n Encoding..")
    cat = pd.Series(df['category'])
    enc = preprocessing.LabelEncoder()
    int_enc = enc.fit_transform(cat)
    labels = int_enc
    print("Encoded classes:", enc.classes_)


    #change into bag of  words
    print("\n Vectorizing...")
    tfidf = TfidfVectorizer(sublinear_tf=True, norm='l2')
    features = tfidf.fit_transform(df['description'])

    top_n = 10
    # try this below line or use just 5 for first 5 docs
    # ndocs = X_counts.shape[0]

    #print("Vocabulary:", tfidf.vocabulary_)
    #print("Stop words (should be none):", tfidf.get_stop_words())
    #print("Features:", features)


    #split train test data
    print("\n Training...")
    x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=44)
    show_set = df['description'][:50]
    show_tfidf = tfidf.transform(show_set)


    print("\n Shapes (X_Train, Y_train): ", x_train.shape, y_train.shape)
    print("Shapes (X_Test, Y_test): ", x_test.shape, y_test.shape)


    print("\n=========TRAINING NAIVES BAYES:MULTINOMIAL==========")

    nb = MultinomialNB()
    nb.fit(x_train, y_train)
    score = nb.score(x_test,y_test)
    pred = nb.predict(x_test)
    print(classification_report(y_test, pred, digits=5, target_names=enc.classes_))
    print("InterAnnotator Agreement score:" ,cohen_kappa_score(y_test, pred))
    #print("PRedictions", pred)
    #print("X_Test", tfidf.inverse_transform(x_test))
    pred_class = []
    for i in pred:
        c = enc.inverse_transform(i)
        pred_class.append(c)
    #print("Pred class", pred_class)


    print("=========TRAINING SVM.LINEARSVC==========")

    svc = svm.LinearSVC(verbose=0)
    start = time.time()
    svc.fit(x_train, y_train)
    print("Time taken to train:", time.time() - start)
    score = svc.score(x_test,y_test)
    pred = svc.predict(x_test)
    print(classification_report(y_test, pred, digits=5, target_names=enc.classes_))
    print("InterAnnotator Agreement score:" ,cohen_kappa_score(y_test, pred))


    print("\n ====SAMPLE PREDICTIONS FROM SVM====")
    for i in range(0,12000,500):
        data = df.iloc[i]
        sample = data['description']
        sample_c = data['category']
        print("\nSample description:", sample)
        print("Label:", sample_c)
        print("Predicted class:", enc.inverse_transform(svc.predict(tfidf.transform([sample]))))


    print("\n=========TRAINING SGD==========")
    sgd = SGDClassifier(verbose=0)
    sgd.fit(x_train, y_train)
    score = sgd.score(x_test,y_test)
    pred = sgd.predict(x_test)
    print(classification_report(y_test, pred, digits=5, target_names=enc.classes_))
    print("InterAnnotator Agreement score:" ,cohen_kappa_score(y_test, pred))


    print("=========TRAINING NEAREST NEIGHBOUR==========")
    knn = KNeighborsClassifier()
    knn.fit(x_train, y_train)
    score = knn.score(x_test, y_test)
    pred = knn.predict(x_test)
    print(classification_report(y_test, pred, digits=5, target_names=enc.classes_))
    print("InterAnnotator Agreement score:" ,cohen_kappa_score(y_test, pred))



    print("=========TRAINING DECISION TREE==========")
    dt = tree.DecisionTreeClassifier()
    dt.fit(x_train, y_train)
    score = dt.score(x_test, y_test)
    pred = dt.predict(x_test)
    print(classification_report(y_test, pred, digits=5, target_names=enc.classes_))
    print("InterAnnotator Agreement score:" ,cohen_kappa_score(y_test, pred))



    print("=========TRAINING RANDOM FOREST==========")
    rf = RandomForestClassifier()
    rf.fit(x_train, y_train)
    score = rf.score(x_test, y_test)
    pred = rf.predict(x_test)
    print(classification_report(y_test, pred, digits=5, target_names=enc.classes_))
    print("InterAnnotator Agreement score:" ,cohen_kappa_score(y_test, pred))

    print("*****************************************************************")
    print("**********************ENSEMBLE METHODS***************************")


    print("=========TRAINING RANDOM FOREST==========")
    rf = RandomForestClassifier()
    rf.fit(x_train, y_train)
    score = rf.score(x_test, y_test)
    pred = rf.predict(x_test)
    print(classification_report(y_test, pred, digits=5, target_names=enc.classes_))
    print("InterAnnotator Agreement score:" ,cohen_kappa_score(y_test, pred))

    print("=========TRAINING ADABOOST==========")
    abc = AdaBoostClassifier()
    abc.fit(x_train, y_train)
    score = abc.score(x_test, y_test)
    pred = abc.predict(x_test)
    print(classification_report(y_test, pred, digits=5, target_names=enc.classes_))
    print("InterAnnotator Agreement score:" ,cohen_kappa_score(y_test, pred))


    def most_informative_feature_for_class(vectorizer, classifier, classlabel, n=10):
        labelid = enc.transform([classlabel])
        feature_names = vectorizer.get_feature_names()
        topn = sorted(zip(classifier.coef_[labelid], feature_names))[-n:]

        for coef, feat in topn:
            print(classlabel, feat, coef)


def query_ing():
    # index the documents
    df = pd.read_json('amazon_Stemmed.json')

    tfidf = TfidfVectorizer(sublinear_tf=True, norm='l2')
    features = tfidf.fit_transform(df['description'])
    #features = features.toarray()
    # index query
    query = ["This is a sample query"]
    q = tfidf.transform(query)
    #print("Features tfidf",features)

    print("saving..")
    #np.save("features.npy", features.toarray())
    print("loading..")

    test = np.load("features.npy")
    print("LAODED NP: ", test)
    print("Query tfidf", q)

    sim = cosine_similarity(q, features)
    max_sim= np.amax(sim)

    #print("Cosine simi", sim)
    #print("COSINE SIMI max, argmax ",max_sim, np.argmax(sim))

    return features




if __name__ == "__main__":
    model()
