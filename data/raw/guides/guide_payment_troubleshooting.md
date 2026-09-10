---
doc_id: guide_payment_troubleshooting
title: Résoudre un problème de paiement
source_type: guide
category: billing
---

# Résoudre un problème de paiement

Ce guide couvre les incidents de paiement les plus fréquents rencontrés
sur CloudDesk et la marche à suivre pour chacun.

## Erreur DC-4095 lors de la validation du paiement

Le code DC-4095 indique que la validation 3D Secure a été refusée par
la banque émettrice de la carte. CloudDesk n'a reçu aucune autorisation
de débit : aucun montant n'a été prélevé.

Marche à suivre :

1. Vérifier que le téléphone associé à la carte est joignable et que
   l'application bancaire est à jour, car la confirmation 3D Secure y
   est généralement envoyée.
2. Relancer le paiement depuis Paramètres → Facturation → Régler
   maintenant.
3. Si l'erreur persiste après deux tentatives, contacter la banque
   émettrice : le plafond de paiement en ligne peut être atteint, ou
   les paiements récurrents peuvent être bloqués sur le contrat.
4. En dernier recours, enregistrer un autre moyen de paiement depuis
   Paramètres → Facturation → Moyens de paiement.

## Le paiement a été débité mais l'abonnement reste inactif

La synchronisation entre l'établissement bancaire et CloudDesk peut
prendre de 24 à 48 heures ouvrées. Pendant ce délai, le débit apparaît
sur le relevé bancaire alors que le statut de l'abonnement affiche
encore « en attente de paiement ».

Aucune action n'est nécessaire pendant ce délai. Si le statut n'a pas
changé au-delà de 48 heures ouvrées, transmettre au support la
référence de transaction visible sur le relevé bancaire ainsi que la
date du débit.

Il ne faut pas relancer le paiement pendant cette période : une seconde
tentative pourrait entraîner un double débit.

## Réactiver un abonnement suspendu pour impayé

Un abonnement suspendu peut être réactivé à tout moment pendant la
période de conservation des données.

1. Se connecter avec un compte disposant du rôle Administrateur.
2. Ouvrir Paramètres → Facturation.
3. Vérifier ou mettre à jour le moyen de paiement enregistré.
4. Cliquer sur Régler maintenant pour solder la facture en attente.

La réactivation est effective dans les minutes qui suivent la
confirmation du paiement. Les projets et les données de l'espace sont
restaurés dans l'état où ils se trouvaient au moment de la suspension.

## Quand transmettre le ticket au support

Les situations suivantes nécessitent une intervention humaine :

- un montant a été prélevé deux fois pour la même période ;
- le débit n'apparaît toujours pas après 48 heures ouvrées ;
- l'erreur DC-4095 persiste après avoir essayé deux moyens de paiement
  différents.

Dans ces cas, joindre la référence de transaction et une capture du
relevé bancaire accélère le traitement.
