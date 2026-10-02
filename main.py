def lire_donnees(nom_fichier):
    with open(nom_fichier) as f:
        lignes = f.read().splitlines() # splitline sert principalement à supprimer les saut de lignes qui pourrait être conserver dans la list (/n) 

    cout_fixe = float(lignes[0])
    cout_stock = float(lignes[1])
    demandes = [float(e) for e in lignes[2].split()] # e (variable temporaire) correspond à chaque élément de la liste et pour chaque élément brut de la liste elle va le convertir en float, split quant à lui sert à découpé la chaine de caractere de façon à l'adapter en une liste python
    
    return cout_fixe, cout_stock, demandes


def verifier_circuit(matrice, N): # Définnisement d'une fonction avec des variables d'entrées avec N : Nombre total de mois.
    # set() crée un ensemble où l'on peut retirer des éléments facilement.
    # range(N + 1) génère la liste des numéros de sommets du mois 0 jusqu au mois N final.
    sommets_restants = set(range(N + 1)) 
    # Crée une copie pour chaque lignes de la matrice avec :
    mat = [ligne[:] for ligne in matrice]

    while sommets_restants:
        sources = [] # Créer une liste vide qui recueillera les sommets qui n'ont pas ou plus de prédécesseur
        
        for j in sommets_restants: # Pour chaque sommet dans l'ensemble sommets_restant
    
            a_un_predecesseur = any(mat[i][j] != float("inf") for i in sommets_restants) # Il existe au moins un sommet i restant qui pointe directement vers j 
            
            if not a_un_predecesseur:
                sources.append(j) # Sinon ajoute(append) le sommet qui n'a pas ou plus de prédécesseur dans la liste source

        if not sources:
            return True # Retourne vrai si il y à aucun sommet dans la liste source

        for s in sources:
            sommets_restants.remove(s) # Parcourt chaque sommet source identifié et le retire de l'ensemble des sommets restants
            
            # Efface tous les arcs sortants du sommet s en les passant à l'infini 
            mat[s] = [float("inf")] * (N + 1) 

    return False  # Aucun circuit détecté 


def resoudre_et_afficher():
    
    cout_fixe, cout_stock, demandes = lire_donnees("donne.txt")
    N = len(demandes)
    # initialisation d'une matrice en attribuant pour chaque ligne qui correspond au nombre N mois la valeur infini _= valeur qui est recopié N fois
    matrice = [[float("inf")] * (N + 1) for _ in range(N + 1)]
    
    # i : Mois où l'on effectue la commande
    for i in range(N):
        # j : Mois jusqu'auquel cette commande va couvrir la demande
        for j in range(i + 1, N + 1):
            cout_stockage = sum(demandes[k] * (k - i) * cout_stock for k in range(i, j))
            # Enregistre le coût total (fixe + stockage) pour la transition du mois i au mois j
            matrice[i][j] = cout_fixe + cout_stockage

    contient_circuit = verifier_circuit(matrice, N)

    if contient_circuit:
        print("Erreur : Le graphe contient un circuit. Impossible d'utiliser la programmation dynamique.")
        return

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
    
    
    curr = N
    while curr != -1: # Tant qu'il y à un prédécesseur alors on continue
        chemin.append(curr) # Ajoute le prédécesseur à chemin
        curr = predecesseur[curr] # Remonte au mois de commande optimal précédent
    chemin.reverse()

    # 6. Affichage des résultats
    print(f"Détection de circuit : {'Circuit détecté' if contient_circuit else 'Aucun circuit'}")
    print(f"Coût total optimal : {min_cost[N]} €\n")
    print("Planning optimal :")
    
    # k : Indice pour parcourir les étapes du chemin optimal
    for k in range(len(chemin) - 1):
        # i : Mois de début du lot de production | j : Mois de fin du lot
        i, j = chemin[k], chemin[k + 1]
        
        # qte : Somme des demandes cumulées à produire au mois i pour couvrir jusqu'en j
        qte = sum(demandes[i:j])
        
        print(f"- Mois {i + 1} -> {j} : {qte} unités | Coût : {matrice[i][j]} €")


if __name__ == "__main__":
    resoudre_et_afficher()
    
    
    #infini signifie qu'il n'existe aucun arc direct  entre ces deux sommet elle sert principalement à de l'initialisation pour ainsi être changé à nimporte quel moment.