"""Interface SupportIQ : connexion, tableau de bord, nouveau ticket et historique."""

from datetime import datetime

import streamlit as st

import api_client
from charts import auto_rate_gauge, status_donut
from theme import BRAND_HTML, apply_theme, chip, kpi_card, page_header, status_label, status_cell_style
from ticket_utils import STATUS_FILTERS, compute_stats, filter_tickets, shorten
import pandas as pd

st.set_page_config(page_title="SupportIQ", page_icon="💬", layout="wide")
apply_theme()

ESCALATION_MESSAGE = (
    "Nous n'avons pas pu répondre automatiquement de façon fiable. "
    "Votre ticket a été transmis à un agent, qui vous répondra."
)
NAV = [
    ("Tableau de bord", ":material/dashboard:"),
    ("Nouveau ticket", ":material/add_circle:"),
    ("Mes tickets", ":material/confirmation_number:"),
]


def start_session(data: dict) -> None:
    st.session_state["token"] = data["access_token"]
    st.session_state["user"] = data["user"]
    st.rerun()


def logout(message: str | None = None) -> None:
    for key in ("token", "user", "page"):
        st.session_state.pop(key, None)
    if message:
        st.session_state["flash"] = message
    st.rerun()


def handle_error(exc: api_client.ApiError) -> None:
    if exc.status_code == 401:
        logout("Votre session a expiré, veuillez vous reconnecter.")
    st.error(str(exc))


def format_date(value: str) -> str:
    return datetime.fromisoformat(value).strftime("%d/%m/%Y %H:%M") + " UTC"


def sources_line(sources: list[dict]) -> str:
    return "Sources consultées : " + ", ".join(s["title"] or s["doc_id"] for s in sources)


def auth_screen() -> None:
    _, center, _ = st.columns([1, 1.3, 1])
    with center:
        st.markdown(BRAND_HTML, unsafe_allow_html=True)
        st.write("")
        if "flash" in st.session_state:
            st.info(st.session_state.pop("flash"))
        login_tab, signup_tab = st.tabs(["Connexion", "Inscription"])

        with login_tab:
            with st.form("login_form"):
                email = st.text_input("Adresse e-mail", key="login_email")
                password = st.text_input("Mot de passe", type="password", key="login_password")
                submitted = st.form_submit_button("Se connecter", type="primary")
            if submitted:
                try:
                    data = api_client.login(email, password)
                except api_client.ApiError as exc:
                    st.error(str(exc))
                else:
                    start_session(data)

        with signup_tab:
            with st.form("signup_form"):
                full_name = st.text_input("Nom complet", key="signup_name")
                email = st.text_input("Adresse e-mail", key="signup_email")
                password = st.text_input(
                    "Mot de passe (8 caractères minimum)", type="password", key="signup_password"
                )
                submitted = st.form_submit_button("Créer mon compte", type="primary")
            if submitted:
                if not full_name.strip() or not email.strip():
                    st.error("Le nom et l'adresse e-mail sont obligatoires.")
                elif len(password) < 8:
                    st.error("Le mot de passe doit contenir au moins 8 caractères.")
                else:
                    try:
                        api_client.signup(email, full_name, password)
                        data = api_client.login(email, password)
                    except api_client.ApiError as exc:
                        st.error(str(exc))
                    else:
                        start_session(data)


def dashboard_page(token: str, user: dict) -> None:
    parts = user["full_name"].split()
    page_header(f"Bonjour {parts[0] if parts else ''}", "Voici un aperçu de vos demandes de support.")
    try:
        tickets = api_client.list_tickets(token)
    except api_client.ApiError as exc:
        handle_error(exc)
        return
    if not tickets:
        st.info("Vous n'avez pas encore de ticket : créez votre première demande depuis « Nouveau ticket ».")
        return

    stats = compute_stats(tickets)
    cards = [
        ("Tickets envoyés", stats["total"], "🎫", "blue"),
        ("Terminés", stats["resolved"], "✅", "green"),
        ("En cours de traitement", stats["in_progress"] + stats["pending"], "⏳", "orange"),
        ("Réponses automatiques", stats["auto"], "🤖", "teal"),
    ]
    for column, card in zip(st.columns(4), cards):
        column.markdown(kpi_card(*card), unsafe_allow_html=True)

    st.write("")
    left, right = st.columns(2)
    with left, st.container(border=True):
        st.markdown("**Taux de réponse automatique**")
        st.plotly_chart(auto_rate_gauge(stats["auto_rate"]), key="gauge")
    with right, st.container(border=True):
        st.markdown("**Répartition par statut**")
        st.plotly_chart(status_donut(stats), key="donut")

    st.markdown("#### Derniers tickets")
    rows = [
        {
            "N°": t["id"],
            "Date": format_date(t["created_at"]),
            "Demande": shorten(t["text"]),
            "Statut": status_label(t["status"]),
        }
        for t in tickets[:5]
    ]
    frame = pd.DataFrame(rows)
    st.dataframe(frame.style.map(status_cell_style, subset=["Statut"]), hide_index=True)


