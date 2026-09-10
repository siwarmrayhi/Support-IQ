---
doc_id: ticket_hist_payment_double
title: "Ticket #4471 - Échec de renouvellement DC-4092"
source_type: historical_ticket
category: billing
---

# Ticket #4471 - Échec de renouvellement DC-4092

## Contexte client

Client sur le plan Pro, abonnement actif depuis 14 mois. Facturation
mensuelle automatique par carte bancaire.

## Description du problème

Le client signale avoir reçu un e-mail l'informant que le renouvellement
automatique de son abonnement a échoué, avec le code d'erreur
**DC-4092** affiché dans son espace de facturation. Il indique ne pas
avoir modifié ses informations de paiement récemment et s'inquiète
d'une possible suspension de son espace de travail.

## Diagnostic de l'agent

Vérification effectuée depuis l'espace d'administration : le code
DC-4092 correspond systématiquement à un **refus lié à l'expiration de
la carte bancaire enregistrée**. La date d'expiration de la carte du
client était effectivement dépassée depuis le début du mois en cours,
ce qui n'avait pas été remarqué par le client.

Ce code est distinct de DC-4095, qui concerne un refus de validation
3D Secure au moment du paiement et non une carte expirée.

## Résolution appliquée

1. Le client a été guidé pour enregistrer une nouvelle carte bancaire
   depuis Paramètres → Facturation → Moyens de paiement.
2. Une fois la nouvelle carte enregistrée, le prélèvement en attente a
   été relancé manuellement depuis le même espace, via le bouton
   « Régler maintenant ».
3. Le paiement a été accepté immédiatement et l'abonnement est resté
   actif sans interruption de service, le délai de régularisation de
   14 jours n'ayant pas été dépassé.

## Note pour les agents

En cas de code DC-4092, vérifier en priorité la date d'expiration de la
carte enregistrée avant d'orienter le client vers d'autres pistes de
diagnostic.
