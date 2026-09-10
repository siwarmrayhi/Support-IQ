---
doc_id: ticket_hist_team_limit
title: "Ticket #4102 - Impossible d'inviter un nouveau membre"
source_type: historical_ticket
category: teams
---

# Ticket #4102 - Impossible d'inviter un nouveau membre

## Contexte client

Client sur le plan Starter, espace de travail comptant déjà 5 membres
actifs.

## Description du problème

Le client signale que le bouton d'invitation dans Paramètres → Équipe
semble inactif : aucune erreur explicite ne s'affiche, mais l'e-mail
d'invitation n'est jamais envoyé lorsqu'il tente d'ajouter un sixième
membre à son équipe.

## Diagnostic de l'agent

Vérification effectuée depuis l'espace d'administration : l'espace de
travail du client compte déjà 5 membres, ce qui correspond exactement
au plafond autorisé par le plan Starter. Le comportement observé
(bouton apparemment inactif, sans message d'erreur visible) est le
symptôme habituel d'un plafond de plan atteint plutôt qu'un
dysfonctionnement technique.

## Résolution appliquée

Deux options ont été présentées au client :

1. **Passer au plan Pro**, qui autorise jusqu'à 50 membres, depuis
   Paramètres → Facturation → Modifier le plan. Le changement est
   immédiat.
2. **Retirer un membre inactif** de l'équipe actuelle pour libérer une
   place dans le quota du plan Starter, sans changer de plan.

Le client a choisi de passer au plan Pro. Une fois le changement
effectué, l'invitation du nouveau membre a fonctionné normalement.

## Note pour les agents

Un bouton d'invitation apparemment inactif, sans message d'erreur
explicite, doit toujours faire vérifier en premier lieu le nombre de
membres actuels par rapport à la limite du plan souscrit, avant
d'envisager un problème technique.
