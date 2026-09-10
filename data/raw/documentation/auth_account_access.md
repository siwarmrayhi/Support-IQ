---
doc_id: auth_account_access
title: Connexion et accès au compte
source_type: documentation
category: authentication
---

# Connexion et accès au compte

Cette page décrit les mécanismes de connexion à CloudDesk et les
options de sécurité disponibles sur votre compte.

## Réinitialiser un mot de passe oublié

1. Sur la page de connexion, cliquer sur « Mot de passe oublié ».
2. Saisir l'adresse e-mail associée au compte.
3. Un e-mail contenant un lien de réinitialisation est envoyé
   immédiatement. Ce lien reste valable **30 minutes**.
4. Choisir un nouveau mot de passe respectant les règles de complexité
   ci-dessous.

Si l'e-mail n'arrive pas après quelques minutes, vérifier le dossier
des indésirables avant de solliciter un nouvel envoi.

## Règles de complexité du mot de passe

Un mot de passe CloudDesk doit contenir au minimum 10 caractères, une
majuscule, un chiffre et un caractère spécial. Les mots de passe déjà
compromis dans des fuites de données connues sont automatiquement
refusés.

## Activer la double authentification (2FA)

La double authentification ajoute une étape de vérification lors de la
connexion, via une application d'authentification (Google
Authenticator, Authy, ou équivalent).

1. Se rendre dans Paramètres → Sécurité → Double authentification.
2. Scanner le QR code affiché avec l'application choisie.
3. Saisir le code à 6 chiffres généré pour confirmer l'activation.
4. Une liste de **codes de secours** est générée à cette étape :
   il est recommandé de les conserver dans un endroit sûr, séparé du
   téléphone habituel.

Une fois activée, chaque connexion demandera, en plus du mot de passe,
un code à usage unique généré par l'application.

## Verrouillage après tentatives échouées

Après **5 tentatives de connexion échouées** consécutives, le compte
est temporairement verrouillé pendant 15 minutes par mesure de
sécurité. Un e-mail de notification est envoyé au titulaire du compte
à chaque verrouillage.

## Se déconnecter de tous les appareils

En cas de doute sur la sécurité du compte, il est possible de forcer
la déconnexion de toutes les sessions actives depuis Paramètres →
Sécurité → Déconnecter tous les appareils. Cette action ne modifie pas
le mot de passe ; il est recommandé de le changer également si une
activité suspecte est constatée.