def new_ticket_page(token: str) -> None:
    page_header(
        "Nouveau ticket",
        "Décrivez votre problème : une réponse vous est proposée tout de suite quand c'est possible.",
    )
    with st.form("ticket_form"):
        text = st.text_area("Votre demande", height=160, max_chars=5000)
        submitted = st.form_submit_button("Envoyer", type="primary")
    if not submitted:
        return
    if not text.strip():
        st.warning("Veuillez décrire votre problème.")
        return

    with st.spinner("Analyse en cours..."):
        try:
            ticket = api_client.create_ticket(token, text)
        except api_client.ApiError as exc:
            handle_error(exc)
            return

    st.markdown(chip(ticket["status"]), unsafe_allow_html=True)
    if ticket["ai_answer"]:
        st.success("Voici une réponse proposée :")
        st.write(ticket["ai_answer"])
        if ticket["sources"]:
            st.caption(sources_line(ticket["sources"]))
    else:
        st.info(ESCALATION_MESSAGE)


def ticket_card(ticket: dict) -> None:
    with st.container(border=True):
        left, right = st.columns([4, 1])
        left.markdown(f"**Ticket #{ticket['id']}** · {format_date(ticket['created_at'])}")
        right.markdown(chip(ticket["status"]), unsafe_allow_html=True)
        st.write(ticket["text"])
        if ticket["ai_answer"]:
            with st.expander("Réponse automatique"):
                st.write(ticket["ai_answer"])
                if ticket["sources"]:
                    st.caption(sources_line(ticket["sources"]))
        if ticket["manager_reply"]:
            with st.expander("Réponse de l'agent", expanded=True):
                st.write(ticket["manager_reply"])


def history_page(token: str) -> None:
    page_header("Mes tickets", "Retrouvez toutes vos demandes et leur avancement.")
    try:
        tickets = api_client.list_tickets(token)
    except api_client.ApiError as exc:
        handle_error(exc)
        return
    if not tickets:
        st.info("Vous n'avez encore envoyé aucun ticket.")
        return

    search_col, status_col = st.columns([3, 1])
    query = search_col.text_input(
        "Rechercher",
        placeholder="Rechercher par mot-clé ou par numéro (ex. #3), puis Entrée",
        label_visibility="collapsed",
        key="ticket_search",
    )
    status_choice = status_col.selectbox(
        "Statut", list(STATUS_FILTERS), label_visibility="collapsed", key="ticket_status"
    )

    results = filter_tickets(tickets, query, STATUS_FILTERS[status_choice])
    st.caption(f"{len(results)} ticket(s) sur {len(tickets)}")
    if not results:
        st.info("Aucun ticket ne correspond à votre recherche.")
        return
    for ticket in results:
        ticket_card(ticket)


def go(page: str) -> None:
    st.session_state["page"] = page


MANAGER_NAV = [
    ("Tableau de bord", ":material/dashboard:"),
    ("Tickets", ":material/view_kanban:"),
]
KANBAN_STATUSES = ["pending_review", "in_progress", "resolved"]
MAX_PER_COLUMN = 20


def sidebar(nav: list, user: dict) -> str:
    current = st.session_state.get("page", nav[0][0])
    with st.sidebar:
        st.markdown(BRAND_HTML, unsafe_allow_html=True)
        st.write("")
        for label, icon in nav:
            st.button(
                label,
                icon=icon,
                key=f"nav_{label}",
                type="primary" if label == current else "secondary",
                on_click=go,
                args=(label,),
            )
        st.divider()
        st.caption(f"Connecté : {user['full_name']}")
        if st.button("Se déconnecter", icon=":material/logout:", key="logout"):
            logout()
    return current


def client_area(user: dict, token: str) -> None:
    current = sidebar(NAV, user)
    if current == "Tableau de bord":
        dashboard_page(token, user)
    elif current == "Nouveau ticket":
        new_ticket_page(token)
    else:
        history_page(token)


