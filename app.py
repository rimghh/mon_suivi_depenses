import os
from datetime import date
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

CSV_PATH = "expenses.csv"

# --- Fonctions CSV ---
def load_csv():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    return pd.DataFrame(columns=["date", "category", "amount", "desc"])

def save_csv(df):
    df.to_csv(CSV_PATH, index=False)

# --- Données ---
df = load_csv()

# --- UI ---
st.title("💰 Money Tracker — Gérez vos dépenses simplement !")

col1, col2 = st.columns(2)
with col1:
    d = st.date_input("Date", value=date.today())
    cat = st.selectbox("Catégorie", ["Alimentation", "Transport", "Logement", "Shopping", "Autres"])
with col2:
    amount = st.number_input("Montant (€)", min_value=0.0, step=1.0)
    desc = st.text_input("Description (facultatif)")

if st.button("➕ Ajouter"):
    if amount > 0:
        new_row = {"date": d.isoformat(), "category": cat, "amount": amount, "desc": desc}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_csv(df)
        st.success("✅ Enregistré dans expenses.csv")
    else:
        st.warning("⚠️ Entrez un montant > 0")

st.markdown("---")

# --- Tableau + total ---
st.subheader("📋 Mes dépenses")
st.dataframe(df, use_container_width=True)

total = float(df["amount"].sum()) if not df.empty else 0.0
st.metric("💵 Total", f"{total:,.2f} €".replace(",", " "))

# --- Graphique par catégorie ---
st.subheader("📊 Dépenses par catégorie")
if not df.empty:
    by_cat = df.groupby("category", as_index=False)["amount"].sum().set_index("category")
    st.bar_chart(by_cat)  # Streamlit dessine automatiquement
else:
    st.info("Ajoutez des dépenses pour voir le graphique.")


