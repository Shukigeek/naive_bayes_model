import matplotlib.pyplot as plt

def plot_prediction_results(results: dict):
    labels = list(results.keys())
    total = sum(results.values())

    values = [round(score * 100 / total, 2) for score in results.values()]

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    axs[0].bar(labels, values, color='skyblue')
    axs[0].set_ylabel('Probability (%)')
    axs[0].set_title('Prediction - Bar Chart')

    axs[1].pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    axs[1].axis('equal')
    axs[1].set_title('Prediction - Pie Chart')

    plt.tight_layout()
    plt.show()

