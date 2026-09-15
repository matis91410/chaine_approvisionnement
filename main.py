def lire_donnees(nom_fichier):
    with open(nom_fichier) as f:
        lignes = [ligne for ligne in f if ligne]

    cout_fixe = float(lignes[0])
    cout_stock = float(lignes[1])
    demandes = [float(x) for x in lignes[2].split()]
    nombre_mois = len(demandes)

    return cout_fixe, cout_stock, demandes, nombre_mois


def calculer_cout_arc(demandes, i, j, cout_fixe, cout_stock):
    cout_stockage = sum(demandes[k] * (k - i) * cout_stock for k in range(i, j))
    return cout_fixe + cout_stockage


# Détection de circuit basée sur la MATRICE d'adjacence
def verifier_circuit_matrice(matrice, N):
    """Vérifie la présence de circuit en analysant les colonnes (prédécesseurs) de la matrice."""
    sommets_restants = set(range(N + 1))

    # Copie de travail de la matrice pour ne pas altérer l'originale
    mat = [ligne[:] for ligne in matrice]

    while sommets_restants:
        sources = []
        for j in sommets_restants:
            # Un sommet j est une source si sa colonne ne contient aucun arc entrant (!= inf)
            a_un_predecesseur = any(mat[i][j] != float("inf") for i in sommets_restants)
            if not a_un_predecesseur:
                sources.append(j)

        # Si aucun sommet sans prédécesseur n'est trouvé, il y a un circuit !
        if not sources:
            return True

        # Suppression des sources et de leurs arcs sortants (effacement des lignes)
        for s in sources:
            sommets_restants.remove(s)
            for col in range(N + 1):
                mat[s][col] = float("inf")

    return False  # Aucun circuit


def resoudre_et_afficher():
    cout_fixe, cout_stock, demandes, nombre_mois = lire_donnees("donne.txt")
    N = nombre_mois

    # 1. CRÉATION DE LA MATRICE D'ADJACENCE (Taille (N+1) x (N+1))
    matrice = [[float("inf")] * (N + 1) for _ in range(N + 1)]

    for i in range(N):
        for j in range(i + 1, N + 1):
            matrice[i][j] = calculer_cout_arc(demandes, i, j, cout_fixe, cout_stock)

    # 2. VÉRIFICATION DU CIRCUIT VIA LA MATRICE
    contient_circuit = verifier_circuit_matrice(matrice, N)

    # 3. RESSOLUTION PAR PROGRAMMATION DYNAMIQUE
    min_cost = [0] + [float("inf")] * N
    predecesseur = [-1] * (N + 1)

    for j in range(1, N + 1):
        for i in range(j):
            # Lecture directe dans la matrice M[i][j]
            cout = min_cost[i] + matrice[i][j]
            if cout < min_cost[j]:
                min_cost[j] = cout
                predecesseur[j] = i

    # 4. RECONSTITUTION DU CHEMIN
    chemin = []
    curr = N
    while curr != -1:
        chemin.append(curr)
        curr = predecesseur[curr]
    chemin.reverse()

    # 5. AFFICHAGE
    print(
        f"Données : {N} mois | Coût fixe : {cout_fixe:.0f} € | Stockage : {cout_stock:.0f} €/mois"
    )
    print(
        f"Graphe sans circuit (Analyse Matrice) : {'Non' if contient_circuit else 'Oui (Triangulaire supérieure)'}"
    )
    print(f"Coût total optimal : {min_cost[N]:,.2f} €\n")

    print("Planning optimal :")
    for k in range(len(chemin) - 1):
        i, j = chemin[k], chemin[k + 1]
        qte = sum(demandes[i:j])
        print(
            f"- Mois {i + 1} -> {j} : {qte:,.0f} unités | Coût : {matrice[i][j]:,.2f} €"
        )


if __name__ == "__main__":
    resoudre_et_afficher()