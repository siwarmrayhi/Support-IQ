"""Interface de démonstration de SupportIQ."""

import httpx
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.title("SupportIQ")
st.caption("Copilote de support client pour CloudDesk")

ticket = st.text_area("Ticket du client", height=150)

if st.button("Analyser le ticket") and ticket.strip():
    with st.spinner("Analyse en cours..."):
        try:
            response = httpx.post(
                f"{API_URL}/tickets", json={"ticket": ticket}, timeout=120
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            st.error(f"Erreur de l'API : {exc}")
            st.stop()

    data = response.json()
    if data["status"] == "auto_response":
        st.success("Réponse proposée")
        st.write(data["answer"])
        st.subheader("Sources consultées")
        for source in data["sources"]:
            st.write(f"- {source['title']} ({source['doc_id']})")
    else:
        st.warning(
            "Je ne dispose pas de suffisamment d'informations dans la base "
            "de connaissances pour répondre de manière fiable à cette demande. "
            "Ce ticket doit être examiné par un agent humain."
        )