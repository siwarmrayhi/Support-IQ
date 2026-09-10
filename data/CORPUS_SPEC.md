# Spécification du corpus CloudDesk — V0 (10 documents)

CloudDesk est une plateforme SaaS fictive de gestion de projets, d'équipes,
d'abonnements et de comptes utilisateurs.

Chaque fichier commence par un en-tête YAML délimité par `---`.
Le champ `doc_id` doit correspondre **exactement** aux `relevant_doc_ids`
du dataset d'évaluation.

Longueur cible : 300 à 600 mots par document. Pas plus.

---

## Les trois plans (à garder cohérent partout)

| Plan | Prix / mois | Membres max | Projets actifs max |
|---|---|---|---|
| Starter | 12 € / utilisateur | 5 | 10 |
| Pro | 29 € / utilisateur | 50 | illimité |
| Business | 59 € / utilisateur | illimité | illimité |

---

## documentation/ (3 fichiers)

### 1. `auth_account_access.md`
```yaml
doc_id: auth_account_access
title: Connexion et accès au compte
source_type: documentation
category: authentication
```
**Doit contenir :** procédure de réinitialisation du mot de passe (lien
"Mot de passe oublié", e-mail de réinitialisation valable 30 minutes),
règles de complexité du mot de passe, activation de la double
authentification (2FA), verrouillage après 5 tentatives échouées.

**Cible de :** T001

---

### 2. `billing_subscription_plans.md`
```yaml
doc_id: billing_subscription_plans
title: Plans, abonnements et résiliation
source_type: documentation
category: billing
```
**Doit contenir :** le tableau des trois plans ci-dessus avec les limites
de membres, procédure de changement de plan, procédure de résiliation
(effet à la fin de la période en cours, pas de remboursement au prorata),
comportement en cas de suspension pour impayé : **les projets sont
conservés en lecture seule pendant 30 jours**, délai de régularisation
de 14 jours avant suspension.

**Cible de :** T006, T016, T018, T019

---

### 3. `teams_management.md`
```yaml
doc_id: teams_management
title: Gestion des équipes et des membres
source_type: documentation
category: teams
```
**Doit contenir :** inviter un membre (Paramètres → Équipe → Inviter),
les trois rôles (Administrateur, Membre, Lecteur) et leurs permissions,
retirer un membre, transférer la propriété d'un espace.

Mentionner que le nombre de membres est **limité par le plan souscrit**,
sans répéter les chiffres (ils sont dans `billing_subscription_plans`).

**Cible de :** T005, T019

---

## faq/ (3 fichiers)

Format : une suite de paires question / réponse, séparées par `##`.
Chaque paire doit rester compréhensible isolément — c'est ce qui
permettra un chunking propre.

### 4. `faq_account.md`
```yaml
doc_id: faq_account
title: FAQ - Compte utilisateur
source_type: faq
category: authentication
```
**Questions à couvrir :** changer son adresse e-mail (avec confirmation
sur les deux adresses), changer la langue de l'interface, supprimer
définitivement son compte, modifier son nom affiché.

**Cible de :** T002, T020

---

### 5. `faq_billing.md`
```yaml
doc_id: faq_billing
title: FAQ - Facturation
source_type: faq
category: billing
```
**Questions à couvrir :** moyens de paiement acceptés (carte bancaire
Visa/Mastercard, prélèvement SEPA, virement pour le plan Business
uniquement), où télécharger les factures (Paramètres → Facturation →
Historique, PDF disponibles 24 mois), changer de carte bancaire,
récupération du numéro de TVA intracommunautaire.

**Cible de :** T004, T007

---

### 6. `faq_projects.md`
```yaml
doc_id: faq_projects
title: FAQ - Projets
source_type: faq
category: projects
```
**Questions à couvrir :** créer un projet, **archiver un projet**
(le retire de la vue principale, réversible), dupliquer un projet,
exporter les données d'un projet en CSV.

**Cible de :** T003

---

## guides/ (2 fichiers)

### 7. `guide_payment_troubleshooting.md`
```yaml
doc_id: guide_payment_troubleshooting
title: Résoudre un problème de paiement
source_type: guide
category: billing
```
**Doit contenir :** la procédure pour **DC-4095** (échec de validation
3D Secure auprès de la banque), le cas du paiement débité mais non
reflété (délai de synchronisation bancaire de 24 à 48 h), la procédure
de réactivation après suspension.

**Cible de :** T014, T018

---

### 8. `guide_login_troubleshooting.md`
```yaml
doc_id: guide_login_troubleshooting
title: Résoudre un problème de connexion
source_type: guide
category: authentication
```
**Doit contenir :** la procédure pour **AUTH-401** (désynchronisation
horaire entre le téléphone et le serveur après activation de la 2FA),
la perte de l'appareil d'authentification (codes de secours générés à
l'activation), le déverrouillage d'un compte bloqué.

**Cible de :** T015, T020

---

## tickets/ (2 fichiers)

Format : un ticket historique = un fichier = un chunk.
Structure : contexte client, description du problème, diagnostic,
résolution appliquée.

### 9. `ticket_hist_payment_double.md`
```yaml
doc_id: ticket_hist_payment_double
title: Ticket #4471 - Échec de renouvellement DC-4092
source_type: historical_ticket
category: billing
```
**Doit contenir :** un client dont le renouvellement automatique a
échoué avec le code **DC-4092** (carte bancaire expirée), le diagnostic
de l'agent, la résolution (mise à jour du moyen de paiement puis
relance manuelle du prélèvement depuis l'espace Facturation).

**Cible de :** T017

---

### 10. `ticket_hist_team_limit.md`
```yaml
doc_id: ticket_hist_team_limit
title: Ticket #4102 - Impossible d'inviter un nouveau membre
source_type: historical_ticket
category: teams
```
**Doit contenir :** un client dont le bouton d'invitation semble
inactif, le diagnostic (plafond de 5 membres du plan Starter atteint),
la résolution (passage au plan Pro ou retrait d'un membre inactif).

**Cible de :** T019 (indirectement — il renforce le lien équipes/plans)

---

## Ce que le corpus ne doit SURTOUT PAS contenir

Ces sujets correspondent aux 6 tickets de refus. Si l'un d'eux apparaît,
même en une phrase, même pour dire "non", le test est invalidé.

- Paiement échelonné ou mensualisation de l'offre annuelle (T008)
- API, webhooks, intégrations tierces, Salesforce (T009)
- Application mobile iOS ou Android (T010)
- Localisation ou hébergement des données, RGPD, certifications (T011)
- Tarifs associatifs, réductions, remises, offres éducation (T012)
- Politique de rétention ou de récupération des projets supprimés (T013)

**Attention à la nuance :** ne pas écrire "nous n'acceptons pas le
paiement échelonné". Une mention explicite donnerait au système de quoi
répondre correctement, et le ticket ne testerait plus le refus.
Le sujet doit être totalement absent.

---

## Règle de cohérence

Les chiffres (5 membres, 30 jours, 14 jours, 24-48 h, 24 mois) doivent
être identiques partout où ils apparaissent. Une incohérence dans le
corpus rendrait ton évaluation ininterprétable : tu ne saurais pas si
une mauvaise réponse vient du système ou de tes données.
