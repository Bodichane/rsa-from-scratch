# RSA From Scratch

## Description
Ce projet est une implémentation de l'algorithme RSA à partir de zéro, sans
aucune bibliothèque cryptographique. Il implémente également quelques attaques
visant à casser ce schéma de chiffrement.

## Concepts mathématiques

### PGCD
Sert à vérifier que l'indicatrice d'Euler $\phi(n)$ et l'exposant de chiffrement
$e$ sont premiers entre eux.

### Inverse modulaire
Puisque $e$ est premier avec $\phi(n)$, le théorème de Bézout garantit
l'existence de deux entiers $d$ et $k$ tels que :
$$ed = 1 + k\phi(n)$$
<br>Cela signifie $ed \equiv 1 \pmod{\phi(n)}$, ce qui prouve que $e$ est
inversible modulo $\phi(n)$. Cette propriété permet de calculer l'exposant de
déchiffrement : `d = mod_inverse(e, phi)`.

### Indicatrice d'Euler $\phi(n)$
Un entier $p > 1$ est premier si et seulement si tous les nombres de $1$ à
$p - 1$ sont premiers avec $p$. On a alors $\phi(p) = p - 1$. Dans le cas de RSA,
pour deux nombres premiers $p$ et $q$, on obtient :
$$\phi(n) = (p - 1)(q - 1)$$
<br>Cette valeur est essentielle pour générer la clé privée du système.

### Exponentiation modulaire
L'exponentiation modulaire calcule l'entier $c$ tel que :
$$c \equiv m^e \pmod n$$
<br>Cette formule chiffre le message $m$ de façon efficace à l'aide de l'exposant
$e$ et du module $n$.

---

## Attaques implémentées

### Attaque à faible exposant (Small $e$)
Cette attaque est exploitable lorsque l'exposant de chiffrement est très petit
(typiquement $e = 3$). Si le message $m$ est court, on peut se retrouver avec
$m^3 < n$. Le chiffrement devient alors une simple puissance :
$$c \equiv m^3 \pmod n \implies c = m^3$$
<br>Il suffit alors de calculer la racine cubique ordinaire de $c$ sur les
entiers pour retrouver le texte clair, sans factoriser $n$.

### Attaque par module commun
Cette attaque est possible lorsque deux utilisateurs partagent le même module $n$
mais possèdent des exposants de chiffrement différents $e_1$ et $e_2$ pour
chiffrer le même message $m$. On a :
$$c_1 \equiv m^{e_1} \pmod n \quad \text{and} \quad c_2 \equiv m^{e_2} \pmod n$$
<br>Si $\gcd(e_1, e_2) = 1$, le théorème de Bézout garantit l'existence de deux
entiers $a$ et $b$ tels que :
$$a \cdot e_1 + b \cdot e_2 = 1$$
<br>À l'aide de l'algorithme d'Euclide étendu, on calcule $a$ et $b$ (l'un d'eux
étant négatif, on utilise l'inverse modulaire). On retrouve alors le message
d'origine :
$$(c_1)^a \cdot (c_2)^b \equiv (m^{e_1})^a \cdot (m^{e_2})^b \equiv m^{a \cdot e_1 + b \cdot e_2} \equiv m^1 \equiv m \pmod n$$
<br>Le message est ainsi intercepté sans connaître les clés privées.

### Attaque de Bleichenbacher (oracle de padding PKCS#1)
Cette attaque par canal auxiliaire repose sur un serveur jouant le rôle d'oracle
de padding. Le serveur renvoie une information (ou une erreur différente) selon
que le padding du message déchiffré est valide (`True`) ou invalide (`False`).
Le but est de retrouver le message en choisissant soigneusement des entiers $s$
successifs et en envoyant le chiffré modifié au serveur :
$$c' \equiv c \cdot s^e \pmod n$$
<br>En analysant les réponses de l'oracle pour différents choix de $s$, on
resserre progressivement l'intervalle des valeurs possibles pour le message
jusqu'à l'isoler complètement.

---

## Installation et utilisation

### Prérequis
Ce projet est développé en **Python 3**. Aucune bibliothèque tierce n'est requise
puisque toutes les fonctions (RSA et attaques) sont codées à partir de zéro.

### 1. Cloner le projet
```bash
git clone https://github.com/Bodichane/rsa-from-scratch
cd rsa-from-scratch
```

### 2. Lancer le chiffrement/déchiffrement RSA
Pour générer les clés, chiffrer et déchiffrer un message de démonstration :
```bash
python rsa.py
```

### 3. Lancer les simulations d'attaque
Chaque attaque possède son propre script de démonstration prouvant sa
faisabilité :

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

### Temps d'exécution attendus

Toutes les clés sont générées sur 2048 bits (deux nombres premiers de 1024
bits), sans aucune bibliothèque tierce : la génération des clés domine le temps
de calcul. Mesuré sur une machine de bureau ordinaire :

| Script | Temps typique | Résultat |
|---|---|---|
| `rsa.py` | ~10 s | vérifie que `decrypt(encrypt(m)) == m` |
| `attacks/small_e.py` | ~40 s | retrouve le message sans factoriser `n` |
| `attacks/common_modulus.py` | ~5 s | retrouve le message sans aucune clé privée |
| `attacks/bleichenbacher.py` | ~30 s | trouve le premier `s` accepté par l'oracle |

Chaque script se termine par une assertion : un code de sortie 0 signifie que
l'attaque a réellement réussi, et pas seulement que le script s'est exécuté.

## Structure du projet
* `rsa.py` : primitives mathématiques de base (Miller-Rabin, PGCD, inverse
  modulaire, exponentiation modulaire) et logique RSA. Importable sans effet de
  bord — la démonstration est sous `if __name__ == "__main__"`.
* `attacks/small_e.py` : attaque à faible exposant (`e = 3`).
* `attacks/common_modulus.py` : attaque par module commun.
* `attacks/bleichenbacher.py` : padding PKCS#1 v1.5 et oracle de padding.

## Bilan
Ce projet m'a aidé à comprendre les fondamentaux du chiffrement RSA, de sa
logique conceptuelle jusqu'aux fonctions mathématiques qui le sous-tendent.

J'ai rencontré des difficultés, en particulier pour implémenter les fonctions
`mod_inverse()` et `addPadding()`. En les développant, j'ai appris à utiliser de
nouvelles méthodes natives de Python (comme `bit_length()`, `to_bytes()`,
`from_bytes()`, etc.). À la fin de ce projet, je suis désormais capable
d'expliquer le fonctionnement de RSA ainsi que les attaques auxquelles il est
vulnérable.

## Références et liens utiles
* [Chiffrement RSA — Wikipédia](https://fr.wikipedia.org/wiki/Chiffrement_RSA)
* [Indicatrice d'Euler — Wikipédia](https://fr.wikipedia.org/wiki/Indicatrice_d%27Euler)
* [Identité de Bézout — Wikipédia](https://fr.wikipedia.org/wiki/Identit%C3%A9_de_B%C3%A9zout)
* [PKCS #1 — Wikipédia](https://fr.wikipedia.org/wiki/PKCS)
* [RFC 8017 — PKCS #1 v2.2](https://www.rfc-editor.org/rfc/rfc8017)
* [Test de primalité de Miller-Rabin — Wikipédia](https://fr.wikipedia.org/wiki/Test_de_primalit%C3%A9_de_Miller-Rabin)
* Bleichenbacher, D. (1998). *Chosen Ciphertext Attacks Against Protocols Based on the RSA Encryption Standard PKCS #1*, CRYPTO ’98.
