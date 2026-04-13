import random
import re

import streamlit as st


DATA = {
    "Relaciona algebra": "Predstavlja formalni jezik za relacioni model koji obezbeđuje formalnu osnovu, tj. matematičku podlogu za operacijsku komponentu relacionog modela.",
    "SELEKCIJA": "Operacija kojom se iz relacije izdvajaju torke koje imaju zadatu vrednost specificiranih atributa. Unarna je i komutativna.",
    "PROJEKCIJA": "Operacija kojom se iz relacije izdvajaju kolone koje odgovaraju atributima po kojima se vrši operacija.",
    "UNIJSKA KOMPATIBILNOST": "Uslov koji pojedine operacije moraju da ispune; obe relacije imaju isti stepen i domene korespondentnih atributa.",
    "UNIJA": "Skup torki koje pripadaju relacijama r ili s, ili obema. Rezultujuća relacija ima imena atributa prve relacije.",
    "RAZLIKA": "Skup torki koje pripadaju relaciji r, ali ne pripadaju relaciji s.",
    "PRESEK": "Skup torki koje pripadaju obema relacijama. Komutativna je i asocijativna operacija.",
    "DEKARTOV PROIZVOD": "Relacija q koju čine torke dužine n + m za sve kombinacije torki iz r i s.",
    "DELJENJE": "Skup torki t koje se javljaju u r u kombinaciji sa svim torkama iz s.",
    "θ - SPOJ": "Spoj relacija gde se dobija rezultat kada kombinacija torki zadovoljava uslov Ai θ Bj.",
    "FUNKCIJE AGREGACIJE": "Funkcije koje omogućavaju da se izračunavaju nove vrednosti - agregirane vrednosti.",
    "Funkcionalna zavisnost": "Izraz oblika f: X --> Y koji predstavlja prvi tip ograničenja u relacionom modelu podataka.",
    "ZATVARAČ SKUPA FZ": "Skup svih funkcionalnih zavisnosti koje su sadržane u F ili se mogu izvesti (F+).",
    "ZATVARAČ SKUPA ATRIBUTA": "Skup atributa Y koje funkcionalno određuje X; koristi se za nalaženje super ključa.",
    "1NF": "Šema u kojoj domeni sadrže samo proste, tj. atomične vrednosti atributa.",
    "2NF": "Šema u kojoj je svaki atribut ili u ključu kandidatu ili nije parcijalno zavisan od njega.",
    "3NF": "Šema gde za svaku X --> A važi da je trivijalna, da je X super ključ ili da je A ključni atribut.",
    "BCNF": "Za svaku FZ X --> Y važi da je trivijalna ili da je X super ključ.",
    "Dekompozicija": "Proces zamene šeme relacije skupom šema uz očuvanje atributa i spoja bez gubitka.",
}


def normalize_answer(value: str) -> str:
    normalized = value.strip().casefold()
    normalized = normalized.replace("–", "-").replace("—", "-")
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = re.sub(r"\s*-\s*", "-", normalized)
    return normalized


