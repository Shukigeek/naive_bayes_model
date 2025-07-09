import matplotlib.pyplot as plt

def plot_prediction_results(results: dict):
    labels = list(results.keys())
    total = sum(results.values())
    values = [round(score * 100 / total, 2) for score in results.values()]
    plt.bar(labels, values, color='skyblue')
    plt.ylabel('Probability (%)')
    plt.title('Prediction Results')
    plt.show()
