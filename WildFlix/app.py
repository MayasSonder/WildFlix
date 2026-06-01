import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
from streamlit_authenticator import Authenticate
from recommandation import recommander, df

# ---- DICTIONNAIRE DE TRADUCTIONS ----
LANG = {
    "🇫🇷 Français": {
        "recommandations": "🎬 Recommandations",
        "explorer": "🔍 Explorer",
        "mon_compte": "👤 Mon compte",
        "choisis_film": "Choisis un film",
        "genre": "Genre",
        "tous": "Tous",
        "note_min": "Note IMDb minimum",
        "duree_max": "Durée max (min)",
        "films_trouves": "films trouvés",
        "films_similaires": "🎬 Films similaires :",
        "surprise": "🎲 Surprends-moi !",
        "bienvenue": "Bienvenue",
        "deconnexion": "🚪 Déconnexion",
        "connexion": "🔐 Connexion",
        "commencer": "COMMENCER",
        "retour": "⬅️ Retour à l'accueil",
        "genre_label": "Genre",
        "duree": "Durée",
        "note_imdb": "Note IMDb",
        "oscars": "Oscars gagnés",
        "nominations": "Nominations",
        "synopsis": "Synopsis",
        "erreur_login": "❌ Identifiants incorrects",
        "on_te_propose": "🎬 On te propose :",
    },
    "🇬🇧 English": {
        "recommandations": "🎬 Recommendations",
        "explorer": "🔍 Explore",
        "mon_compte": "👤 My account",
        "choisis_film": "Choose a movie",
        "genre": "Genre",
        "tous": "All",
        "note_min": "Minimum IMDb rating",
        "duree_max": "Max duration (min)",
        "films_trouves": "movies found",
        "films_similaires": "🎬 Similar movies:",
        "surprise": "🎲 Surprise me!",
        "bienvenue": "Welcome",
        "deconnexion": "🚪 Logout",
        "connexion": "🔐 Login",
        "commencer": "START",
        "retour": "⬅️ Back to home",
        "genre_label": "Genre",
        "duree": "Duration",
        "note_imdb": "IMDb Rating",
        "oscars": "Oscars won",
        "nominations": "Nominations",
        "synopsis": "Synopsis",
        "erreur_login": "❌ Wrong credentials",
        "on_te_propose": "🎬 We suggest:",
    },
    "🇪🇸 Español": {
        "recommandations": "🎬 Recomendaciones",
        "explorer": "🔍 Explorar",
        "mon_compte": "👤 Mi cuenta",
        "choisis_film": "Elige una película",
        "genre": "Género",
        "tous": "Todos",
        "note_min": "Nota IMDb mínima",
        "duree_max": "Duración máx (min)",
        "films_trouves": "películas encontradas",
        "films_similaires": "🎬 Películas similares:",
        "surprise": "🎲 ¡Sorpréndeme!",
        "bienvenue": "Bienvenido",
        "deconnexion": "🚪 Cerrar sesión",
        "connexion": "🔐 Iniciar sesión",
        "commencer": "COMENZAR",
        "retour": "⬅️ Volver al inicio",
        "genre_label": "Género",
        "duree": "Duración",
        "note_imdb": "Nota IMDb",
        "oscars": "Oscars ganados",
        "nominations": "Nominaciones",
        "synopsis": "Sinopsis",
        "erreur_login": "❌ Credenciales incorrectas",
        "on_te_propose": "🎬 Te proponemos:",
    },
    "🇸🇦 العربية": {
        "recommandations": "🎬 توصيات",
        "explorer": "🔍 استكشاف",
        "mon_compte": "👤 حسابي",
        "choisis_film": "اختر فيلماً",
        "genre": "النوع",
        "tous": "الكل",
        "note_min": "تقييم IMDb الأدنى",
        "duree_max": "المدة القصوى (دقيقة)",
        "films_trouves": "أفلام موجودة",
        "films_similaires": "🎬 أفلام مشابهة:",
        "surprise": "🎲 فاجئني!",
        "bienvenue": "مرحباً",
        "deconnexion": "🚪 تسجيل الخروج",
        "connexion": "🔐 تسجيل الدخول",
        "commencer": "ابدأ",
        "retour": "⬅️ العودة",
        "genre_label": "النوع",
        "duree": "المدة",
        "note_imdb": "تقييم IMDb",
        "oscars": "جوائز أوسكار",
        "nominations": "ترشيحات",
        "synopsis": "ملخص",
        "erreur_login": "❌ بيانات الدخول غير صحيحة",
        "on_te_propose": "🎬 نقترح عليك:",
    },
    "🇩🇪 Deutsch": {
        "recommandations": "🎬 Empfehlungen",
        "explorer": "🔍 Entdecken",
        "mon_compte": "👤 Mein Konto",
        "choisis_film": "Wähle einen Film",
        "genre": "Genre",
        "tous": "Alle",
        "note_min": "Mindestbewertung IMDb",
        "duree_max": "Max. Dauer (Min.)",
        "films_trouves": "Filme gefunden",
        "films_similaires": "🎬 Ähnliche Filme:",
        "surprise": "🎲 Überrasch mich!",
        "bienvenue": "Willkommen",
        "deconnexion": "🚪 Abmelden",
        "connexion": "🔐 Anmelden",
        "commencer": "STARTEN",
        "retour": "⬅️ Zurück zur Startseite",
        "genre_label": "Genre",
        "duree": "Dauer",
        "note_imdb": "IMDb-Bewertung",
        "oscars": "Gewonnene Oscars",
        "nominations": "Nominierungen",
        "synopsis": "Zusammenfassung",
        "erreur_login": "❌ Falsche Anmeldedaten",
        "on_te_propose": "🎬 Unser Vorschlag:",
    },
}

