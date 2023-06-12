from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split,cross_val_score,KFold
from repository.event_repository import EventRepository
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import json

def crossValidate():
    dataset = EventRepository().getMusicalEventRates()
    dataset["category"] = dataset["category"].map({"Concert": 0, "Festival": 1})
    dataset["price"] = dataset["price"].map({False: 0, True: 1})
    dataset["private"] = dataset["private"].map({False: 0, True: 1})
    y = dataset["rate"]
    dataset = dataset.drop("rate", axis = 1)
    X_train, X_test, y_train, y_test = train_test_split(dataset, y, test_size=0.2, random_state=42)

    models = []
    models.append(('LR', LogisticRegression(max_iter=1500)))
    models.append(('KNN', KNeighborsClassifier()))
    models.append(('RF', RandomForestClassifier()))
    models.append(('DT', DecisionTreeClassifier()))
    
    results = dict()
    for name, model in models:
        kfold = KFold(n_splits=10,random_state=7, shuffle=True)
        cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring='accuracy')
        results[name]= (cv_results.mean())

    return results

def predictMusical(dataset):
    dataset["category"] = dataset["category"].map({"Concert": 0, "Festival": 1})
    dataset["price"] = dataset["price"].map({False: 0, True: 1})
    dataset["private"] = dataset["private"].map({False: 0, True: 1})
    y = dataset["rate"]
    dataset = dataset.drop("rate", axis = 1)

    X_train, X_test, y_train, y_test = train_test_split(dataset, y, test_size=0.2, random_state=42)


    rf =  RandomForestClassifier(n_estimators=100)
    rf.fit(X_train, y_train)
    #####
    pred_events = EventRepository().getUpcomingMusicalEvents()
    input = pred_events

    input = input.drop("id", axis = 1)
    input = input.drop("event_type", axis = 1)

    pred_events = pred_events.drop("category", axis = 1)
    pred_events = pred_events.drop("price", axis = 1)
    pred_events = pred_events.drop("private", axis = 1)
    pred_events = pred_events.drop("start_date", axis = 1)
    pred_events = pred_events.drop("end_date", axis = 1)
    
    input["category"] = input["category"].map({"Concert": 0, "Festival": 1})
    input["price"] = input["price"].map({False: 0, True: 1})
    input["private"] = input["private"].map({False: 0, True: 1})
    
    pred = rf.predict(input).tolist()
    pred_events['prediction'] = pred
    pred_events = pred_events.sort_values(by="prediction", ascending=False)
    json_data = pred_events.to_json(orient='records')

    return json.loads(json_data)

def predictSport(dataset):
    dataset["category"] = dataset["category"].map({"Football": 0, "Basketball": 1, "Volleyball": 2, "Jogging": 3})
    dataset["price"] = dataset["price"].map({False: 0, True: 1})
    dataset["private"] = dataset["private"].map({False: 0, True: 1})
    y = dataset["rate"]
    dataset = dataset.drop("rate", axis = 1)

    X_train, X_test, y_train, y_test = train_test_split(dataset, y, test_size=0.2, random_state=42)


    rf =  RandomForestClassifier(n_estimators=100)
    rf.fit(X_train, y_train)
    #####
    pred_events = EventRepository().getUpcomingSportEvents()
    input = pred_events

    input = input.drop("id", axis = 1)
    input = input.drop("event_type", axis = 1)

    pred_events = pred_events.drop("category", axis = 1)
    pred_events = pred_events.drop("price", axis = 1)
    pred_events = pred_events.drop("private", axis = 1)
    pred_events = pred_events.drop("start_date", axis = 1)
    pred_events = pred_events.drop("end_date", axis = 1)
    
    input["category"] = input["category"].map({"Football": 0, "Basketball": 1, "Volleyball": 2, "Jogging": 3})
    input["price"] = input["price"].map({False: 0, True: 1})
    input["private"] = input["private"].map({False: 0, True: 1})
    
    pred = rf.predict(input).tolist()
    pred_events['prediction'] = pred
    pred_events = pred_events.sort_values(by="prediction", ascending=False)
    json_data = pred_events.to_json(orient='records')

    return json.loads(json_data)


def predictNature(dataset):
    dataset["category"] = dataset["category"].map({"Camp": 0, "Hiking": 1})
    dataset["price"] = dataset["price"].map({False: 0, True: 1})
    dataset["private"] = dataset["private"].map({False: 0, True: 1})
    y = dataset["rate"]
    dataset = dataset.drop("rate", axis = 1)

    X_train, X_test, y_train, y_test = train_test_split(dataset, y, test_size=0.2, random_state=42)


    rf =  RandomForestClassifier(n_estimators=100)
    rf.fit(X_train, y_train)
    #####
    pred_events = EventRepository().getUpcomingNatureEvents()
    input = pred_events

    input = input.drop("id", axis = 1)
    input = input.drop("event_type", axis = 1)

    pred_events = pred_events.drop("category", axis = 1)
    pred_events = pred_events.drop("price", axis = 1)
    pred_events = pred_events.drop("private", axis = 1)
    pred_events = pred_events.drop("start_date", axis = 1)
    pred_events = pred_events.drop("end_date", axis = 1)
    
    input["category"] = input["category"].map({"Camp": 0, "Hiking": 1})
    input["price"] = input["price"].map({False: 0, True: 1})
    input["private"] = input["private"].map({False: 0, True: 1})
    
    pred = rf.predict(input).tolist()
    pred_events['prediction'] = pred
    pred_events = pred_events.sort_values(by="prediction", ascending=False)
    json_data = pred_events.to_json(orient='records')

    return json.loads(json_data)

def predictStagePlay(dataset):
    dataset["category"] = dataset["category"].map({"Theatre": 0, "StandUp": 1})
    dataset["price"] = dataset["price"].map({False: 0, True: 1})
    dataset["private"] = dataset["private"].map({False: 0, True: 1})
    y = dataset["rate"]
    dataset = dataset.drop("rate", axis = 1)

    X_train, X_test, y_train, y_test = train_test_split(dataset, y, test_size=0.2, random_state=42)

    rf =  RandomForestClassifier(n_estimators=100)
    rf.fit(X_train, y_train)
    #####
    pred_events = EventRepository().getUpcomingStagePlayEvents()
    input = pred_events

    input = input.drop("id", axis = 1)
    input = input.drop("event_type", axis = 1)

    pred_events = pred_events.drop("category", axis = 1)
    pred_events = pred_events.drop("price", axis = 1)
    pred_events = pred_events.drop("private", axis = 1)
    pred_events = pred_events.drop("start_date", axis = 1)
    pred_events = pred_events.drop("end_date", axis = 1)
    
    input["category"] = input["category"].map({"Theatre": 0, "StandUp": 1})
    input["price"] = input["price"].map({False: 0, True: 1})
    input["private"] = input["private"].map({False: 0, True: 1})
    
    pred = rf.predict(input).tolist()
    pred_events['prediction'] = pred
    pred_events = pred_events.sort_values(by="prediction", ascending=False)
    json_data = pred_events.to_json(orient='records')

    return json.loads(json_data)