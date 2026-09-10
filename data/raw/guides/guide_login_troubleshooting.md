---
doc_id: guide_login_troubleshooting
title: Résoudre un problème de connexion
source_type: guide
category: authentication
---

# Résoudre un problème de connexion

Ce guide couvre les incidents de connexion les plus fréquents sur
CloudDesk.

## Erreur AUTH-401 après activation de la double authentification

Le code AUTH-401 signale un rejet du code de vérification généré par
l'application d'authentification. La cause la plus fréquente est une
**désynchronisation de l'horloge** entre le téléphone et les serveurs
CloudDesk : les codes à usage unique sont calculés à partir de l'heure
exacte, et un décalage de plus de 30 secondes suffit à les invalider.

Marche à suivre :

1. Vérifier que la date et l'heure du téléphone sont réglées sur
   « automatique » dans les paramètres de l'appareil, et non fixées
   manuellement.
2. Attendre le prochain code généré par l'application (renouvelé toutes
   les 30 secondes) et réessayer.
3. Si l'erreur persiste, désactiver puis réactiver la double
   authentification depuis Paramètres → Sécurité, ce qui resynchronise
   l'application avec le compte.

## Perte de l'appareil d'authentification

En cas de changement de téléphone ou de perte de l'appareil utilisé
pour la double authentification, l'accès au compte reste possible grâce
aux **codes de secours** générés lors de l'activation de la 2FA.

1. Sur l'écran demandant le code de vérification, cliquer sur
   « Utiliser un code de secours ».
2. Saisir l'un des codes conservés lors de l'activation initiale.
3. Une fois connecté, reconfigurer la double authentification sur le
   nouvel appareil depuis Paramètres → Sécurité, ce qui invalide
   l'ancienne configuration et génère une nouvelle liste de codes de
   secours.

Si aucun code de secours n'a été conservé, contacter le support avec
une pièce justifiant l'identité du titulaire du compte.

## Compte verrouillé après plusieurs tentatives échouées

Après 5 tentatives de connexion échouées, le compte est verrouillé
automatiquement pendant 15 minutes. Aucune action n'est nécessaire :
l'accès est rétabli automatiquement à l'issue de ce délai. Il n'est pas
possible de raccourcir ce délai, y compris en contactant le support,
par mesure de sécurité.

## Quand transmettre le ticket au support

Une intervention humaine est nécessaire si l'erreur AUTH-401 persiste
après resynchronisation de l'horloge et réinitialisation de la 2FA, ou
si l'accès au compte est perdu sans code de secours disponible.
