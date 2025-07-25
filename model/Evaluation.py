from model.naive_bayes_model import Model
from model.prediction import Predict
from sklearn.model_selection import train_test_split
import pandas as pd


class ModelTester:
    def __init__(self, model: Model):
        self.model = model
        self.predictor = Predict(model)

    def test_full_dataset_prediction(self):
        df = self.model.df
        classifier = self.model.classified
        correct = 0
        total = len(df)

        for _idx, row in df.iterrows():
            input_row = {feature: row[feature] for feature in self.model.features}
            results = self.predictor.predict_row(input_row)
            predicted = max(results, key=results.get)
            actual = row[classifier]
            if predicted == actual:
                correct += 1

        accuracy = correct / total
        print(f"Accuracy on full dataset: {accuracy*100:.2f}% ({correct}/{total})")
        return accuracy

    def test_with_train_test_split(self, test_size=0.3):
        df = self.model.df
        X = df.drop(columns=[self.model.classified])
        y = df[self.model.classified]


        X = X.astype(str)


        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)


        train_df = X_train.copy()
        train_df[self.model.classified] = y_train


        new_model = type(self.model)(train_df, self.model.classified)
        new_model.create_model()
        predictor = Predict(new_model)


        correct = 0
        total = len(X_test)

        for i in range(total):
            row = X_test.iloc[i].to_dict()
            true_label = y_test.iloc[i]
            results = predictor.predict_row(row)
            predicted = max(results, key=results.get)
            if predicted == true_label:
                correct += 1

        accuracy = correct / total
        print(
            f"✅ Accuracy on test set ({int((1 - test_size) * 100)}% train / {int(test_size * 100)}% test): {accuracy:.2%}")

