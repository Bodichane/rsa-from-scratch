# RSA From Scratch

## Description
Ce projet est une implémentation de l'algorithme RSA à partir de zéro, sans aucune utilisation de bibliothèques cryptographiques. Nous avons également implémenté quelques attaques pour tenter de casser cette méthode de chiffrement.

## Concepts mathématiques

### PGCD 
Utilisé pour vérifier que l'indicatrice d'Euler $\phi(n)$ et l'exposant de chiffrement $e$ sont premiers entre eux. 

### Inverse modulaire
Puisque $e$ est premier avec $\phi(n)$, le théorème de Bachet-Bézout garantit l'existence de deux entiers $d$ et $k$ tels que :
$$ed = 1 + k\phi(n)$$,
Cela signifie que $ed \equiv 1 \pmod{\phi(n)}$, ce qui prouve que $e$ est inversible modulo $\phi(n)$. Cette propriété permet de calculer l'exposant de déchiffrement : `d = inverseModulaire(e, phi)`.

### Fonction phi d'Euler $\phi(n)$
Un entier $p > 1$ est premier si et seulement si tous les nombres de $1$ à $p - 1$ sont premiers avec $p$. On a alors $\phi(p) = p - 1$. Dans le cas de RSA, pour deux nombres premiers $p$ et $q$, on obtient :
$$\phi(n) = (p - 1)(q - 1)$$

### Exponentiation modulaire
L'exponentiation modulaire consiste à calculer l'entier $c$ tel que :
$$c \equiv m^e \pmod n$$
Cette formule permet de chiffrer efficacement le message $m$ à l'aide de l'exposant $e$ et du module $n$.

## Description
Ce projet est une implémentation de l'algorithme RSA à partir de zéro, sans aucune utilisation de bibliothèques cryptographiques. Nous avons également implémenté quelques attaques pour tenter de casser cette méthode de chiffrement.

## Concepts mathématiques

### PGCD 
Utilisé pour vérifier que l'indicatrice d'Euler $\phi(n)$ et l'exposant de chiffrement $e$ sont premiers entre eux. 

### Inverse modulaire
Puisque $e$ est premier avec $\phi(n)$, le théorème de Bachet-Bézout garantit l'existence de deux entiers $d$ et $k$ tels que :
$$ed = 1 + k\phi(n)$$
<br>Cela signifie que $ed \equiv 1 \pmod{\phi(n)}$, ce qui prouve que $e$ est inversible modulo $\phi(n)$. Cette propriété permet de calculer l'exposant de déchiffrement : `d = inverseModulaire(e, phi)`.

### Fonction phi d'Euler $\phi(n)$
Un entier $p > 1$ est premier si et seulement si tous les nombres de $1$ à $p - 1$ sont premiers avec $p$. On a alors $\phi(p) = p - 1$. Dans le cas de RSA, pour deux nombres premiers $p$ et $q$, on obtient :
$$\phi(n) = (p - 1)(q - 1)$$
<br>Cette valeur est essentielle pour générer la clé privée du système.

### Exponentiation modulaire
L'exponentiation modulaire consiste à calculer l'entier $c$ tel que :
$$c \equiv m^e \pmod n$$
<br>Cette formule permet de chiffrer efficacement le message $m$ à l'aide de l'exposant $e$ et du module $n$.

---

## Attaques implémentées

### Attaque par exposant faible (Small $e$)
Cette attaque peut être exploitée lorsque la valeur de l'exposant de chiffrement est très petite (généralement $e = 3$). Si le message $m$ est court, on peut se retrouver dans le cas où $m^3 < n$. 
Le chiffrement devient alors une simple puissance : 
$$c \equiv m^3 \pmod n \implies c = m^3$$
<br>Il suffit alors de calculer la racine cubique classique de $c$ dans les entiers pour retrouver le message en clair, sans avoir à factoriser $n$.

### Attaque par module commun (Common Modulus)
Cette attaque est réalisable lorsque deux utilisateurs partagent le même module $n$ mais possèdent des exposants de chiffrement $e_1$ et $e_2$ différents pour chiffrer le même message $m$.
On dispose de :
$$c_1 \equiv m^{e_1} \pmod n \quad \text{et} \quad c_2 \equiv m^{e_2} \pmod n$$
<br>Si $\text{pgcd}(e_1, e_2) = 1$, le théorème de Bachet-Bézout assure qu'il existe deux entiers $a$ et $b$ tels que :
$$a \cdot e_1 + b \cdot e_2 = 1$$
<br>En appliquant l'algorithme d'Euclide étendu, on calcule $a$ et $b$ (l'un des deux étant négatif, on utilise l'inverse modulaire). On retrouve ensuite le message d'origine ainsi :
$$(c_1)^a \cdot (c_2)^b \equiv (m^{e_1})^a \cdot (m^{e_2})^b \equiv m^{a \cdot e_1 + b \cdot e_2} \equiv m^1 \equiv m \pmod n$$
<br>Le message est ainsi intercepté sans nécessiter la connaissance des clés privées.

### Attaque de Bleichenbacher (Oracle de padding PKCS#1 v1.5)
Cette attaque par canal auxiliaire (*side-channel*) se base sur un serveur agissant comme un oracle de padding. Le serveur renvoie une information (ou une erreur différente) selon que le padding du message déchiffré est valide (`True`) ou invalide (`False`). 
L'objectif est de découvrir le message en choisissant judicieusement des entiers $s$ successifs, en envoyant au serveur le texte chiffré modifié :
$$c' \equiv c \cdot s^e \pmod n$$
<br>En analysant les réponses de l'oracle pour différents choix de $s$, on réduit progressivement l'intervalle des valeurs possibles pour le message jusqu'à l'isoler complètement.

---

## Installation et Utilisation

### Prérequis
Ce projet est développé en **Python 3**. Aucune bibliothèque tierce n'est requise puisque toutes les fonctions (RSA et attaques) sont codées à partir de zéro.

### 1. Cloner le projet
Téléchargez le dépôt localement sur votre machine :
```bash
git clone https://github.com](https://github.com/Bodichane/rsa-from-scratch/
cd rsa-from-scratch
```

### 2. Exécuter le chiffrement/déchiffrement RSA
Pour générer des clés, chiffrer et déchiffrer un message de démonstration :
```bash
python main.py
```

### 3. Lancer les simulations d'attaques
Chaque attaque dispose de son propre script de démonstration pour prouver sa faisabilité :

* **Attaque Small $e$** :
  ```bash
  python attacks/small_e.py
  ```
* **Attaque par module commun** :
  ```bash
  python attacks/common_modulus.py
  ```
* **Attaque de Bleichenbacher** :
  ```bash
  python attacks/bleichenbacher.py
  ```

## Structure du projet
* `rsa.py` : Fonctions mathématiques de base (PGCD, inverse modulaire, exponentiation) et logique RSA.
* `attacks/` : Dossier contenant les scripts des différentes attaques implémentées.
* `main.py` : Point d'entrée principal pour tester le projet.
  
## Réflexion
Ce projet m'a permis de comprendre les bases du chiffrement RSA, en partant de sa logique conceptuelle jusqu'aux fonctions mathématiques qui se cachent derrière.
