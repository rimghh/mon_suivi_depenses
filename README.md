# SmartWallet 💶
# 💰 Mon Suivi de Dépenses - Application Streamlit

## 📋 Description

Cette application permet de **gérer facilement ses revenus, dépenses et budget personnel** grâce à une interface interactive développée avec **Streamlit**.  
Elle offre la possibilité de suivre les transactions, visualiser les statistiques financières et enregistrer les données de manière simple et efficace.

---

##  Fonctionnalités principales

- Gestion **multi-utilisateur** avec connexion et inscription.- 🧾 **Suivi des dépenses** : ajout, modification et suppression de dépenses.  
- **Gestion des revenus** : enregistrement et visualisation des sources de revenus.  
- **Analyse budgétaire** : affichage de graphiques (par catégorie, par mois, etc.).  
- **Budget personnalisé** : suivi de l’écart entre le budget prévu et réel.  
- **Sauvegarde locale** des données (via fichiers CSV).  
- **Interface intuitive** avec navigation entre plusieurs sections :
  - compte
  - Revenus
  - Dépenses
  - Budget

---

## 🛠️ Installation

1. Cloner le projet
   ```bash
   git clone https://github.com/ton-utilisateur/mon_suivi_depenses.git
   cd mon_suivi_depenses
   
2. Créer un environnement virtuel et l’activer :
python3 -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate


3. Installer les dépendances :
pip install -r requirements.txt


4. Lancer l’application :
streamlit run app.py

📋 **Utilisation**

Créer un compte ou se connecter.

Ajouter des revenus en précisant la source, le montant et le type.

Ajouter des dépenses avec la catégorie, le montant et éventuellement une description.

Consulter le budget pour voir le total des revenus, des dépenses et le budget restant, avec visualisation graphique.

L’application filtre automatiquement les données pour chaque utilisateur connecté.
