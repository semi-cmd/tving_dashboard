import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


def run_pipeline():

    print("Loading data...")

    watch = pd.read_csv("data/raw/synthetic_watch_2025.csv")
    search = pd.read_csv("data/raw/synthetic_search_2025.csv")
    recommend = pd.read_csv("data/raw/synthetic_recommend_2025.csv")

    print("Preprocessing...")

    watch["timestamp"] = pd.to_datetime(watch["timestamp"])
    search["timestamp"] = pd.to_datetime(search["timestamp"])
    recommend["timestamp"] = pd.to_datetime(recommend["timestamp"])

    watch["date"] = watch["timestamp"].dt.date

    print("Building features...")

    watch_feat = watch.groupby("user_id").agg(
        total_watch_time=("view_duration_minutes","sum"),
        watch_count=("movie_id","count")
    )

    search_feat = search.groupby("user_id").agg(
        search_count=("search_query","count"),
        avg_search_time=("search_duration_seconds","mean"),
        search_click_rate=("is_clicked","mean")
    )

    reco_feat = recommend.groupby("user_id").size().to_frame("recommend_count")

    features = watch_feat.join(search_feat).join(reco_feat)

    features = features.fillna(0)

    os.makedirs("data/processed", exist_ok=True)

    features.to_csv("data/processed/feature_table.csv")

    print("Feature table saved")

    print("Creating churn label...")

    last_watch = watch.groupby("user_id")["timestamp"].max()

    dataset_end = watch["timestamp"].max()

    inactivity_days = (dataset_end - last_watch).dt.days

    churn = (inactivity_days >= 28).astype(int)

    churn_df = churn.to_frame("churn")

    dataset = features.join(churn_df)

    print("Training model...")

    X = dataset.drop("churn",axis=1)
    y = dataset["churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,y,test_size=0.2,random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8
    )

    model.fit(X_train,y_train)

    print("Predicting risk...")

    risk_score = model.predict_proba(features)[:,1]

    prediction = features.copy()

    prediction["risk_score"] = risk_score

    prediction.to_csv("data/processed/prediction_result.csv")

    print("Prediction result saved")

    prediction["active_hour_score"] = 0.8

    prediction["intervention_score"] = prediction["risk_score"] * 0.8

    prediction.to_csv("data/processed/intervention_result.csv")

    print("Intervention result saved")

    print("Pipeline complete!")


if __name__ == "__main__":
    run_pipeline()