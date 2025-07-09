import matplotlib.pyplot as plt
from model.naive_bayes_model import Model

class Predict:
    def __init__(self, model: Model):
        self.model = model
    def predict_row(self, row: dict) -> dict:

        if not self.model.model:
            self.model.create_model()

        results = {}
        for label in self.model.labels:
            prob = 1
            for key, value in row.items():
                prob *= self.model.model[key][value][label]
            prior = len(self.model.df[self.model.df[self.model.classified] == label]) / len(self.model.df)
            results[label] = prob * prior
        return results

    def print_prediction_results(self,results: dict):
        total = sum(results.values())
        print("\nPrediction results:")
        for label, score in results.items():
            print(f"{label}: {round(score * 100 / total, 2)}%")
        final_prediction = max(results, key=results.get)
        print(f"\n🧠 Predicted class: {self.model.classified} = {final_prediction}")



if __name__ == '__main__':
    pass
