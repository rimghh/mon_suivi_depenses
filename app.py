import os
from datetime import date
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="💰 Money Tracker",
    layout="wide",  # Largeur totale de la page
    initial_sidebar_state="expanded"
)

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

# --- Mise en page principale : 2 colonnes ---
col_menu, col_main = st.columns([1, 3])  # menu = 1/4, contenu = 3/4

# ==================== MENU LATÉRAL ====================
with col_menu:
    st.header("🏦 Espace personnel")
    st.write("Naviguez entre les différentes sections :")

    section = st.radio(
        "Choisissez une section :",
        ["📋 Suivi des dépenses", "📈 Graphique mensuel", "💸 Prêts", "💰 Placements"]
    )
st.markdown("---")
st.info("💡 Astuce : ajoutez vos dépenses dans la section principale.")
# ==================== CONTENU PRINCIPAL ====================
with col_main:

    if section == "📋 Suivi des dépenses":
        st.title("💰 Money Tracker — Suivi de vos dépenses")

        col1, col2 = st.columns(2)
        with col1:
            d = st.date_input("Date", value=date.today())
            cat = st.selectbox("Catégorie", ["Alimentation", "Transport", "Logement", "Shopping", "Autres"])
        with col2:
            amount = st.number_input("Montant (€)", min_value=0.0, step=1.0)
            desc = st.text_input("Description (facultatif)")

        if st.button("➕ Ajouter la dépense"):
            if amount > 0:
                new_row = {"date": d.isoformat(), "category": cat, "amount": amount, "desc": desc}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_csv(df)
                st.success("✅ Dépense enregistrée !")
            else:
                st.warning("⚠️ Entrez un montant > 0")

        st.markdown("---")
        st.subheader("📋 Mes dépenses")
        st.dataframe(df, width='stretch')

        total = float(df["amount"].sum()) if not df.empty else 0.0
        st.metric("💵 Total des dépenses", f"{total:,.2f} €".replace(",", " "))

    elif section == "📈 Graphique mensuel":
        st.title("📈 Graphique mensuel des dépenses")
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            df["month"] = df["date"].dt.to_period("M")
            monthly = df.groupby("month")["amount"].sum()
            st.bar_chart(monthly)
        else:
            st.info("Aucune donnée pour le moment.")

    elif section == "💸 Prêts":
        st.title("💸 Gestion des prêts")
        st.write("💡 Ici, vous pourrez ajouter ou suivre vos crédits (bancaires, personnels, etc.)")
        st.warning("Section en construction 🚧")

    elif section == "💰 Placements":
        st.title("💰 Placements et investissements")
        st.write("💡 Suivez vos placements sur livret, actions ou crypto ici.")
        st.warning("Section en construction 🚧")





