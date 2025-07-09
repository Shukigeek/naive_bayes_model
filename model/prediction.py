from model.naive_bayes_model import Model
import math

class Predict:
    def __init__(self, model: Model):
        self.model = model



    def predict_row(self, row: dict) -> dict:
        if not self.model.model:
            self.model.create_model()

        results = {}
        for label in self.model.labels:
            log_prob = 0
            for key, value in row.items():
                prob = self.model.model[key].get(value, {}).get(label, 1e-9)
                log_prob += math.log(prob)
            prior = len(self.model.df[self.model.df[self.model.classified] == label]) / len(self.model.df)
            log_prob += math.log(prior)
            results[label] = math.exp(log_prob)
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
