from sklearn import tree
from sklearn.metrics import accuracy_score

clf = tree.DecisionTreeClassifier()
#t0 = time() 
clf = clf.fit(features_train, labels_train)
#print "training time:", round(time()-t0, 3), "s"

#t0 = time()
pred = clf.predict(features_test)
#print "Predict time:", round(time()-t0, 3), "s"

accuracy = accuracy_score(labels_test, pred)
#print "Accuracy score:" + str(accuracy)