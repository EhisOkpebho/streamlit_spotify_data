import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analyse musicale", layout="wide")

page = st.sidebar.selectbox("Navigation", ["Analyse des facteurs de popularité", "Recherche d'artistes par genre"])

uploaded_file = st.file_uploader("Téléchargez votre fichier CSV", type="csv")

column_translation = {
    'track_id': 'ID de la piste',
    'artists': 'Artistes',
    'album_name': "Nom de l'album",
    'track_name': 'Nom de la piste',
    'popularity': 'Popularité',
    'duration_ms': 'Durée (ms)',
    'explicit': 'Explicite',
    'danceability': 'Danseabilité',
    'energy': 'Énergie',
    'key': 'Clé',
    'loudness': 'Sonie',
    'mode': 'Mode',
    'speechiness': 'Parlabilité',
    'acousticness': 'Acoustique',
    'instrumentalness': 'Instrumentalité',
    'liveness': 'Vivacité',
    'valence': 'Valence',
    'tempo': 'Tempo',
    'time_signature': 'Signature temporelle',
    'track_genre': 'Genre musical'
}

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    df.rename(columns=column_translation, inplace=True)

    if page == "Analyse des facteurs de popularité":
        st.title("Analyse des facteurs de popularité des titres musicaux")
        st.write("Aperçu des données :", df.head(10))
        st.write("Colonnes disponibles :", df.columns.tolist())

        st.sidebar.header("Filtrer les colonnes")
        selected_columns = st.sidebar.multiselect("Sélectionnez les colonnes à afficher", df.columns, default=df.columns)
        st.write("Colonnes sélectionnées :", df[selected_columns].head())

        st.subheader("Popularité vs Danseabilité")
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x='Danseabilité', y='Popularité', ax=ax, alpha=0.7)
        plt.title("Popularité en fonction de la danseabilité")
        st.pyplot(fig)

        st.subheader("Distribution des niveaux de popularité")
        fig, ax = plt.subplots()
        sns.histplot(df['Popularité'], bins=20, kde=True, ax=ax)
        plt.title("Histogramme des niveaux de popularité")
        st.pyplot(fig)

        st.subheader("Popularité moyenne par genre musical")
        if 'Genre musical' in df.columns:
            genre_popularity = df.groupby('Genre musical')['Popularité'].mean().sort_values(ascending=False)
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

    elif page == "Recherche d'artistes par genre":
        st.title("Recherche d'artistes dominants par genre")
        if 'Genre musical' in df.columns and 'Artistes' in df.columns:
            selected_genre = st.selectbox("Choisissez un genre", df['Genre musical'].unique())
            genre_data = df[df['Genre musical'] == selected_genre]

            top_artists = genre_data.groupby('Artistes')['Popularité'].mean().sort_values(ascending=False).head(10)

            st.subheader(f"Artistes les plus populaires dans le genre : {selected_genre}")
            st.table(top_artists)
        else:
            st.warning("Les colonnes 'Genre musical' et 'Artistes' sont nécessaires pour cette analyse. Veuillez vérifier votre fichier CSV.")
else:
    st.info("Téléchargez un fichier CSV pour commencer l'analyse.")
    
