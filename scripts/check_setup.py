"""Vérifie que l'environnement SupportIQ est correctement configuré."""

import numpy as np
import torch
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

from supportiq.config import settings


def check_torch() -> None:
    print(f"PyTorch        : {torch.__version__}")
    print(f"CUDA disponible: {torch.cuda.is_available()}")
    print(f"Device configuré: {settings.embedding_device}")


def check_llm() -> None:
    llm = ChatGoogleGenerativeAI(
        model=settings.llm_model,
        google_api_key=settings.google_api_key,
        temperature=0,
    )
    reponse = llm.invoke("Réponds uniquement par le mot : OK")
    print(f"LLM {settings.llm_model} : {reponse.text.strip()}")


def check_embeddings() -> None:
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": settings.embedding_device},
        encode_kwargs={"normalize_embeddings": True},
    )

    phrases = [
        "Je n'arrive pas à me connecter à mon compte.",
        "Problème d'authentification lors de la connexion.",
        "Comment changer la couleur du thème ?",
    ]
    vecteurs = np.array(embeddings.embed_documents(phrases))

    print(f"Dimension      : {vecteurs.shape[1]}")
    print(f"sim(0,1) proche  : {vecteurs[0] @ vecteurs[1]:.3f}")
    print(f"sim(0,2) éloigné : {vecteurs[0] @ vecteurs[2]:.3f}")


if __name__ == "__main__":
    check_torch()
    check_llm()
    check_embeddings()