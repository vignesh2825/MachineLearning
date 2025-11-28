import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.markdown("<h2 style='text-align:center;'> Login</h2>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

if not st.session_state.logged_in:
    login_page()
    st.stop()

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

st.markdown("""
<style>
body { background: linear-gradient(120deg, #f6d5f7 0%, #fbe9d7 100%); } h1 { color: #5e0cff !important; font-weight: 900; text-shadow: 1px 1px 3px rgba(0,0,0,0.15); } .glass { background: rgba(255,255,255,0.55); padding: 25px; border-radius: 20px; backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.5); box-shadow: 0 8px 30px rgba(0,0,0,0.08); margin-bottom: 20px; } .stButton>button { background: linear-gradient(to right, #ff4b4b, #ff9068); color: white; font-weight: bold; border-radius: 12px; padding: 0.7em 1.4em; border: none; transition: 0.3s ease; } .stButton>button:hover { transform: scale(1.05); box-shadow: 0px 4px 15px rgba(0,0,0,0.2); }
</style>
""", unsafe_allow_html=True)

st.title("Instagram Engagement Predictor")

df = pd.read_csv("Instagram_Analytics.csv")
df = df.dropna(subset=["engagement_rate"])

X = df.select_dtypes(include=["int64", "float64"]).drop("engagement_rate", axis=1)
y = df["engagement_rate"]

numerical_columns = list(X.columns)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=120, random_state=42)
model.fit(X_train, y_train)

st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.subheader("Enter Post Values")

user_data = {}
for col in numerical_columns:
    user_data[col] = st.number_input(col, value=0.0, placeholder="Enter value")

st.markdown("</div>", unsafe_allow_html=True)

if st.button("Predict Engagement"):
    input_df = pd.DataFrame([user_data])
    result = model.predict(input_df)[0]
    st.success(f"Predicted Engagement Rate: {result:.2f} %")
