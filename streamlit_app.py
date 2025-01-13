import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Analyse des facteurs de popularité des titres musicaux")

uploaded_file = st.file_uploader("Téléchargez votre fichier CSV", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("Aperçu des données :", df.head())
    st.write("Colonnes disponibles :", df.columns.tolist())

    st.sidebar.header("Filtrer les colonnes")
    selected_columns = st.sidebar.multiselect("Sélectionnez les colonnes à afficher", df.columns, default=df.columns)
    st.write("Colonnes sélectionnées :", df[selected_columns].head())

    st.subheader("Popularité vs Danseabilité")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x='danceability', y='popularity', ax=ax, alpha=0.7)
    plt.title("Popularité en fonction de la danseabilité")
    st.pyplot(fig)

    st.subheader("Distribution des niveaux de popularité")
    fig, ax = plt.subplots()
    sns.histplot(df['popularity'], bins=20, kde=True, ax=ax)
    plt.title("Histogramme des niveaux de popularité")
    st.pyplot(fig)

    st.subheader("Popularité moyenne par genre musical")
    if 'track_genre' in df.columns:
        genre_popularity = df.groupby('track_genre')['popularity'].mean().sort_values(ascending=False)
        st.bar_chart(genre_popularity)

    st.subheader("Corrélations entre les variables")
    numeric_cols = df.select_dtypes(include=['float64', 'int64'])
    if not numeric_cols.empty:
        corr_matrix = numeric_cols.corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        plt.title("Matrice de corrélation")
        st.pyplot(fig)
    else:
        st.warning("Aucune colonne numérique disponible pour calculer la corrélation.")
else:
    st.info("Téléchargez un fichier CSV pour commencer l'analyse.")
