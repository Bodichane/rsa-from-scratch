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
