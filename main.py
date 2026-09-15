def lire_donnees(nom_fichier):
    with open(nom_fichier) as f:
        lignes = [ligne for ligne in f if ligne]

    cout_fixe = float(lignes[0])
    cout_stock = float(lignes[1])
    demandes = [float(x) for x in lignes[2].split()]
    nombre_mois = len(demandes)

    return cout_fixe, cout_stock, demandes, nombre_mois
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

