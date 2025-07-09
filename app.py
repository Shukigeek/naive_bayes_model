import streamlit as st
from model.naive_bayes_model import Model
from model.prediction import Predict
from Data.interactor import DataLoader
from cleaning.Clean_Data import Clean


# טעינת דאטה
@st.cache_data
def load_model():
    loader = DataLoader()
    loader.load_data("all_star.csv","csv")
    # loader.load_from_mysql("root", "", "localhost", "complaints", "SELECT * FROM complaints")
    loader.clean(Clean())
    df = loader.get_df()
    model = Model(df, "Label")
    model.create_model()
    return model


# הרצה
st.set_page_config(page_title="Naive Bayes Classifier", layout="centered")
st.title("🧠 מערכת סיווג Naive Bayes")
st.markdown("הזן נתונים וקבל תחזית לסיווג")

model = load_model()
predictor = Predict(model)

# קלט מהמשתמש
user_input = {}
for feature in model.features:
    options = list(model.model[feature].keys())
    user_input[feature] = st.selectbox(f"בחר ערך עבור '{feature}':", options)

# לחצן לניבוי
if st.button("נבא"):
    results = predictor.predict_row(user_input)
    st.subheader("📊 תוצאות תחזית:")

    total = sum(results.values())
    sorted_results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))

    for label, prob in sorted_results.items():
        st.write(f"**{label}**: {round(prob * 100 / total, 2)}%")

    st.success(f"🔮 התחזית הסופית: {max(results, key=results.get)}")

    # גרף עוגה
    import matplotlib.pyplot as plt

    labels = list(results.keys())
    values = [round(score * 100 / total, 2) for score in results.values()]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    ax.axis('equal')
    st.pyplot(fig)
