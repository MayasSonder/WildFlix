import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
from streamlit_authenticator import Authenticate
from recommandation import recommander, df

# Détection query param AVANT tout
if "go" in st.query_params and st.query_params["go"] == "login":
    st.session_state.page = "login"
    st.query_params.clear()
    st.rerun()

# Si cookie actif, on redirige vers app
if st.session_state.get("authentication_status") and st.session_state.get("page") == "accueil":
    st.session_state.page = "app"

st.set_page_config(layout="wide")

st.markdown("""
<style>
    .block-container { padding: 0 !important; max-width: 100% !important; }
    footer { display: none !important; }
    header { display: none !important; }
    [data-testid="stAppViewContainer"] { padding: 0 !important; }
    [data-testid="stVerticalBlock"] { gap: 0 !important; padding: 0 !important; }
    iframe { display: block; border: none; }
    [data-testid="stSidebar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
posters = df["Poster"].dropna().head(14).tolist()
poster_imgs = "".join([f'<img src="{url}">' for url in posters * 2])

config = {
    'credentials': {
        'usernames': {
            'utilisateur': {'name': 'Utilisateur', 'password': 'utilisateurMDP'},
            'admin': {'name': 'Admin', 'password': 'adminMDP'}
        }
    },
    'cookie': {'name': 'moviemind_cookie', 'key': 'moviemind_key', 'expiry_days': 30}
}

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

if "page" not in st.session_state:
    st.session_state.page = "accueil"

# ---- PAGE ACCUEIL ----
if st.session_state.page == "accueil":
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
    @keyframes scroll {{
        0%   {{ transform: translateX(0); }}
        100% {{ transform: translateX(-50%); }}
    }}
    .posters-track {{
        display: flex;
        animation: scroll 25s linear infinite;
        width: max-content;
        position: fixed;
        top: 0; left: 0;
        height: 100vh;
        z-index: 0;
    }}
    .posters-track img {{
        height: 100vh;
        width: 300px;
        object-fit: cover;
        margin-right: 5px;
    }}
    .overlay {{
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        background: rgba(0,0,0,0.6);
        z-index: 1;
    }}
    .title {{
        position: fixed;
        top: 35%;
        left: 50%;
        transform: translateX(-50%);
        color: #FFE81F;
        font-size: 110px;
        font-family: 'Bebas Neue', sans-serif;
        text-shadow: 0 0 20px #FFE81F, 0 0 40px #FFE81F88;
        letter-spacing: 8px;
        z-index: 2;
        white-space: nowrap;
    }}
    div.stButton {{
        position: fixed;
        top: 62%;
        left: 50%;
        transform: translateX(-50%);
        z-index: 3;
        width: auto !important;
    }}
    div.stButton > button {{
        background-color: #FFE81F !important;
        color: black !important;
        font-size: 22px !important;
        font-weight: bold !important;
        font-family: 'Bebas Neue', sans-serif !important;
        letter-spacing: 3px !important;
        padding: 15px 60px !important;
        border: none !important;
        border-radius: 3px !important;
        cursor: pointer !important;
        width: auto !important;
        white-space: nowrap !important;
    }}
    div.stButton > button:hover {{ background-color: white !important; }}
    </style>
    <div class="posters-track">{poster_imgs}</div>
    <div class="overlay"></div>
    <div class="title">MOVIE MIND</div>
    """, unsafe_allow_html=True)

    if st.button("COMMENCER"):
        st.session_state.page = "login"
        st.rerun()

# ---- PAGE LOGIN ----
elif st.session_state.page == "login":
    st.markdown("""
    <style>
        .block-container { padding: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)
    st.title("🔐 Connexion")
    authenticator.login()
    if st.session_state.get("authentication_status") is False:
        st.error("❌ Identifiants incorrects")
    if st.session_state.get("authentication_status"):
        st.session_state.page = "app"
        st.rerun()
    if st.button("⬅️ Retour à l'accueil"):
        st.session_state.page = "accueil"
        st.rerun()

# ---- APP PRINCIPALE ----
elif st.session_state.page == "app" and st.session_state.get("authentication_status"):
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: block !important; }
        .block-container { padding: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.title("🎬 MovieMind")
        page = st.radio("", [
            "🎬 Recommandations",
            "🔍 Explorer",
            "👤 Mon compte"
        ])

    if page == "🎬 Recommandations":
        st.title("🎬 Recommandations")
        film_choisi = st.selectbox("Choisis un film", df["Title"].dropna().tolist())
        if film_choisi:
            film = df[df["Title"] == film_choisi].iloc[0]
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(film["Poster"], width=200)
            with col2:
                st.write(f"**Genre :** {film['Genre_1']}")
                st.write(f"**Note IMDb :** {film['imdbRating']}")
                st.write(f"**Durée :** {film['Runtime']} min")
                st.write(f"**Oscars gagnés :** {film['Oscars']}")
                st.write(f"**Nominations :** {film['Nominations']}")
                st.write(f"**Synopsis :** {film['Plot']}")
            st.subheader("🎬 Films similaires :")
            reco = recommander(film_choisi)
            cols = st.columns(5)
            for i, titre in enumerate(reco):
                film_reco = df[df["Title"] == titre].iloc[0]
                with cols[i]:
                    st.image(film_reco["Poster"], width=130)
                    st.caption(titre)

    elif page == "🔍 Explorer":
        st.title("🔍 Explorer")
        genre = st.selectbox("Filtrer par genre", ["Tous"] + sorted(df["Genre_1"].dropna().unique().tolist()))

        if genre == "Tous":
            films_filtres = df.dropna(subset=["Poster"]).sort_values("Released_year", ascending=False)
        else:
            films_filtres = df[df["Genre_1"] == genre].dropna(subset=["Poster"]).sort_values("Released_year", ascending=False)

        cols = st.columns(4)
        for i, (_, film) in enumerate(films_filtres.iterrows()):
            with cols[i % 4]:
                st.markdown(f"""
                <div style="position:relative; margin-bottom:15px;">
                    <img src="{film['Poster']}" style="width:100%; border-radius:8px;">
                    <div style="position:absolute; bottom:8px; left:8px; background:#27ae60; color:white; 
                                font-weight:bold; padding:3px 8px; border-radius:5px; font-size:14px;">
                        {film['imdbRating']}
                    </div>
                </div>
                <p style="margin:0; font-size:13px; color:white;">{film['Title']}</p>
                <p style="margin:0; font-size:11px; color:gray;">{film['Genre_1']}</p>
                """, unsafe_allow_html=True)

    elif page == "👤 Mon compte":
        st.title(f"Bienvenue {st.session_state['name']} ! 👋")
        authenticator.logout("🚪 Déconnexion")
        if not st.session_state.get("authentication_status"):
            st.session_state.page = "accueil"
            st.rerun()