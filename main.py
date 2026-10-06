def lire_donnees(nom_fichier):
    with open(nom_fichier) as f:
        lignes = f.read().splitlines()

    cout_fixe = float(lignes[0])
    cout_stockage = float(lignes[1])
    demandes = [float(x) for x in lignes[2].split()]

    return cout_fixe, cout_stockage, demandes


def verifier_presence_circuit(matrice, nombre_sommets):
    sommets_restants = set(range(nombre_sommets))
    mat = [ligne[:] for ligne in matrice]

    while sommets_restants:
        sources = [
            j for j in sommets_restants 
            if not any(mat[i][j] != float("inf") for i in sommets_restants)
        ]
        
        if not sources:
            return True  # Circuit trouvé !

        for s in sources:
            sommets_restants.remove(s)
            mat[s] = [float("inf")] * nombre_sommets

    return False


def construire_matrice_couts(demandes, cout_fixe, cout_stockage):
    """Construit la matrice d'adjacence des coûts entre chaque mois."""
    N = len(demandes)
    matrice = [[float("inf")] * (N + 1) for _ in range(N + 1)]

    for i in range(N):
        for j in range(i + 1, N + 1):
            cout_stock_cumule = sum(
                demandes[k] * (k - i) * cout_stockage 
                for k in range(i, j)
            )
            matrice[i][j] = cout_fixe + cout_stock_cumule

    return matrice


def analyser_strategie(chemin, demandes, cout_fixe, matrice):
    """Calcule toutes les métriques de coût et de stock pour un chemin donné."""
    nb_commandes = len(chemin) - 1
    cout_commandes = nb_commandes * cout_fixe
    cout_total = sum(matrice[chemin[k]][chemin[k + 1]] for k in range(nb_commandes))
    cout_stockage = cout_total - cout_commandes

    stocks_fin_mois = []
    stock_actuel = 0
    idx_chemin = 0

    for mois in range(len(demandes)):
        if mois == chemin[idx_chemin]:
            prochain_point = chemin[idx_chemin + 1]
            stock_actuel += sum(demandes[mois:prochain_point])
            idx_chemin += 1
            
        stock_actuel -= demandes[mois]
        stocks_fin_mois.append(stock_actuel)

    return {
        "nb_cmd": nb_commandes,
        "qte_tot": sum(demandes),
        "stk_max": max(stocks_fin_mois),
        "stk_moy": sum(stocks_fin_mois) / len(demandes),
        "c_cmd": cout_commandes,
        "c_stk": cout_stockage,
        "c_tot": cout_total
    }


def trouver_chemin_optimal(matrice, N):
    """Recherche du chemin de coût minimal avec la programmation dynamique."""
    min_cost = [0] + [float("inf")] * N
    predecesseur = [-1] * (N + 1)

    for j in range(1, N + 1):
        for i in range(j):
            if matrice[i][j] != float("inf"):
                cout = min_cost[i] + matrice[i][j]
                if cout < min_cost[j]:
                    min_cost[j] = cout
                    predecesseur[j] = i

    chemin = []
    actuel = N
    while actuel != -1:
        chemin.append(actuel)
        actuel = predecesseur[actuel]
    chemin.reverse()

    return chemin


def resoudre_et_afficher():
    # 1. Chargement des données
    cout_fixe, cout_stockage, demandes = lire_donnees("donne.txt")
    N = len(demandes)

    # 2. Construction de la matrice de coûts du graphe
    matrice = construire_matrice_couts(demandes, cout_fixe, cout_stockage)

    # 3. Sécurité : Vérification de la présence de circuit dans le graphe
    circuit_detecte = verifier_presence_circuit(matrice, N + 1)
    if circuit_detecte:
        print(" Erreur : Le graphe contient un circuit. Impossible de continuer.")
        return

    # 4. Calcul du chemin optimal
    chemin_optimal = trouver_chemin_optimal(matrice, N)

    # 5. Définition des stratégies à comparer
    strategies = [
        ("1. Commandes mensuelles", list(range(N + 1))),
        ("2. Commande unique au début", [0, N]),
        ("3. Stratégie optimale", chemin_optimal)
    ]

    # 6. Affichage structuré du Tableau Comparatif
    print(" Analyse du graphe : Aucun circuit détecté\n")
    print("=" * 110)
    print(f"| {'Stratégie':<38} | {'Nb Cmd':<6} | {'Qte Tot':<7} | {'Stk Max':<7} | {'Stk Moy':<7} | {'Coût Cmd (€)':<12} | {'Coût Stk (€)':<12} | {'Coût Tot (€)':<12} |")
    print("=" * 110)

    for nom, chemin in strategies:
        m = analyser_strategie(chemin, demandes, cout_fixe, matrice)
        print(
            f"| {nom:<38} "
            f"| {m['nb_cmd']:<6} "
            f"| {m['qte_tot']:<7.0f} "
            f"| {m['stk_max']:<7.0f} "
            f"| {m['stk_moy']:<7.1f} "
            f"| {m['c_cmd']:<12.2f} "
            f"| {m['c_stk']:<12.2f} "
            f"| {m['c_tot']:<12.2f} |"
        )

    print("=" * 110)

    # 7. Planning d'exécution pour la stratégie retenue
    print("\n Planning optimal d'approvisionnement :")
    for k in range(len(chemin_optimal) - 1):
        i, j = chemin_optimal[k], chemin_optimal[k + 1]
        quantite = sum(demandes[i:j])
        cout_arc = matrice[i][j]
        print(f"  • Mois {i + 1} -> Mois {j} : Commander {quantite:.0f} unités (Coût de l'arc : {cout_arc:.2f} €)")


if __name__ == "__main__":
    resoudre_et_afficher()