def mask_term(definition: str, term: str) -> str:
    return re.sub(re.escape(term), "___", definition, flags=re.IGNORECASE)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            color: #2f241d;
            background:
                radial-gradient(circle at top left, rgba(244, 206, 118, 0.26), transparent 24%),
                radial-gradient(circle at top right, rgba(113, 160, 196, 0.10), transparent 22%),
                linear-gradient(180deg, #f6efe5 0%, #eadbc5 100%);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stAppViewContainer"] > .main {
            padding-top: 1.4rem;
        }

        .page-header {
            margin-bottom: 1.2rem;
        }

        .page-title {
            color: #241812;
            font-size: clamp(2.3rem, 5vw, 3.45rem);
            line-height: 0.98;
            font-weight: 900;
            letter-spacing: -0.03em;
            margin: 0;
            text-shadow: 0 1px 0 rgba(255, 255, 255, 0.35);
        }

        .page-subtitle {
            color: #735844;
            font-size: 1rem;
            line-height: 1.55;
            margin: 0.5rem 0 0;
            max-width: 46rem;
        }

        h1,
        [data-testid="stHeading"] h1 {
            color: #241812 !important;
            text-shadow: 0 1px 0 rgba(255, 255, 255, 0.35);
        }

        [data-testid="stCaptionContainer"] p {
            color: #735844 !important;
            font-size: 0.98rem !important;
            font-weight: 600;
        }

        .hero-card,
        .question-card,
        .summary-card,
        .review-card {
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(122, 92, 61, 0.18);
            border-radius: 24px;
            box-shadow: 0 22px 44px rgba(76, 55, 34, 0.10);
            padding: 1.35rem 1.4rem;
        }

        .hero-card {
            background: linear-gradient(145deg, rgba(255, 250, 243, 0.96), rgba(248, 238, 223, 0.92));
        }

        .question-card {
            background: linear-gradient(145deg, rgba(255, 251, 246, 0.97), rgba(246, 234, 217, 0.95));
        }

        .summary-card {
            background: linear-gradient(145deg, rgba(255, 252, 248, 0.97), rgba(244, 235, 221, 0.94));
        }

        .review-card {
            background: linear-gradient(145deg, rgba(255, 252, 247, 0.97), rgba(239, 232, 223, 0.95));
        }

        .hero-card::before,
        .question-card::before,
        .summary-card::before,
        .review-card::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 6px;
        }

        .hero-card::before {
            background: linear-gradient(180deg, #c67235 0%, #9d432d 100%);
        }

        .question-card::before {
            background: linear-gradient(180deg, #c68b45 0%, #84532d 100%);
        }

        .summary-card::before {
            background: linear-gradient(180deg, #ae7748 0%, #6d4631 100%);
        }

        .review-card::before {
            background: linear-gradient(180deg, #4a768d 0%, #305569 100%);
        }

        .eyebrow {
            color: #7a5c3d;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.4rem;
        }

        .hero-title {
            color: #2d2118;
            font-size: 2.4rem;
            line-height: 1.05;
            font-weight: 800;
            margin: 0;
        }

        .hero-copy,
        .question-copy,
        .summary-copy {
            color: #594639;
            font-size: 1rem;
            line-height: 1.65;
            margin-top: 0.9rem;
        }

        .definition-label {
            color: #7a5c3d;
            font-size: 0.86rem;
            font-weight: 700;
            letter-spacing: 0.07em;
            text-transform: uppercase;
            margin-bottom: 0.8rem;
        }

        .definition-text {
            color: #2f241d;
            font-size: 1.22rem;
            line-height: 1.8;
            margin: 0;
        }

        .metric-shell {
            background: linear-gradient(180deg, rgba(193, 150, 95, 0.18), rgba(122, 92, 61, 0.08));
            border: 1px solid rgba(122, 92, 61, 0.12);
            border-radius: 18px;
            padding: 0.95rem 1rem;
            min-height: 102px;
        }

        .metric-label {
            color: #7a5c3d;
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 700;
        }

        .metric-value {
            color: #2f241d;
            font-size: 1.7rem;
            font-weight: 800;
            margin-top: 0.25rem;
        }

        .metric-note {
            color: #715c4d;
            font-size: 0.9rem;
            margin-top: 0.2rem;
        }

        .feedback-good,
        .feedback-bad {
            border-radius: 18px;
            padding: 1rem 1.1rem;
            margin-top: 0.7rem;
        }

        .feedback-good {
            background: rgba(47, 125, 75, 0.12);
            border: 1px solid rgba(47, 125, 75, 0.18);
            color: #1f5a35;
        }

        .feedback-bad {
            background: rgba(163, 59, 47, 0.1);
            border: 1px solid rgba(163, 59, 47, 0.16);
            color: #7e2f25;
        }

        .review-list {
            margin: 0.8rem 0 0;
            padding-left: 1.2rem;
            color: #4d3b30;
            line-height: 1.75;
        }

        .footer-note {
            color: #6e594a;
            font-size: 0.9rem;
            margin-top: 0.3rem;
        }

        [data-testid="stWidgetLabel"] p {
            color: #6d4e39 !important;
            font-weight: 700;
        }

        div[data-baseweb="input"] > div {
            background: rgba(255, 249, 242, 0.98) !important;
            border: 1px solid rgba(143, 104, 68, 0.32) !important;
            border-radius: 16px !important;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.45);
        }

        div[data-baseweb="input"] > div:focus-within {
            border-color: #bf6f38 !important;
            box-shadow: 0 0 0 3px rgba(191, 111, 56, 0.16) !important;
        }

        div[data-baseweb="input"] input {
            color: #2f241d !important;
            caret-color: #9c4f28 !important;
            font-weight: 600;
        }

        div[data-baseweb="input"] input::placeholder {
            color: #947f72 !important;
            opacity: 1 !important;
        }

        div[data-testid="stFormSubmitButton"] button,
        div.stButton > button {
            min-height: 3rem;
            border-radius: 16px;
            border: none;
            font-weight: 800;
            letter-spacing: 0.01em;
            box-shadow: 0 12px 24px rgba(61, 41, 25, 0.14);
            transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
        }

        div.stButton > button {
            background: linear-gradient(135deg, #2e3546 0%, #171d29 100%);
            color: #fff8f1;
        }

        div[data-testid="stFormSubmitButton"] button,
        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #d86545 0%, #bb4938 100%);
            color: #fff8f1;
        }

        div[data-testid="stFormSubmitButton"] button:hover,
        div.stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 16px 30px rgba(61, 41, 25, 0.18);
            filter: brightness(1.03);
        }

        div[data-testid="stFormSubmitButton"] button:focus,
        div.stButton > button:focus {
            outline: none;
            box-shadow: 0 0 0 3px rgba(191, 111, 56, 0.18), 0 16px 30px rgba(61, 41, 25, 0.18);
        }

        [data-testid="stProgressBar"] > div {
            background-color: rgba(88, 70, 57, 0.18);
        }

        [data-testid="stProgressBar"] > div > div {
            background: linear-gradient(90deg, #c36b3c 0%, #7d4b2c 100%);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state() -> None:
    defaults = {
        "started": False,
        "finished": False,
        "terms": [],
        "current_index": 0,
        "correct_answers": 0,
        "errors": [],
        "submitted": False,
        "feedback": None,
        "last_answer": "",
        "answer_input": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def start_session() -> None:
    terms = list(DATA.keys())
    random.shuffle(terms)

    st.session_state.started = True
    st.session_state.finished = False
    st.session_state.terms = terms
    st.session_state.current_index = 0
    st.session_state.correct_answers = 0
    st.session_state.errors = []
    st.session_state.submitted = False
    st.session_state.feedback = None
    st.session_state.last_answer = ""
    st.session_state.answer_input = ""


def restart_session() -> None:
    start_session()


def return_home() -> None:
    st.session_state.started = False
    st.session_state.finished = False
    st.session_state.feedback = None
    st.session_state.submitted = False
    st.session_state.last_answer = ""
    st.session_state.answer_input = ""


def current_term() -> str:
    return st.session_state.terms[st.session_state.current_index]


def submit_answer() -> None:
    answer = st.session_state.answer_input.strip()
    term = current_term()
    is_correct = normalize_answer(answer) == normalize_answer(term)

    st.session_state.submitted = True
    st.session_state.last_answer = answer

    if is_correct:
        st.session_state.correct_answers += 1
        st.session_state.feedback = {
            "type": "good",
            "title": "Tačno.",
            "body": "Odgovor je pogođen iz prve. Nastavi dalje.",
        }
        return

    entered_text = answer if answer else "(bez unosa)"
    st.session_state.errors.append(term)
    st.session_state.feedback = {
        "type": "bad",
        "title": "Netačno.",
        "body": f"Tačan pojam: {term}<br>Tvoj unos: {entered_text}",
    }


def next_question() -> None:
    st.session_state.current_index += 1
    st.session_state.submitted = False
    st.session_state.feedback = None
    st.session_state.last_answer = ""
    st.session_state.answer_input = ""

    if st.session_state.current_index >= len(st.session_state.terms):
        st.session_state.finished = True


def render_metric(label: str, value: str, note: str) -> None:
    st.markdown(
        f"""
        <div class="metric-shell">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home() -> None:
    left, right = st.columns([1.4, 0.9], gap="large")

    with left:
        st.markdown(
            """
            <div class="hero-card">
                <div class="eyebrow">Relacioni model</div>
                <h1 class="hero-title">Drill za učenje pojmova bez terminala</h1>
                <p class="hero-copy">
                    Dobijaš definiciju, upisuješ tačan pojam, a aplikacija odmah proverava odgovor.
                    Redosled pitanja se nasumično meša pri svakoj rundi, pa možeš više puta da ponavljaš gradivo.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            f"""
            <div class="summary-card">
                <div class="eyebrow">Pregled runde</div>
                <p class="summary-copy">
                    Ukupno pojmova: <strong>{len(DATA)}</strong><br>
                    Format: jedan pojam po definiciji<br>
                    Kraj runde: lista pojmova za ponavljanje
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.button(
        "Pokreni drill",
        type="primary",
        use_container_width=True,
        on_click=start_session,
    )

    st.caption("Ovaj folder je spreman za GitHub i Streamlit Cloud.")


def render_feedback() -> None:
    feedback = st.session_state.feedback
    if not feedback:
        return

    class_name = "feedback-good" if feedback["type"] == "good" else "feedback-bad"
    st.markdown(
        f"""
        <div class="{class_name}">
            <strong>{feedback["title"]}</strong><br>
            {feedback["body"]}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quiz() -> None:
    total = len(st.session_state.terms)
    index = st.session_state.current_index
    term = current_term()
    definition = mask_term(DATA[term], term)
    progress_value = (index + (1 if st.session_state.submitted else 0)) / total

    st.markdown(
        """
        <div class="question-card">
            <div class="eyebrow">Aktivna runda</div>
            <div class="question-copy">
                Pogodi pojam na osnovu definicije. Posle proveravanja dobijaš odmah tačan odgovor.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        render_metric("Pitanje", f"{index + 1} / {total}", "Koliko si stigao u trenutnoj rundi")
    with col2:
        render_metric("Tačnih", str(st.session_state.correct_answers), "Broj pogodaka do sada")
    with col3:
        mistakes = len(dict.fromkeys(st.session_state.errors))
        render_metric("Greške", str(mistakes), "Jedinstveni pojmovi za ponavljanje")

    st.progress(progress_value)
    st.write("")
    st.markdown(
        f"""
        <div class="question-card">
            <div class="definition-label">Definicija</div>
            <p class="definition-text">{definition}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    with st.form("answer_form", clear_on_submit=False):
        st.text_input(
            "Tvoj odgovor",
            key="answer_input",
            disabled=st.session_state.submitted,
            placeholder="Upiši pojam ovde",
        )
        st.form_submit_button(
            "Proveri odgovor",
            type="primary",
            disabled=st.session_state.submitted,
            use_container_width=True,
            on_click=submit_answer,
        )

    render_feedback()

    if st.session_state.submitted:
        is_last = index == total - 1
        next_label = "Prikaži rezultat" if is_last else "Sledeći pojam"
        st.button(next_label, use_container_width=True, on_click=next_question)

    st.button("Pokreni novu rundu", use_container_width=True, on_click=restart_session)


def render_summary() -> None:
    total = len(st.session_state.terms)
    correct = st.session_state.correct_answers
    missed_terms = list(dict.fromkeys(st.session_state.errors))
    accuracy = round((correct / total) * 100) if total else 0

    top_left, top_right = st.columns([1.2, 0.8], gap="large")

    with top_left:
        st.markdown(
            f"""
            <div class="summary-card">
                <div class="eyebrow">Runda završena</div>
                <h1 class="hero-title" style="font-size: 2rem;">Rezultat {correct} / {total}</h1>
                <p class="summary-copy">
                    Tačnost u ovoj rundi: <strong>{accuracy}%</strong>.<br>
                    Ako imaš grešaka, ispod te čeka spisak pojmova za brzo ponavljanje.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top_right:
        st.markdown(
            """
            <div class="review-card">
                <div class="eyebrow">Sledeći korak</div>
                <p class="summary-copy">
                    Odmah pokreni novu random rundu ili prođi kroz listu promašenih pojmova dok ti je gradivo sveže.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        render_metric("Ukupno", str(total), "Broj pojmova u sesiji")
    with col2:
        render_metric("Tačnih", str(correct), "Odgovori koji su pogođeni")
    with col3:
        render_metric("Za obnavljanje", str(len(missed_terms)), "Pojmovi koje vredi ponoviti")

    st.write("")
    if missed_terms:
        review_markup = "".join(f"<li><strong>{term}</strong>: {DATA[term]}</li>" for term in missed_terms)
        st.markdown(
            f"""
            <div class="review-card">
                <div class="eyebrow">Pojmovi za ponavljanje</div>
                <ul class="review-list">{review_markup}</ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="review-card">
                <div class="eyebrow">Perfektna runda</div>
                <p class="summary-copy">Sve je tačno. Ova tura može pravo na GitHub bez blama.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Igraj ponovo", type="primary", use_container_width=True, on_click=restart_session)
    with col2:
        if st.button("Povratak na početak", use_container_width=True):
            st.session_state.started = False
            st.session_state.finished = False
            st.session_state.feedback = None
            st.session_state.submitted = False
            st.session_state.answer_input = ""
            st.rerun()

    st.markdown(
        '<p class="footer-note">Za Streamlit Cloud izaberi ovaj repo i glavni fajl `app.py`.</p>',
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(
        page_title="Relaciona Algebra Drill",
        page_icon="📚",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    inject_styles()
    init_state()

    st.title("Relaciona Algebra Drill")
    st.caption("Samostalna Streamlit verzija spremna za GitHub i Streamlit Cloud.")

    if not st.session_state.started:
        render_home()
        return

    if st.session_state.finished:
        render_summary()
        return

    render_quiz()


if __name__ == "__main__":
    main()
