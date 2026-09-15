def lire_donnees(nom_fichier):
    with open(nom_fichier) as f:
        lignes = [ligne for ligne in f if ligne]

    cout_fixe = float(lignes[0])
    cout_stock = float(lignes[1])
    demandes = [float(x) for x in lignes[2].split()]
    nombre_mois = len(demandes)

    return cout_fixe, cout_stock, demandes, nombre_mois


