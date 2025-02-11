import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Analyse des Maladies Cardiaques", layout="wide")
st.title("💉 Analyse Innovante des Maladies Cardiaques")

# Charger les données
@st.cache_data
def load_data():
    data = pd.read_csv("heart.csv")  # Remplacez par le chemin de votre fichier si nécessaire
    return data

data = load_data()

# Barre latérale : Contrôles interactifs
st.sidebar.header("🛠️ Contrôles Interactifs")
age_filter = st.sidebar.slider("🎂 Filtrer par Âge", int(data['age'].min()), int(data['age'].max()), (40, 60))
chol_filter = st.sidebar.slider("🍔 Filtrer par Cholestérol", int(data['chol'].min()), int(data['chol'].max()), (200, 300))
target_filter = st.sidebar.radio("🩺 Filtrer par Présence de Maladie", ("Tous", "Pas de Maladie", "Maladie"))

# Filtrer les données
filtered_data = data[(data['age'] >= age_filter[0]) & (data['age'] <= age_filter[1])]
filtered_data = filtered_data[(filtered_data['chol'] >= chol_filter[0]) & (filtered_data['chol'] <= chol_filter[1])]

if target_filter == "Pas de Maladie":
    filtered_data = filtered_data[filtered_data['target'] == 0]
elif target_filter == "Maladie":
    filtered_data = filtered_data[filtered_data['target'] == 1]

# Afficher les statistiques
st.markdown("## 📊 Statistiques Clés")
st.metric(label="Nombre de Patients", value=len(filtered_data))
st.metric(label="Âge Moyen", value=round(filtered_data['age'].mean(), 1))
st.metric(label="Cholestérol Moyen", value=round(filtered_data['chol'].mean(), 1))

# Graphiques interactifs
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎨 Distribution de l'Âge")
    fig_age = px.histogram(filtered_data, x='age', nbins=20, title="Distribution de l'Âge", color_discrete_sequence=['#636EFA'])
    st.plotly_chart(fig_age, use_container_width=True)

with col2:
    st.markdown("### 🎨 Distribution du Cholestérol")
    fig_chol = px.histogram(filtered_data, x='chol', nbins=20, title="Distribution du Cholestérol", color_discrete_sequence=['#EF553B'])
    st.plotly_chart(fig_chol, use_container_width=True)

# Relation entre variables
st.markdown("## 🔍 Analyse des Relations entre Variables")
fig_scatter = px.scatter(
    filtered_data, x='age', y='chol', color='target',
    title="Relation entre Âge et Cholestérol",
    color_discrete_map={0: '#636EFA', 1: '#EF553B'},
    labels={"target": "Présence de Maladie"}
)
st.plotly_chart(fig_scatter, use_container_width=True)

# Téléchargement des données filtrées
st.markdown("### 📥 Télécharger les Données Filtrées")
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered_data)
st.download_button(
    label="📂 Télécharger en CSV",
    data=csv,
    file_name="donnees_filtrees.csv",
    mime="text/csv"
)

# Pied de page
st.markdown("---")