# Détection query param AVANT tout
if "go" in st.query_params and st.query_params["go"] == "login":
    st.session_state.page = "login"
    st.query_params.clear()
    st.rerun()

# Si cookie actif, on redirige vers app
if st.session_state.get("authentication_status") and st.session_state.get("page") == "accueil":
    st.session_state.page = "app"

st.set_page_config(layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<style>
    .block-container { padding: 0 !important; max-width: 100% !important; }
    footer { display: none !important; }
    [data-testid="stAppViewContainer"] { padding: 0 !important; }
    [data-testid="stVerticalBlock"] { gap: 0 !important; padding: 0 !important; }
    iframe { display: block; border: none; }
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

# Langue par défaut
if "langue" not in st.session_state:
    st.session_state["langue"] = "🇫🇷 Français"

# Raccourci traduction
t = LANG[st.session_state["langue"]]

# ---- PAGE ACCUEIL ----
if st.session_state.page == "accueil":
    st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{ display: none !important; }}
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

    if st.button(t["commencer"]):
        st.session_state.page = "login"
        st.rerun()

# ---- PAGE LOGIN ----
elif st.session_state.page == "login":
    st.markdown("""
    <style>
        .block-container { padding: 2rem !important; }
        [data-testid="stSidebar"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)
    st.title(t["connexion"])
    authenticator.login()
    if st.session_state.get("authentication_status") is False:
        st.error(t["erreur_login"])
    if st.session_state.get("authentication_status"):
        st.session_state.page = "app"
        st.rerun()
    if st.button(t["retour"]):
        st.session_state.page = "accueil"
        st.rerun()

# ---- APP PRINCIPALE ----
elif st.session_state.page == "app" and st.session_state.get("authentication_status"):
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: block !important; }
        .block-container { padding: 2rem !important; }
        [data-testid="stVerticalBlock"] { gap: 1rem !important; }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        langue = st.selectbox("🌐", list(LANG.keys()), key="langue")
        t = LANG[langue]
        st.title("🎬 MovieMind")
        page = st.radio("", [
            t["recommandations"],
            t["explorer"],
            t["mon_compte"]
        ])
        st.markdown("---")
        if st.button(t["surprise"]):
            top_films = df[df["imdbRating"] >= 7.0].dropna(subset=["Poster"])
            surprise = top_films.sample(1).iloc[0]
            st.session_state["surprise_film"] = surprise["Title"]

    if page == t["recommandations"]:
        st.title(t["recommandations"])

        # Si un film surprise a été tiré, on l'affiche
        if "surprise_film" in st.session_state:
            st.success(f"{t['on_te_propose']} **{st.session_state['surprise_film']}**")

        titles_sorted = sorted(df["Title"].dropna().tolist())
        film_choisi = st.selectbox(t["choisis_film"], titles_sorted,
                                   index=titles_sorted.index(st.session_state["surprise_film"]) if "surprise_film" in st.session_state else 0)
        if film_choisi:
            film = df[df["Title"] == film_choisi].iloc[0]
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(film["Poster"], width=200)
            with col2:
                st.write(f"**{t['genre_label']} :** {film['Genre_1']}")
                st.write(f"**{t['note_imdb']} :** {film['imdbRating']}")
                st.write(f"**{t['duree']} :** {film['Runtime']} min")
                st.write(f"**{t['oscars']} :** {film['Oscars']}")
                st.write(f"**{t['nominations']} :** {film['Nominations']}")
                st.write(f"**{t['synopsis']} :** {film['Plot']}")
            st.subheader(t["films_similaires"])
            reco = recommander(film_choisi)
            cols = st.columns(5)
            for i, titre in enumerate(reco):
                film_reco = df[df["Title"] == titre].iloc[0]
                with cols[i]:
                    st.image(film_reco["Poster"], width=130)
                    st.caption(titre)
                    st.write(f"⭐ {film_reco['imdbRating']}")

    elif page == t["explorer"]:
        st.title(t["explorer"])

        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            st.selectbox(t["genre"], [t["tous"]] + sorted(df["Genre_1"].dropna().unique().tolist()), key="explorer_genre")
        with col_f2:
            st.slider(t["note_min"], 0.0, 10.0, 5.0, 0.5, key="explorer_note")
        with col_f3:
            st.slider(t["duree_max"], 60, 300, 180, 10, key="explorer_duree")

        genre = st.session_state["explorer_genre"]
        note_min = st.session_state["explorer_note"]
        duree_max = st.session_state["explorer_duree"]

        films_filtres = df.dropna(subset=["Poster"]).copy()
        films_filtres["imdbRating"] = pd.to_numeric(films_filtres["imdbRating"], errors="coerce")
        films_filtres["Runtime"] = pd.to_numeric(films_filtres["Runtime"], errors="coerce")
        if genre != t["tous"]:
            films_filtres = films_filtres[films_filtres["Genre_1"] == genre]
        films_filtres = films_filtres[films_filtres["imdbRating"] >= note_min]
        films_filtres = films_filtres[films_filtres["Runtime"] <= duree_max]
        films_filtres = films_filtres.sort_values("imdbRating", ascending=False)

        st.markdown(f"**{len(films_filtres)} {t['films_trouves']}**")

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

    elif page == t["mon_compte"]:
        st.title(f"{t['bienvenue']} {st.session_state['name']} ! 👋")
        authenticator.logout(t["deconnexion"])
        if not st.session_state.get("authentication_status"):
            st.session_state.page = "accueil"
            st.rerun()