def run_action(action, *args) -> None:
    try:
        action(*args)
    except api_client.ApiError as exc:
        handle_error(exc)
    else:
        st.rerun()


def manager_dashboard(token: str) -> None:
    page_header("Tableau de bord", "Vue d'ensemble de l'activité du support.")
    try:
        tickets = api_client.manager_tickets(token)
    except api_client.ApiError as exc:
        handle_error(exc)
        return
    if not tickets:
        st.info("Aucun ticket pour le moment.")
        return

    stats = compute_stats(tickets)
    cards = [
        ("Tickets reçus", stats["total"], "🎫", "blue"),
        ("À traiter", stats["pending"], "📥", "orange"),
        ("En cours", stats["in_progress"], "💬", "teal"),
        ("Terminés", stats["resolved"], "✅", "green"),
    ]
    for column, card in zip(st.columns(4), cards):
        column.markdown(kpi_card(*card), unsafe_allow_html=True)

    st.write("")
    left, right = st.columns(2)
    with left, st.container(border=True):
        st.markdown("**Taux de réponse automatique**")
        st.plotly_chart(auto_rate_gauge(stats["auto_rate"]), key="m_gauge")
    with right, st.container(border=True):
        st.markdown("**Répartition par statut**")
        st.plotly_chart(status_donut(stats), key="m_donut")


def kanban_card(token: str, user: dict, ticket: dict) -> None:
    ticket_id = ticket["id"]
    status = ticket["status"]
    mine = ticket["assigned_to_id"] in (None, user["id"])
    with st.container(border=True):
        st.markdown(f"**Ticket #{ticket_id}**")
        st.caption(f"{ticket['client_name']} · {format_date(ticket['created_at'])}")
        st.text(shorten(ticket["text"], 160))

        if status == "resolved":
            who = "Réponse automatique" if ticket["decision"] == "auto_response" else "Réponse de l'agent"
            with st.expander(who):
                st.write(ticket["manager_reply"] or ticket["ai_answer"] or "")
            return

        if ticket["assigned_to_name"]:
            st.caption(f"Pris en charge par {ticket['assigned_to_name']}")
        if status == "pending_review":
            if st.button("Prendre en charge", key=f"take_{ticket_id}", icon=":material/play_arrow:"):
                run_action(api_client.change_status, token, ticket_id, "in_progress")
        elif mine:
            if st.button("Remettre à traiter", key=f"release_{ticket_id}", icon=":material/undo:"):
                run_action(api_client.change_status, token, ticket_id, "pending_review")

        if mine:
            with st.expander("Répondre"):
                with st.form(f"reply_{ticket_id}"):
                    text = st.text_area("Réponse au client", key=f"text_{ticket_id}", max_chars=5000)
                    sent = st.form_submit_button("Envoyer la réponse", type="primary")
                if sent:
                    if text.strip():
                        run_action(api_client.reply_to_ticket, token, ticket_id, text)
                    else:
                        st.warning("La réponse est vide.")


def kanban_page(token: str, user: dict) -> None:
    page_header("Tickets", "Prenez en charge les demandes et répondez à vos clients.")
    try:
        tickets = api_client.manager_tickets(token)
    except api_client.ApiError as exc:
        handle_error(exc)
        return
    query = st.text_input(
        "Rechercher",
        placeholder="Rechercher par mot-clé, client ou numéro (ex. #3), puis Entrée",
        label_visibility="collapsed",
        key="manager_search",
    )
    tickets = filter_tickets(tickets, query)

    for column, status in zip(st.columns(3), KANBAN_STATUSES):
        items = [t for t in tickets if t["status"] == status]
        with column:
            st.markdown(f"{chip(status)} &nbsp; **{len(items)}**", unsafe_allow_html=True)
            if not items:
                st.caption("Aucun ticket")
            for ticket in items[:MAX_PER_COLUMN]:
                kanban_card(token, user, ticket)
            if len(items) > MAX_PER_COLUMN:
                st.caption(f"{len(items) - MAX_PER_COLUMN} autres : affinez la recherche.")


def manager_area(user: dict, token: str) -> None:
    current = sidebar(MANAGER_NAV, user)
    if current == "Tickets":
        kanban_page(token, user)
    else:
        manager_dashboard(token)

user = st.session_state.get("user")
token = st.session_state.get("token")

if not user or not token:
    auth_screen()
elif user["role"] == "manager":
    manager_area(user, token)
else:
    client_area(user, token)