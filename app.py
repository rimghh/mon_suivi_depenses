import os
from datetime import date
import pandas as pd
import streamlit as st

# ==================== CONFIG ====================
st.set_page_config(
    page_title="💶 SmartWallet",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSV_PATH = "expenses.csv"
USERS_CSV = "users.csv"
REVENUS_CSV = "revenus.csv"
# ==================== FONCTIONS ====================
@st.cache_data
def load_expenses():
    if os.path.exists(CSV_PATH):
        # on force les types pour éviter les surprises
        return pd.read_csv(CSV_PATH, dtype={"date": "string", "category": "string", "amount": "float64", "desc": "string"})
    # DataFrame vide typé
    return pd.DataFrame({
        "date": pd.Series(dtype="string"),
        "category": pd.Series(dtype="string"),
        "amount": pd.Series(dtype="float"),
        "desc": pd.Series(dtype="string"),
    })

def save_expenses(df: pd.DataFrame):
    df.to_csv(CSV_PATH, index=False)

def register_user(email, pwd, name, phone):
    # version pédagogique (mot de passe en clair) — OK pour projet débutant
    if not os.path.exists(USERS_CSV):
        pd.DataFrame(columns=["email", "pwd", "name", "phone"]).to_csv(USERS_CSV, index=False)
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
    user = users[(users["email"] == email) & (users["pwd"] == pwd)]
    if not user.empty:
        return user.iloc[0].to_dict()
    return None
def load_revenus():
    if os.path.exists(REVENUS_CSV):
        return pd.read_csv(REVENUS_CSV)
    return pd.DataFrame(columns=["date", "type", "amount", "desc"])

def save_revenus(df):
    df.to_csv(REVENUS_CSV, index=False)
# ==================== DONNÉES ====================
expenses_df = load_expenses()

# ==================== NAVBAR (simple CSS facultatif) ====================
st.markdown("""
<style>
.nav { background-color:#a8e6cf; padding:10px; border-radius:10px; display:flex; justify-content:space-around; align-items:center; font-weight:600; }
</style>
""", unsafe_allow_html=True)

tabs = ["⚙️ Compte" , "Budget total" , "💼 Revenus", "📋 Suivi des dépenses" , "💰 Placements"]
selected_tab = st.radio("Navigation", tabs, horizontal=True, label_visibility="collapsed", key="menu")
st.markdown(f"<div class='nav'><b>{selected_tab}</b></div>", unsafe_allow_html=True)

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
            st.success("Compte créé. Connectez-vous ci-dessous.") if ok else st.error("Cet email est déjà utilisé.")

    else:
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

    if st.session_state.get("logged_in", False):
        st.subheader("📄 Mes données personnelles")
        user = st.session_state.get("user_data", {})
        st.write(f"**Nom :** {user.get('name','')}")
        st.write(f"**Email :** {user.get('email','')}")
        st.write(f"**Téléphone :** {user.get('phone','')}")

# ==================== REVENUS ====================
elif selected_tab == "💼 Revenus":
    st.title("💼 Revenus")
    st.write("Saisissez vos revenus et consultez l’historique.")

    # --- Chargement des revenus ---
    if "revenus" not in st.session_state:
        rev_df = load_revenus()  # chargement du CSV si dispo
        st.session_state["revenus"] = rev_df
    else:
        rev_df = st.session_state["revenus"]

    # --- Saisie d’un nouveau revenu ---
    with st.form("ajout_revenu"):
        source = st.text_input("Source du revenu (ex : Salaire, Freelance...)")
        montant = st.number_input("Montant (€)", min_value=0.0, step=10.0)
        date_revenu = st.date_input("Date du revenu")
        type_revenu = st.selectbox("Type de revenu", ["Fixe", "Variable"])

        submit_revenu = st.form_submit_button("Ajouter")

        if submit_revenu:
            if source and montant > 0:
                nouveau_revenu = {
                    "source": source,
                    "amount": montant,
                    "date": str(date_revenu),
                    "type": type_revenu
                }
                # Ajout dans le DataFrame
                st.session_state["revenus"] = pd.concat(
                    [st.session_state["revenus"], pd.DataFrame([nouveau_revenu])],
                    ignore_index=True
                )

                # Sauvegarde dans le CSV
                save_revenus(st.session_state["revenus"])
                st.success("✅ Revenu ajouté avec succès !")
            else:
                st.warning("Veuillez saisir une source et un montant valide.")

    # --- Affichage des revenus existants ---
    if not st.session_state["revenus"].empty:
        st.subheader("Historique des revenus")
        st.dataframe(st.session_state["revenus"])
    else:
     st.info("Aucun revenu enregistré pour le moment.")

# ==================== SUIVI DES DÉPENSES ====================
elif selected_tab == "📋 Suivi des dépenses":
    st.title("💰 Money Tracker — Suivi de vos dépenses")

    c1, c2 = st.columns(2)
    with c1:
        d = st.date_input("Date", value=date.today(), key="dep_date")
        cat = st.selectbox("Catégorie", ["Alimentation", "Transport", "Logement", "Shopping", "Autres"], key="dep_cat")
    with c2:
        amount = st.number_input("Montant (€)", min_value=0.0, step=1.0, key="dep_amount")
        desc = st.text_input("Description (facultatif)", key="dep_desc")

    if st.button("➕ Ajouter la dépense"):
        if amount > 0:
            new_row = {"date": d.isoformat(), "category": cat, "amount": float(amount), "desc": desc}
            updated = pd.concat([expenses_df, pd.DataFrame([new_row])], ignore_index=True)
            save_expenses(updated)
            st.cache_data.clear()  # pour recharger les données fraîches
            st.success("✅ Dépense enregistrée !")
            expenses_df = load_expenses()
        else:
            st.warning("⚠️ Entrez un montant > 0")

    st.markdown("---")
    st.subheader("📋 Mes dépenses")
    expenses_df = load_expenses()
    st.dataframe(expenses_df, use_container_width=True)
    total_depenses = float(expenses_df["amount"].sum()) if not expenses_df.empty else 0.0
    st.metric("💵 Total des dépenses", f"{total_depenses:,.2f} €".replace(",", " "))

    st.subheader("📈 Dépenses par mois")
    if not expenses_df.empty:
        tmp = expenses_df.copy()
        tmp["date"] = pd.to_datetime(tmp["date"], errors="coerce")
        monthly = (tmp.set_index("date")
                      .groupby(pd.Grouper(freq="M"))["amount"]
                      .sum()
                      .reset_index())
        monthly.rename(columns={"date": "Mois", "amount": "Montant (€)"}, inplace=True)
        st.bar_chart(monthly, x="Mois", y="Montant (€)", use_container_width=True)
    else:
        st.info("Aucune donnée pour le moment.")
 #==============placements==============
elif selected_tab == "💰 Placements":
    st.title("💰 Placements")
    st.write("Calculez l'intérêt reçu pour un placement.")

    principal = st.number_input("Montant placé (€)", min_value=0.0, step=10.0, key="principal")
    annual_rate = st.number_input("Taux annuel (%)", min_value=0.0, step=0.1, key="rate")
    period = st.selectbox("Période de calcul", ["Mensuel", "Annuel"])

    # --- Fonction pour calculer les intérêts ---
    def compute_interest(principal, annual_rate, period):
        r = annual_rate / 100
        if period == "Mensuel":
            monthly = principal * (r / 12)
            yearly = principal * r
        else:  # Annuel
            yearly = principal * r
            monthly = yearly / 12
        return {"monthly": monthly, "yearly": yearly}

    # --- Bouton pour calculer ---
    if st.button("Calculer l'intérêt"):
        res = compute_interest(principal, annual_rate, period)
        st.success(f"Intérêt mensuel estimé : {res['monthly']:.2f} €")
        st.info(f"Intérêt annuel estimé : {res['yearly']:.2f} €")


#============== budget===========
elif selected_tab == "Budget total":
    st.header("💰 Gestion du Budget")

    # --- Récupération des données existantes ---
    # Revenus
    if "revenus" in st.session_state:
        rev_df = st.session_state["revenus"]
        total_revenu = float(rev_df["amount"].sum()) if not rev_df.empty else 0.0
    else:
        total_revenu = 0.0

    # Dépenses
    total_depenses = float(expenses_df["amount"].sum()) if not expenses_df.empty else 0.0

    # Placements (on peut stocker dans session_state depuis l'onglet Placements)
    montant_placement = float(st.session_state.get("placements", 0.0))

    # --- Calcul du budget restant ---
    budget_restant = total_revenu - total_depenses - montant_placement

    # --- Vérification logique ---
    if total_revenu == 0:
        st.info("🧮 Ajoutez des revenus pour afficher le budget.")
    elif budget_restant < 0:
        st.warning("⚠️ Vos dépenses et placements dépassent vos revenus !")
    else:
        # --- Résumé ---
        st.subheader("Résumé du budget")
        st.write(f"**Revenus :** {total_revenu:.2f} €")
        st.write(f"**Dépenses :** {total_depenses:.2f} €")
        st.write(f"**Placements :** {montant_placement:.2f} €")
        st.write(f"**Budget restant :** {budget_restant:.2f} €")

        # --- Graphe circulaire ---
        import matplotlib.pyplot as plt

        labels = ['Dépenses', 'Placements', 'Budget restant']
        values = [total_depenses, montant_placement, budget_restant]

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

       