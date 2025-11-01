import os
from datetime import date
import pandas as pd
import streamlit as st
# ==================== CONFIG ====================
st.set_page_config(
    page_title="💰 Money Tracker",
    layout="wide",
    initial_sidebar_state="expanded"
)

CSV_PATH = "expenses.csv"
USERS_CSV = "users.csv"

# ==================== FONCTIONS ====================
# CSV Dépenses
def load_csv():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    return pd.DataFrame(columns=["date", "category", "amount", "desc"])

def save_csv(df):
    df.to_csv(CSV_PATH, index=False)

# CSV Utilisateurs
def register_user(email, pwd, name, phone):
    if not os.path.exists(USERS_CSV):
        pd.DataFrame(columns=["email","pwd","name","phone"]).to_csv(USERS_CSV,index=False)
    users = pd.read_csv(USERS_CSV)
    if email in users["email"].values:
        return False
    new_user = pd.DataFrame([{"email": email, "pwd": pwd, "name": name, "phone": phone}])
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv(USERS_CSV, index=False)
    return True

def authenticate(email, pwd):
    if not os.path.exists(USERS_CSV):
        return None
    users = pd.read_csv(USERS_CSV)
    user = users[(users["email"]==email) & (users["pwd"]==pwd)]
    if not user.empty:
        return user.iloc[0].to_dict()
    return None

# Calcul intérêts
def compute_interest(principal, annual_rate, period):
    r = annual_rate / 100.0
    if period == "Mensuel":
        monthly_interest = principal * (r / 12)
        return {"monthly": monthly_interest, "yearly": monthly_interest * 12}
    else:
        yearly_interest = principal * r
        return {"monthly": yearly_interest / 12, "yearly": yearly_interest}

# ==================== DONNÉES ====================
df = load_csv()

# ==================== BARRE DE NAVIGATION HAUT ====================
st.markdown("""
    <style>
    .nav {
        background-color: #a8e6cf;
        padding: 10px;
        border-radius: 10px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        font-weight: 600;
    }
    .nav-item {
        cursor: pointer;
        padding: 8px 16px;
        border-radius: 6px;
        transition: background 0.2s;
    }
    .nav-item:hover {
        background-color: #81c784;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Crée une barre de navigation
tabs = ["⚙️ Compte" , "Budget total disponible" , "💼 Revenus" , "📋 Suivi des dépenses", "💰 Placements"]
selected_tab = st.radio("Navigation", tabs, horizontal=True, label_visibility="collapsed", key="menu")

st.markdown(f"<div class='nav'> <b>{selected_tab}</b></div>", unsafe_allow_html=True)


        
# ==================== COMPTE ====================
if selected_tab == "⚙️ Compte":
    st.title("⚙️ Mon compte")
    choice = st.selectbox("Connexion / Inscription", ["Se connecter", "S'enregistrer"])
    
    if choice == "S'enregistrer":
        st.subheader("Créer un nouveau compte")
        new_email = st.text_input("Email", key="reg_email")
        new_pwd = st.text_input("Mot de passe", type="password", key="reg_pwd")
        new_name = st.text_input("Nom complet", key="reg_name")
        new_phone = st.text_input("Téléphone", key="reg_phone")
        
        if st.button("Créer un compte", key="btn_register"):
            ok = register_user(new_email, new_pwd, new_name, new_phone)
            if ok:
                st.success("Compte créé. Connectez-vous ci-dessous.")
            else:
                st.error("Cet email est déjà utilisé.")
    
    else:  # Se connecter
        st.subheader("Se connecter")
        email = st.text_input("Email", key="login_email")
        pwd = st.text_input("Mot de passe", type="password", key="login_pwd")
        
        if st.button("Se connecter", key="btn_login"):
            user_data = authenticate(email, pwd)
            if user_data:
                st.session_state.logged_in = True
                st.session_state.user_data = user_data
                st.success(f"Connecté(e) : {email}")
            else:
                st.error("Email ou mot de passe incorrect.")
    
    # Affichage des données personnelles si connecté
    if st.session_state.get("logged_in", False):
        st.subheader("📄 Mes données personnelles")
        user = st.session_state.get("user_data", {})
        st.write(f"**Nom :** {user.get('name','')}")
        st.write(f"**Email :** {user.get('email','')}")
        st.write(f"**Téléphone :** {user.get('phone','')}")

# ==================== SUIVI DES DÉPENSES ====================
elif selected_tab == "📋 Suivi des dépenses":
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

# ==================== GRAPHIQUE ====================

    st.title("📈 Graphique mensuel des dépenses")
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.to_period("M")
        monthly = df.groupby("month")["amount"].sum()
        st.bar_chart(monthly)
    else:
        st.info("Aucune donnée pour le moment.")

# ==================== PLACEMENTS ====================
elif selected_tab == "💰 Placements":
    st.title("💰 Placements")
    st.write("Calculez l'intérêt reçu pour un placement.")
    principal = st.number_input("Montant placé (€)", min_value=0.0, step=10.0, key="principal")
    annual_rate = st.number_input("Taux annuel (%)", min_value=0.0, step=0.1, key="rate")
    period = st.selectbox("Période de calcul", ["Mensuel", "Annuel"])

    if st.button("Calculer l'intérêt"):
        res = compute_interest(principal, annual_rate, period)
        st.success(f"Intérêt mensuel estimé : {res['monthly']:.2f} €")
        st.info(f"Intérêt annuel estimé : {res['yearly']:.2f} €")

# ==================== REVENUS ====================
elif selected_tab == "💼 Revenus":
    st.title("💰 Gestion des revenus")

    # Initialisation si vide
    if "revenus" not in st.session_state:
        st.session_state["revenus"] = pd.DataFrame(columns=["date", "type", "amount", "desc"])

    revenus_df = st.session_state["revenus"]

    # --- Formulaire d'ajout ---
    st.subheader("➕ Ajouter un revenu")
    col1, col2 = st.columns(2)
    with col1:
        date_rev = st.date_input("Date", value=date.today())
        type_rev = st.selectbox("Type de revenu", ["Salaire", "Prime", "Cadeau", "Vente", "Autre"])
    with col2:
        montant_rev = st.number_input("Montant (€)", min_value=0.0, step=10.0)
        desc_rev = st.text_input("Description (facultatif)")

    if st.button("Ajouter le revenu"):
        if montant_rev > 0:
            new_rev = pd.DataFrame([{
                "date": date_rev.isoformat(),
                "type": type_rev,
                "amount": montant_rev,
                "desc": desc_rev
            }])
            st.session_state["revenus"] = pd.concat([revenus_df, new_rev], ignore_index=True)
            st.success("✅ Revenu ajouté avec succès !")
        else:
            st.warning("⚠️ Entrez un montant supérieur à 0 €")

    # --- Historique ---
    st.markdown("---")
    st.subheader("📋 Historique des revenus")

    if st.session_state["revenus"].empty:
        st.info("Aucun revenu enregistré pour le moment.")
    else:
        df = st.session_state["revenus"]
        st.dataframe(df, use_container_width=True)
        total_rev = df["amount"].sum()
        st.metric("💵 Total des revenus enregistrés", f"{total_rev:,.2f} €".replace(",", " "))

        # --- Graphiques ---
        st.subheader("📊 Visualisation")
        df["date"] = pd.to_datetime(df["date"])
        by_type = df.groupby("type")["amount"].sum()
        st.bar_chart(by_type, use_container_width=True)
        by_date = df.groupby("date")["amount"].sum()
        st.line_chart(by_date, use_container_width=True)
