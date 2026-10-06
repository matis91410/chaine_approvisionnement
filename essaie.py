def lire_donnees(nom_fichier):
    # Lit le fichier et extrait le coût fixe, le coût de stockage et les demandes
    with open(nom_fichier) as f:
        lignes = f.read().splitlines()
    return float(lignes[0]), float(lignes[1]), [float(x) for x in lignes[2].split()]


def verifier_circuit(matrice, N):
    # Vérifie si le graphe contient un circuit en supprimant les sommets sans prédécesseur
    sommets = set(range(N + 1))
    mat = [ligne[:] for ligne in matrice]

    while sommets_restants:
        sources = [] 
        for j in sommets_restants:
            a_un_predecesseur = any(mat[i][j] != float("inf") for i in sommets_restants) # Il existe au moins un sommet i restant qui pointe directement vers j 
            
            if not a_un_predecesseur:
                sources.append(j)

        if not sources:
            return True 

        for s in sources:
            sommets_restants.remove(s) # Parcourt chaque sommet source identifié et le retire de l'ensemble des sommets restants
            
            # Efface tous les arcs sortants du sommet s en les passant à l'infini 
            mat[s] = [float("inf")] * (N + 1) 

    return False 


def analyser_strategie(chemin, demandes, f_cost, matrice):
    # Calcule toutes les métriques (commandes, coûts, stocks max et moyen) pour un chemin donné
    nb_cmd = len(chemin) - 1
    c_cmd = nb_cmd * f_cost
    c_tot = sum(matrice[chemin[k]][chemin[k + 1]] for k in range(nb_cmd))
    c_stk = c_tot - c_cmd

    # Reconstitution du niveau de stock en fin de chaque mois
    stocks = []
    stock = 0
    idx = 0
    for m in range(len(demandes)):
        if m == chemin[idx]:
            stock += sum(demandes[m:chemin[idx + 1]])
            idx += 1
        stock -= demandes[m]
        stocks.append(stock)

    return {
        "nb_cmd": nb_cmd,
        "qte_tot": sum(demandes),
        "stk_max": max(stocks),
        "stk_moy": sum(stocks) / len(demandes),
        "c_cmd": c_cmd,
        "c_stk": c_stk,
        "c_tot": c_tot
    }


