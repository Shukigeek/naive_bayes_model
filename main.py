from Data.interactor import DataLoader
from cleaning.Clean_Data import Clean
from model.naive_bayes_model import Model
from model.prediction import Predict
from model.Evaluation import ModelTester
from ui.cli_interface import get_input_from_user
from ui.message import greet_user
from ui.plot_utils import plot_prediction_results


def main():
    greet_user()

    # 1. טעינת דאטה
    print("📂 Loading dataset...")
    loader = DataLoader()
    # loader.load_data("C:/Users/shuki/AppData/Local/Microsoft/Windows/INetCache/IE/PQVOU4RU/buy_computer_data[1].csv","csv")
    # loader.load_data("all_star.csv", "csv")
    loader.load_from_mysql("root","","localhost","complaints","SELECT * FROM complaints")
    # 2. ניקוי דאטה
    print("🧹 Cleaning data...")
    loader.clean(Clean())
    df = loader.get_df()

    # 3. יצירת המודל
    print("🧠 Creating model...")
    target_column = "החלטה"
    model = Model(df, target_column)
    model.create_model()

    # 4. בדיקת ביצועים כלליים
    print("🔎 Testing model on full dataset...")
    tester = ModelTester(model)
    tester.test_full_dataset_prediction()
    tester.test_with_train_test_split()

    # 5. אינטראקציה עם המשתמש לחיזוי
    print("\n👤 Now let's make a prediction based on your input:")
    predictor = Predict(model)
    example_row = get_input_from_user(model.features, model)
    results = predictor.predict_row(example_row)
    predictor.print_prediction_results(results)
    #for a graph
    plot_prediction_results(results)

if __name__ == "__main__":
    main()