def resoudre_et_afficher():
    f_cost, h_cost, demandes = lire_donnees("donne.txt")
    N = len(demandes)

    # 1. Construction de la matrice d'adjacence (coût fixe + stockage)
    matrice = [[float("inf")] * (N + 1) for _ in range(N + 1)]
    for i in range(N):
        for j in range(i + 1, N + 1):
            stk_cost = sum(demandes[k] * (k - i) * h_cost for k in range(i, j))
            matrice[i][j] = f_cost + stk_cost

    # 2. Sécurité : vérification d'absence de circuit
    contient_circuit = verifier_circuit(matrice, N)
    if contient_circuit:
        print("Erreur : Le graphe contient un circuit.")
        return

    # 3. Programmation dynamique (Wagner-Whitin)
    min_cost = [0] + [float("inf")] * N
    prev = [-1] * (N + 1)

    for j in range(1, N + 1):
        for i in range(j):
            cost = min_cost[i] + matrice[i][j]
            if cost < min_cost[j]:
                min_cost[j] = cost
                prev[j] = i

    # Reconstitution du chemin optimal
    chemin_ww = []
    curr = N
    while curr != -1:
        chemin_ww.append(curr)
        curr = prev[curr]
    chemin_ww.reverse()

    # 4. Chemins des stratégies à comparer
    strats = [
        ("1. Commandes mensuelles", list(range(N + 1))),
        ("2. Commande unique au début", [0, N]),
        ("3. Politique optimale (Wagner-Whitin)", chemin_ww)
    ]

    # 5. Affichage du tableau comparatif
    print(f"Détection de circuit : {'Circuit détecté' if def lire_donnees(nom_fichier):
    # Ouvre le fichier spécifié en mode lecture
    with open(nom_fichier) as f:
        lignes = f.read().splitlines() # splitline sert principalement à supprimer les saut de lignes qui pourrait être conserver dans la list (/n) 

    # Extrait la première ligne correspondant au coût fixe d'une commande
    cout_fixe = float(lignes[0])
    # Extrait la deuxième ligne correspondant au coût unitaire de stockage par mois
    cout_stock = float(lignes[1])
    demandes = [float(e) for e in lignes[2].split()] # e (variable temporaire) correspond à chaque élément de la liste et pour chaque élément brut de la liste elle va le convertir en float, split quant à lui sert à découpé la chaine de caractere de façon à l'adapter en une liste python
    
    # Renvoie les trois paramètres extraits sous forme de tuple
    return cout_fixe, cout_stock, demandes


def verifier_circuit(matrice, N): # Définnisement d'une fonction avec des variables d'entrées avec N : Nombre total de mois.
    # set() crée un ensemble où l'on peut retirer des éléments facilement.
    # range(N + 1) génère la liste des numéros de sommets du mois 0 jusqu au mois N final.
    sommets_restants = set(range(N + 1)) 
    # Crée une copie pour chaque lignes de la matrice avec :
    mat = [ligne[:] for ligne in matrice]

    # Tant qu'il reste au moins un sommet à analyser dans le graphe
    while sommets_restants:
        sources = [] # Créer une liste vide qui recueillera les sommets qui n'ont pas ou plus de prédécesseur
        
        for j in sommets_restants: # Pour chaque sommet dans l'ensemble sommets_restant
    
            a_un_predecesseur = any(mat[i][j] != float("inf") for i in sommets_restants) # Il existe au moins un sommet i restant qui pointe directement vers j 
            
            # Vérifie si le sommet j est une source (aucun sommet restant ne pointe vers lui)
            if not a_un_predecesseur:
                sources.append(j) # Sinon ajoute(append) le sommet qui n'a pas ou plus de prédécesseur dans la liste source

        # Si aucun sommet n'est trouvé sans prédécesseur alors qu'il reste des sommets, il y a un circuit
        if not sources:
            return True # Retourne vrai si il y à aucun sommet dans la liste source

        # Parcourt tous les sommets identifiés comme sources
        for s in sources:
            sommets_restants.remove(s) # Parcourt chaque sommet source identifié et le retire de l'ensemble des sommets restants
            
            # Efface tous les arcs sortants du sommet s en les passant à l'infini 
            mat[s] = [float("inf")] * (N + 1) 

    return False  # Aucun circuit détecté 


# Définit la fonction de calcul des indicateurs de performance pour un chemin donné
def calculer_indicateurs(chemin, demandes, cout_fixe, matrice):
    # Calcule le nombre total de commandes passées dans cette stratégie
    nb_commandes = len(chemin) - 1
    # Calcule la somme globale des unités demandées sur toute la période
    qte_totale = sum(demandes)
    # Calcule le coût total lié au passage des commandes (nombre de commandes x coût fixe)
    cout_commande = nb_commandes * cout_fixe
    
    # Reconstitution du stock en fin de mois pour chaque mois
    stocks_fin_mois = []
    # Initialise le niveau de stock disponible au début de la simulation
    stock_courant = 0
    # Initialise le pointeur pour parcourir la liste des étapes du chemin
    idx_chemin = 0
    
    # Parcourt chaque mois m de la période de planification
    for m in range(len(demandes)):
        # Réception d'une commande au mois m
        if m == chemin[idx_chemin]:
            # Récupère l'indice du mois jusqu'auquel la commande actuelle doit couvrir les besoins
            prochain_m = chemin[idx_chemin + 1]
            # Ajoute au stock courant la somme des demandes allant du mois m au mois prochain_m
            stock_courant += sum(demandes[m:prochain_m])
            # Avance d'un cran dans l'index du chemin de commande
            idx_chemin += 1
            
        # Consommation de la demande du mois m
        stock_courant -= demandes[m]
        # Sauvegarde le niveau de stock restant à la fin du mois m
        stocks_fin_mois.append(stock_courant)
        
    # Identifie la valeur maximale atteinte par le stock parmi tous les fins de mois
    stock_max = max(stocks_fin_mois) if stocks_fin_mois else 0
    # Calcule le niveau moyen du stock sur l'ensemble des mois
    stock_moyen = sum(stocks_fin_mois) / len(demandes) if demandes else 0
    
    # Coût total calculé via la matrice d'adjacence
    cout_tot = sum(matrice[chemin[k]][chemin[k + 1]] for k in range(nb_commandes))
    # Déduit le coût de stockage total en soustrayant le coût de commande au coût total
    cout_stockage = cout_tot - cout_commande

    # Renvoie l'ensemble des métriques calculées sous la forme d'un dictionnaire
    return {
        "nb_cmd": nb_commandes,
        "qte_tot": qte_totale,
        "stock_max": stock_max,
        "stock_moyen": stock_moyen,
        "cout_cmd": cout_commande,
        "cout_stock": cout_stockage,
        "cout_total": cout_tot
    }


# Définit la fonction principale qui exécute l'analyse et affiche les résultats
def resoudre_et_afficher():
    
    # Charge les variables de coût et le tableau des demandes à partir du fichier texte
    cout_fixe, cout_stock, demandes = lire_donnees("donne.txt")
    # Calcule le nombre total de mois d'étude
    N = len(demandes)
    # initialisation d'une matrice en attribuant pour chaque ligne qui correspond au nombre N mois la valeur infini _= valeur qui est recopié N fois
    # infini signifie qu'il n'existe aucun arc direct entre ces deux sommet elle sert principalement à de l'initialisation pour ainsi être changé à nimporte quel moment.
    matrice = [[float("inf")] * (N + 1) for _ in range(N + 1)]
    
    # i : Mois où l'on effectue la commande
    for i in range(N):
        # j : Mois jusqu'auquel cette commande va couvrir la demande
        for j in range(i + 1, N + 1):
            # Calcule le coût cumulé de possession du stock pour couvrir les mois allant de i à j-1
            cout_stockage = sum(demandes[k] * (k - i) * cout_stock for k in range(i, j))
            # Enregistre le coût total (fixe + stockage) pour la transition du mois i au mois j
            matrice[i][j] = cout_fixe + cout_stockage

    # Lance la vérification pour s'assurer que le graphe ne possède aucun cycle
    contient_circuit = verifier_circuit(matrice, N)

    # Si un circuit est trouvé, affiche un message d'erreur et stoppe l'exécution
    if contient_circuit:
        # Affiche le message prévenant de la présence d'un circuit
        print("Erreur : Le graphe contient un circuit. Impossible d'utiliser la programmation dynamique.")
        # Interrompt le déroulement de la fonction
        return
    
    # --- STRATÉGIE 1 : Commandes mensuelles ---
    chemin_mensuel = list(range(N + 1))  # Chemin [0, 1, 2, ..., N]

    # --- STRATÉGIE 2 : Commande unique au début ---
    chemin_unique = [0, N]               # Chemin [0, N]
    
    # --- STRATÉGIE 3 : Politique optimale ---
    min_cost = [0] + [float("inf")] * N # initialisation d'un tableau qui va contenir le coût minimal cumulé pour arriver à chaque mois j
    predecesseur = [-1] * (N + 1)       # initialisation d'un tableau qui va stocker les prédécesseur afin de garder en mémoire le mois de départ de la commande retenue

    for j in range(1, N + 1): # On avance mois par mois (du mois 1 jusqu'au mois N)
        for i in range(j): # On teste tous les mois de départ i possibles pour la dernière commande 
            cout = min_cost[i] + matrice[i][j] # Calcule le coût cumulé si l'on passe la dernière commande au mois i
            if cout < min_cost[j]: # Si ce nouveau coût est plus faible que le meilleur coût actuellement connu pour j
                min_cost[j] = cout # On met à jour le coût minimal pour atteindre le mois j
                predecesseur[j] = i # On enregistre le mois i comme le prédécesseur optimal pour j

    # 5. Reconstitution du chemin optimal (de la fin vers le début)
    chemin = []
    
    # Initialise le pointeur au dernier sommet (mois N) pour démarrer la remontée du chemin
    curr = N
    while curr != -1: # Tant qu'il y à un prédécesseur alors on continue
        chemin.append(curr) # Ajoute le prédécesseur à chemin
        curr = predecesseur[curr] # Remonte au mois de commande optimal précédent
    # Remet les mois dans l'ordre chronologique de 0 à N
    chemin.reverse()

    # --- CALCUL DES INDICATEURS POUR CHAQUE STRATÉGIE ---
    # Calcule les indicateurs pour la stratégie des commandes mensuelles
    m_mensuel = calculer_indicateurs(chemin_mensuel, demandes, cout_fixe, matrice)
    # Calcule les indicateurs pour la stratégie de la commande unique
    m_unique = calculer_indicateurs(chemin_unique, demandes, cout_fixe, matrice)
    # Calcule les indicateurs pour la stratégie optimale de Wagner-Whitin
    m_ww = calculer_indicateurs(chemin, demandes, cout_fixe, matrice)

    # --- AFFICHAGE COMPARATIF ---
    # Affiche le résultat du test de présence de circuit
    print(f"Détection de circuit : {'Circuit détecté' if contient_circuit else 'Aucun circuit'}\n")
    
    # Imprime la ligne d'en-tête supérieure du tableau
    print("=" * 115)
    # Imprime les titres des colonnes du tableau comparatif avec un alignement sur la largeur
    print(f"{'Stratégie':<28} | {'Nb Cmd':<7} | {'Qte Tot':<9} | {'Stk Max':<9} | {'Stk Moy':<9} | {'Coût Cmd (€)':<13} | {'Coût Stk (€)':<13} | {'Coût Tot (€)':<12}")
    # Imprime la ligne de séparation sous le titre des colonnes
    print("=" * 115)

    # Associe chaque nom de stratégie avec ses métriques calculées dans une liste
    strats = [
        ("1. Commandes mensuelles", m_mensuel),
        ("2. Commande unique au début", m_unique),
        ("3. Politique optimale", m_ww)
    ]

    # Parcourt et affiche chaque stratégie formatée dans le tableau
    for nom, m in strats:
        # Affiche la ligne courante du tableau avec le nom et toutes ses valeurs numériques formatées
        print(f"{nom:<28} | {m['nb_cmd']:<7} | {m['qte_tot']:<9.0f} | {m['stock_max']:<9.0f} | {m['stock_moyen']:<9.1f} | {m['cout_cmd']:<13,.2f} | {m['cout_stock']:<13,.2f} | {m['cout_total']:<12,.2f}")

    # Imprime la ligne de fermeture inférieure du tableau
    printcontient_circuit else 'Aucun circuit'}\n")
    print("=" * 115)
    print(f"{'Stratégie':<36} | {'Nb Cmd':<7} | {'Qte Tot':<9} | {'Stk Max':<9} | {'Stk Moy':<9} | {'Coût Cmd (€)':<12} | {'Coût Stk (€)':<12} | {'Coût Tot (€)':<12}")
    print("=" * 115)

    for nom, path in strats:
        m = analyser_strategie(path, demandes, f_cost, matrice)
        print(f"{nom:<36} | {m['nb_cmd']:<7} | {m['qte_tot']:<9.0f} | {m['stk_max']:<9.0f} | {m['stk_moy']:<9.1f} | {m['c_cmd']:<12,.2f} | {m['c_stk']:<12,.2f} | {m['c_tot']:<12,.2f}")

    print("=" * 115)

    # 6. Planning détaillé de la solution optimale
    print("\nPlanning optimal (Wagner-Whitin) :")
    for k in range(len(chemin_ww) - 1):
        i, j = chemin_ww[k], chemin_ww[k + 1]
        print(f"- Mois {i + 1} -> {j} : {sum(demandes[i:j]):,.0f} unités | Coût : {matrice[i][j]:,.2f} €")


if __name__ == "__main__":
    resoudre_et_afficher()