# -*- coding: cp1252 -*-
################################################################################
#                                                                              #
#                                Tetris 3D                                     #
#                                                                              #
#           jeu de tetris en 3 dimensions avec la bibliothèque vPython         #
#                                                                              #
################################################################################

from visual import * # <- veillez à bien utiliser le raccourci bureau de vPython pour lancer ce script
from random import randrange
import pickle
from time import clock

#-------------------------------------------------------------------------------
def initialisation():
    """Méthode appelée une fois au lancement du script initialisant la scène de rendu, le menu écran, les information de jeu les cadres de jeu et les pièces."""
    global scene2,textScore,textNiveau,textLignes,textTop,textPerdu,textPause,tabMurs,tabCubes,tabCubesPiece,tabCubesPieceProjection,tabCubesNext,tabCouleurs,tabMatieres,indexMatiere,hauteur,largeur,indiceResolution,tabdimCube,posXoNext,posYoNext,premierePartie,tabPieces

    #------------------------ la scène -----------------------------
    scene2 = display(title='TetrisPythonPrincipe3D',x=0, y=0, width=600, height=600,center=(5,0,0), background=(0,0,0))
    scene2.visible = False
    scene2.fullscreen = True
    scene2.bind('keydown',key_input)
    scene2.bind('keyup',key_input2)
    scene2.visible = True

    #------------------------ le menu gauche -----------------------------
    menu = text(pos=(-300,240,0),text="N - Nouvelle Partie\n\nR - Résolution\n\nP - Pause\n\nA - Aide\n\nM - Matière\n\nC - Clignotement", height= 24,align='center', depth=-10, color=color.blue)
    
    titreScore = text(pos=(250,70,0),text="SCORE", height= 26,align='center', depth=-10, color=color.blue)
    textScore = text(pos=(250,30,0),text="0", height= 24,align='center', depth=-10, color=color.white)

    #------------------------ informations de jeu -----------------------------
    titreNiveau = text(pos=(250,-30,0),text="NIVEAU", height= 26,align='center', depth=-10, color=color.blue)
    textNiveau = text(pos=(250,-70,0),text="1", height= 24,align='center', depth=-10, color=color.white)

    titreLignes = text(pos=(250,-130,0),text="LIGNES", height= 26,align='center', depth=-10, color=color.blue)
    textLignes = text(pos=(250,-170,0),text="0", height= 24,align='center', depth=-10, color=color.white)    

    titreTop = text(pos=(250,-230,0),text="TOP", height= 26,align='center', depth=-10, color=color.blue)
    textTop = text(pos=(250,-270,0),text="0", height= 26,align='center', depth=-10, color=color.white)

    textPerdu = text(pos=(0,0,15),text="GAME OVER", height= 26,align='center', depth=10, color=color.white)
    textPerdu.visible = False

    textPause = text(pos=(0,0,15),text="PAUSE", height= 26,align='center', depth=10, color=color.white)
    textPause.visible = False
    
    #--- variables de rendu graphique ---------------------------------------
    tabCouleurs = [0,(0,1,0.5),(0.5,1,0),(1,0,0),(0.5,0.5,1),(1,0.5,0),(0,0.5,1),(0,0,1)]
    tabMatieres = [materials.wood,materials.rough,materials.marble,materials.plastic,materials.earth,materials.diffuse,materials.emissive,materials.unshaded]
    indexMatiere = 0
    
    hauteur = 520
    largeur = 260
    indiceResolution = 0
    tabdimCube = [26,20,13,10]
    dimCube = tabdimCube[indiceResolution]

    #------------------------ cadres du jeu et de la pièce suivante -----------------------------
    #--- cadre du jeu
    tabMurs = []
    murGauche = box(pos=(-139,0,0),size=(18,520,dimCube),color=color.orange,material=materials.wood)
    murDroit = box(pos=(139,0,0),size=(18,520,dimCube),color=color.orange,material=materials.wood)
    murBas = box(pos=(0,-269,0),size=(296,18,dimCube),color=color.orange,material=materials.wood)
    tabMurs.append(murGauche)
    tabMurs.append(murDroit)
    tabMurs.append(murBas)
    #--- cadre de la pièce suivante
    posXoNext, posYoNext = 250, (260-10-52)
    murGaucheNext = box(pos=(posXoNext-52-5,posYoNext,0),size=(10,104,dimCube),color=color.white,material=materials.wood)
    murDroitNext = box(pos=(posXoNext+52+5,posYoNext,0),size=(10,104,dimCube),color=color.white,material=materials.wood)
    murHautNext = box(pos=(posXoNext,posYoNext+52+5,0),size=(104+10+10,10,dimCube),color=color.white,material=materials.wood)
    murBasNext = box(pos=(posXoNext,posYoNext-52-5,0),size=(104+10+10,10,dimCube),color=color.white,material=materials.wood)

    #--- tableau contenant les différents cubes créés, afin de pouvoir les supprimer de la scène
    tabCubes = [] #<- pour le jeu
    tabCubesPiece = []
    tabCubesPieceProjection = []    
    tabCubesNext = [] #<- pour la pièce suivante
    
    #----- Définition des pièces --------------------------------------------------#                                           
    piece1 =[[[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,0,0]],#<-1ere orientation-> O
                   [[0,0,0,0],[0,0,1,1],[0,1,1,0],[0,0,0,0]],#2eme           O O 
                   [[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,0,0]],#3eme             O  
                   [[0,0,0,0],[0,0,1,1],[0,1,1,0],[0,0,0,0]]]#4eme          

    piece2 = [[[0,0,2,0],[0,2,2,0],[0,2,0,0],[0,0,0,0]],        #     O 
                 [[0,0,0,0],[0,2,2,0],[0,0,2,2],[0,0,0,0]],     #   O O 
                 [[0,0,2,0],[0,2,2,0],[0,2,0,0],[0,0,0,0]],     #   O  
                 [[0,0,0,0],[0,2,2,0],[0,0,2,2],[0,0,0,0]]]     

    piece3 = [[[0,3,0,0],[0,3,0,0],[0,3,0,0],[0,3,0,0]],        #   O 
                [[3,3,3,3],[0,0,0,0],[0,0,0,0],[0,0,0,0]],      #   O 
                [[0,3,0,0],[0,3,0,0],[0,3,0,0],[0,3,0,0]],      #   O 
                [[3,3,3,3],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]      #   O 

    piece4 = [[[0,4,4,0],[0,4,4,0],[0,0,0,0],[0,0,0,0]],        #   O O 
                 [[0,4,4,0],[0,4,4,0],[0,0,0,0],[0,0,0,0]],     #   O O 
                 [[0,4,4,0],[0,4,4,0],[0,0,0,0],[0,0,0,0]],       
                 [[0,4,4,0],[0,4,4,0],[0,0,0,0],[0,0,0,0]]]      

    piece5 = [[[0,5,0,0],[0,5,5,0],[0,5,0,0],[0,0,0,0]],        #   O 
                 [[0,0,0,0],[0,0,5,0],[0,5,5,5],[0,0,0,0]],     #   O O 
                 [[0,0,0,5],[0,0,5,5],[0,0,0,5],[0,0,0,0]],     #   O 
                 [[0,5,5,5],[0,0,5,0],[0,0,0,0],[0,0,0,0]]]     

    piece6 = [[[0,0,6,0],[0,0,6,0],[0,6,6,0],[0,0,0,0]],        #     O 
                 [[0,0,0,0],[0,6,6,6],[0,0,0,6],[0,0,0,0]],     #     O
                 [[0,6,6,0],[0,6,0,0],[0,6,0,0],[0,0,0,0]],     #   O O 
                 [[0,0,0,0],[0,6,0,0],[0,6,6,6],[0,0,0,0]]]     

    piece7 = [[[0,7,0,0],[0,7,0,0],[0,7,7,0],[0,0,0,0]],        #   O
                 [[0,0,0,0],[0,0,0,7],[0,7,7,7],[0,0,0,0]],     #   O
                 [[0,7,7,0],[0,0,7,0],[0,0,7,0],[0,0,0,0]],     #   O O 
                 [[0,0,0,0],[0,7,7,7],[0,7,0,0],[0,0,0,0]]]     

    tabPieces =(piece1,piece2,piece3,piece4,piece5,piece6,piece7)

    premierePartie = True # cette variable ne donnera accès qu'à la touche 'n'(nouvelle partie) lors du premier lancement(cf:KeyInput())
    
    # les variables de rendu graphique viennent d'être initialisées pour la 1ère fois
    # cependant on opère comme si un changement de résolution venait d'avoir lieu
    # ceci afin de reduire la taille du code
    changement_resolution()  

#-------------------------------------------------------------------------------
def changement_resolution():
    """Méthode qui modifie la taille de la matrice en fonction de l'indice de résolution."""
    global dimCube,nbrLignesTotales,nbrColonnesTotales,matriceJeu

    dimCube = tabdimCube[indiceResolution]
    nbrLignesTotales = 520/dimCube
    nbrColonnesTotales = 260/dimCube

    matriceJeu = []
    for i in range(nbrLignesTotales):
        matriceJeu.append([0]*nbrColonnesTotales)

    # les murs du jeu prennent une profondeur égale à celle d'un cube
    for mur in tabMurs:
        mur.width = dimCube

    dessine_bloques()

    charger_top() #<- chargement du top score correspondant à la résolution choisie

#-------------------------------------------------------------------------------
def sauver_top():
    """Sauvegarde du score maximum"""
    #tableauTop = [0,0,0,0]
    fichier = open('top4Resol','w')
    pickle.dump(tableauTop,fichier)
    fichier.close()
    textTop.text = str(tableauTop[indiceResolution])
    
#-------------------------------------------------------------------------------
def charger_top():
    """Chargement du score maximum"""
    global top,tableauTop
    
    fichier = open("top4Resol",'r')
    tableauTop = pickle.load(fichier)
    top = tableauTop[indiceResolution]
    fichier.close()
    textTop.text = str(top)

#-------------------------------------------------------------------------------
def tirage_affichage_piece_suivante():
    """Tirage au hazard d'une pièce mémorisée dans pieceSuivante.
       Affichage de cette pièce dans la partie information.Lorsque la pièce
       courante ne peut plus descendre, cette pièce devient la pièce courante"""
    global pieceSuivante,tabCubesNext
    
    index = randrange(0,len(tabPieces))
    pieceSuivante = tabPieces[index]

    for cube in tabCubesNext:
        cube.visible = False
        del cube
    tabCubesNext = []
        
    for ligne in range(4):
        for colonne in range(4):
            if pieceSuivante[0][ligne][colonne] == 0:
                continue
            couleur = tabCouleurs[pieceSuivante[0][ligne][colonne]]
            cube = box(pos=(posXoNext-52+(colonne*26)+(dimCube/2),posYoNext+52-(ligne*26)-(26/2),0),size=(26-1,26-1,26-1),color=couleur,material=tabMatieres[indexMatiere])
            tabCubesNext.append(cube)

#-------------------------------------------------------------------------------
def nouvelle_partie():
    """A chaque nouvelle partie on réinitialise la matrice et certaines
       variables de jeu.On tire au hazard une pièce mémorisée dans pieceCourante."""
    global pieceCourante,pieceSuivante,matriceJeu,tabCubes,tabCubesPiece,tabCubesPieceProjection,score,niveau,nbrLignes,aide,pause,cligno,partieTerminee,premierePartie

    pieceCourante = []
    pieceSuivante = []    
    for ligne in range(nbrLignesTotales):
        for colonne in range(nbrColonnesTotales):
            matriceJeu[ligne][colonne] = 0

    #--- on efface tous les cubes de l'écran et on vide les tableaux qui les contiennent
    for cube in tabCubes:
        cube.visible = False
        del cube
    tabCubes = []

    for cube in tabCubesPiece:
        cube.visible = False
        del cube
    tabCubesPiece = []

    for cube in tabCubesPieceProjection:
        cube.visible = False
        del cube
    tabCubesPieceProjection = []
    #---
    
    score = 0
    textScore.text = '0'

    niveau = 1
    textNiveau.text = '1'    
  
    nbrLignes = 0
    textLignes.text = '0'

    textPerdu.visible = False
    
    index = randrange(0,len(tabPieces))
    pieceCourante = tabPieces[index]

    aide = True
    pause = False
    cligno = True
    
    partieTerminee = True
    premierePartie = False

    nouvelle_piece()

#-------------------------------------------------------------------------------    
def nouvelle_piece():
    """ Mise en place d'une nouvelle pièce dans l'air de jeu.""" 
    global coordCourante,sens,vitesse,tabCubesPiece,tabCubesPieceProjection,pause,top,tempsInit,partieTerminee

    # C'est par le biais de coordCourante que l'on va se déplacer
    # dans la matrice soit horizontalement (gauche:decalColonne=-1,droite:decalColonne=1)
    # soit verticalement (descente:decalLigne=1)
    coordCourante = [0,(nbrColonnesTotales/2)-2]

    # 'Sens' représente l'indice de l'orientation de la pièce courante 
    sens = 0

    # La vitesse de descente est dépendante du niveau    
    vitesse = 1.05 - (niveau*0.05)

    # On détermine la pièce suivante
    tirage_affichage_piece_suivante()  

    tabCubesPiece = []
    tabCubesPieceProjection = []
    
    # A cet instant, si la pièce courante ne peut être imprimée dans la matrice, alors
    # la partie est terminée
    if not verif_deplacement(0,0,0,coordCourante):
        partieTerminee = True
        dessine_piece()
        textPerdu.visible = True           
        if score > top:
            top = score
            tableauTop[indiceResolution] = top
            sauver_top()
    # Sinon on fait partir la boucle de descente
    else :
        if aide:
            projection_image()
        dessine_piece()
        tempsInit = clock()
        pause = False
        if partieTerminee:
            partieTerminee = False
            cycle()

#-------------------------------------------------------------------------------  
def projection_image():
    """Avant n'importe quel déplacement de la pièce courante, une image de celle-ci est
       projetée jusqu'à sa position la plus basse atteignable par rapport à la verticale
       de la pièce."""
    global coordCouranteImage

    # On positionne la pièce image aux coordonées de la pièce courante
    coordCouranteImage = coordCourante[:]

    # On déplace la pièce image de ligne en ligne tant que c'est possible
    while verif_deplacement(1,0,0,coordCouranteImage):
        coordCouranteImage[0] += 1

    # Puis on la dessine
    dessine_projection()

#-------------------------------------------------------------------------------  
def cycle():
    """Boucle qui compare l'instant t à l'instant de la dernière position d'une pièce.
    et ce à une fréquence de f = rate(n) = 1/n. Quand leur différence dépasse la vitesse
    du niveau la pièce essaie de descendre."""
    global pause,tempsPresent
    
    while not partieTerminee:
        rate(50)
        tempsPresent = clock()
        if tempsPresent - tempsInit >= vitesse and not pause:
            pause = True
            descente()
    
#-------------------------------------------------------------------------------    
def descente():
    """Appelée par la méthode cycle quand l'interval de temps entre 2 positions de descente
    est atteint, cette méthode est chargée de faire descendre la pièce d'une ligne si c'est possible."""
    global coordCourante,tempsInit,pause,pieceCourante

    if verif_deplacement(1,0,0,coordCourante):
        coordCourante[0] += 1
        dessine_piece()        
        tempsInit = clock()
        pause = False
    else :
        imprime_piece()
        verif_ligne_complete()
        pieceCourante = pieceSuivante
        nouvelle_piece()

#-------------------------------------------------------------------------------
def imprime_piece():
    """Quand la pièce ne peut plus descendre, on l'imprime dans la matrice par rapport à sa coordonnée courante."""
    global tabCubes
    
    for ligne in range(4):
        for colonne in range(4):
            if pieceCourante[sens][ligne][colonne] != 0:
                matriceJeu[coordCourante[0]+ligne][coordCourante[1]+colonne] = pieceCourante[sens][ligne][colonne]

    # on ajoute le tableau de cubes de la pièce a celui de tous les cubes de l'air de jeu pour pouvoir les effacer
    # via la méthode 'dessine_bloques', quand au moins une ligne sera complète. Sinon ils seront toujours visibles,
    # à moins de les effacer ici mais de faire appel à 'dessine_bloques' après chaque pose de pièce (un peu lourd).
    tabCubes.extend(tabCubesPiece) 

    # on efface la projection
    for cube in tabCubesPieceProjection:
        cube.visible = False
        del cube
        
#-------------------------------------------------------------------------------            
def verif_deplacement(decalLigne,decalColonne,pivot,coord):
    """Vérification par anticipation de la possibilité de déplacement de la pièce ou sa projection."""

##       verif_deplacement(1,0,0,coord) : déplacement vers le bas possible ?
##       verif_deplacement(0,-1,0,coord) : déplacement vers la gauche possible ?
##       verif_deplacement(0,1,0,coord) : déplacement vers la droite possible ?
##       verif_deplacement(0,0,1,coord) : rotation possible ?

##       Pour chaque vérification, on se place à la coordonnée courante de la pièce(ou projection)
##       à laquelle on ajoute le décalage demandé (dans le cas de la rotation aucun décalage, on prend
##       la définition suivante de la pièce en cours).    
##       Puis on boucle en ligne et colonne dans celle-ci(par itération) et pour chaque valeur différente
##       de zéro on vérifie si on sort pas de la matrice de jeu et sinon, si la pièce ne chevauchera pas une pièce déja placée.

    rotation = sens + pivot
    if rotation == 4:
        rotation = 0

    for ligne in range(4):
        for colonne in range(4):
            if pieceCourante[rotation][ligne][colonne] != 0:            
                if (coord[1]+decalColonne)+colonne > nbrColonnesTotales-1 or (coord[1]+decalColonne)+colonne < 0 \
                   or (coord[0]+decalLigne)+ligne > nbrLignesTotales-1:
                    return False
                elif (pieceCourante[rotation][ligne][colonne] * matriceJeu[(coord[0]+decalLigne)+ligne][(coord[1]+decalColonne)+colonne]) != 0 :
                   return False
    return True

#-------------------------------------------------------------------------------
def dessine_piece():
    """Méthode qui redessine la pièce après chaque changement de coordonnée matricielle."""    
    global tabCubesPiece

    for cubePiece in tabCubesPiece:
        cubePiece.visible = False
        del cubePiece
    tabCubesPiece = []
    
    for indiceLigne in range(len(pieceCourante[sens])):
        for indiceColonne in range(len(pieceCourante[sens][0])):
            if pieceCourante[sens][indiceLigne][indiceColonne] != 0:
                couleur = tabCouleurs[pieceCourante[sens][indiceLigne][indiceColonne]]
                cube = box(pos=(-130+((coordCourante[1]+indiceColonne)*dimCube)+(dimCube/2),260-((coordCourante[0]+indiceLigne)*dimCube)-(dimCube/2),0),size=(dimCube-1,dimCube-1,dimCube-1),color=couleur,material=tabMatieres[indexMatiere])
                tabCubesPiece.append(cube)

#-------------------------------------------------------------------------------
def dessine_projection():
    """Méthode qui redessine la projection de la pièce lorsque sa coordonnée matricielle la plus basse a été trouvée."""    
    global tabCubesPieceProjection

    for cube in tabCubesPieceProjection:
        cube.visible = False
        del cube
    tabCubesPieceProjection = []

    for indiceLigne in range(len(pieceCourante[sens])):
        for indiceColonne in range(len(pieceCourante[sens][0])):
            if pieceCourante[sens][indiceLigne][indiceColonne] != 0:
                couleur = tabCouleurs[pieceCourante[sens][indiceLigne][indiceColonne]]
                cube = box(pos=(-130+((coordCouranteImage[1]+indiceColonne)*dimCube)+(dimCube/2),260-((coordCouranteImage[0]+indiceLigne)*dimCube)-(dimCube/2),0),size=(dimCube-1,dimCube-1,dimCube-1),color=couleur,opacity=0.2,material=tabMatieres[indexMatiere])
                tabCubesPieceProjection.append(cube)

#-------------------------------------------------------------------------------
def dessine_bloques():
    """Méthode qui met à jour le rendu graphique en fonction des changements effectués dans la matrice."""
    global tabCubes,tempsInit,pause

    # on commence par effacer tous les cubes de l'écran
    for cube in tabCubes:
        cube.visible = False
        del cube
    tabCubes = []

    # pour chaque valeur de la matrice différent de 0, on crée un cube
    for ligne in range(nbrLignesTotales):
        for colonne in range(nbrColonnesTotales):
            if matriceJeu[ligne][colonne] != 0 :
                couleur = tabCouleurs[matriceJeu[ligne][colonne]]                
                cube = box(pos=(-130+(colonne*dimCube)+(dimCube/2),260-(ligne*dimCube)-(dimCube/2),0),size=(dimCube-1,dimCube-1,dimCube-1),color=couleur,material=tabMatieres[indexMatiere])
                tabCubes.append(cube)

#-------------------------------------------------------------------------------
def verif_ligne_complete():
    """Quand une pièce est posée on verifie les lignes complètes."""
    global tabLignesCompletes,nbrLignes,score,niveau
    
    # variable mémorisant les points pour l'ensemble des lignes completées lors de cette vérification
    points = 0
    # tableau contenant toutes les lignes complètes et leur indice(pour l'animation)
    tabLignesCompletes = []
    
    # On analyse chaque ligne de la matrice
    for indiceLigne in range(nbrLignesTotales):
        if 0 not in matriceJeu[indiceLigne]:  #<- si dans une ligne de la matrice,le chiffre '0' n'est pas présent: cette ligne est complète
            tabLignesCompletes.append((matriceJeu[indiceLigne],indiceLigne))

    # Si le tableau de lignes complètes n'est pas vide
    if tabLignesCompletes:
        # si mode clignotement actif
        if cligno :
            finCligno = False
            tempsInit = clock()
            visible = False        
            nbrCligno = 0
            while not finCligno:
                rate(50)
                tempsPresent = clock()
                if tempsPresent - tempsInit > 0.04:
                    clignotement(visible)
                    nbrCligno += 1                
                    visible = not visible
                    tempsInit = clock()
                    if nbrCligno == 5:
                        finCligno = True

        # Puis on compte les points en fonction de l'indice de la ligne(+1 ainsi indice 19 donne 20points) multiplié par 10
        # plus elle est basse dans le jeu plus on a de points
        for memoire in tabLignesCompletes:
            points += (memoire[1]+1)*10
            nbrLignes += 1
            # Quand l'ajout d'une ligne dépasse un multiple de 20 on change de niveau
            if nbrLignes % 20 == 0:
                niveau += 1
                textNiveau.text = str(niveau)
            # On supprime la ligne et on ajoute une ligne de zéro au debut de la matrice    
            del matriceJeu[memoire[1]]
            matriceJeu[0:0]=[[0]*nbrColonnesTotales]

        # On redessine tout
        dessine_bloques()

        # Bonus lorsqu'on complète plusieurs lignes : les points sont multipliés par le nombre de lignes
        points *= len(tabLignesCompletes)
        score += points
        textScore.text = str(score)
        textLignes.text = str(nbrLignes)

def clignotement(visible = True):
    """Effet de clignotement.Les lignes complètes sont simultanement et succesivement remplacée
    par des zéro puis par elle-même."""
    for memoire in tabLignesCompletes:
        if visible:
            matriceJeu[memoire[1]] = memoire[0]
        else:
            matriceJeu[memoire[1]] = [0]*nbrColonnesTotales
    dessine_bloques()

#-------------------------------------------------------------------------------
#                 Gestion des évènements clavier
#-------------------------------------------------------------------------------
def key_input(evt):
    """Méthode qui s'occupe de switch vers la fonction correspondant à la touche pressée."""
    global partieTerminee
    
    s = evt.key

    if s == 'n':
        nouvelle_partie()
    if not premierePartie:
        if not pause:
            if s == 'left':
                gauche()
            if s == 'right':
                droite()
            if s == 'up':
                tourne()
            if s == 'down':
                acceleration()
            if s == ' ':
                tombe()
                
        if not partieTerminee:
            if s == 'p':
                pause_on_off()
            if s == 'a':
                aide_on_off()
            if s == 'c':
                clignotement_on_off()
               
        if s == 'r':
            partieTerminee = True
            choix_resolution()
            nouvelle_partie()

        if s == 'm':
            changement_matiere()

def key_input2(evt):
    """Méthode qui s'occupe de switch vers la fonction correspondant à la touche relachée."""    

    s = evt.key
    if s== 'down':
        acceleration_relachee()
    
#-------------------------------------------------------------------------------
def acceleration():
    """Touche BAS appuyée : augmentation de la vitesse."""
    global vitesse
    
    vitesse = 0.01

#-------------------------------------------------------------------------------
def acceleration_relachee():
    """Touche BAS relachée : la vitesse prend sa valeur déterminée par le niveau."""
    global vitesse

    vitesse = 1.05 - (niveau*0.05)

#-------------------------------------------------------------------------------  
def tombe():
    """Touche ESPACE appuyée : la pièce tombe."""
    global pause,coordCourante,pieceCourante

    pause = True
    while verif_deplacement(1,0,0,coordCourante):
        coordCourante[0] += 1

    dessine_piece()
    imprime_piece()
    verif_ligne_complete()
    pieceCourante = pieceSuivante
    nouvelle_piece()                
    
#-------------------------------------------------------------------------------
def tourne():
    """Touche HAUT : si c'est possible la pièce tourne."""
    global sens
 
    if verif_deplacement(0,0,1,coordCourante):
        sens += 1
        if sens == 4:
            sens = 0
        if aide:
            projection_image() # Si la pièce peut tourner on recalcule les coordonnées de sa projection image 
        dessine_piece()        

#-------------------------------------------------------------------------------
def gauche():
    """Touche Gauche : si c'est possible la pièce se déplace d'une colonne vers la gauche."""
    global coordCourante

    if verif_deplacement(0,-1,0,coordCourante):
        coordCourante[1] -= 1
        if aide:
            projection_image() # Si la pièce peut se déplacer on recalcule les coordonnées de sa projection image 
        dessine_piece()        

#-------------------------------------------------------------------------------
def droite():
    """Touche Droite : si c'est possible la pièce se déplace d'une colonne vers la droite."""
    global coordCourante
    
    if verif_deplacement(0,1,0,coordCourante):
        coordCourante[1] += 1
        if aide:
            projection_image() # Si la pièce peut se déplacer on recalcule les coordonnées de sa projection image 
        dessine_piece()        

#-------------------------------------------------------------------------------
def pause_on_off():
    """Met le jeu en pause."""
    global pause

    if pause:
        pause = False
        textPause.visible = False
        for cube in tabCubes:
            cube.visible = True
        for cube in tabCubesPiece:
            cube.visible = True
        for cube in tabCubesPieceProjection:
            cube.visible = True
    else:
        pause = True
        textPause.visible = True
        for cube in tabCubes:
            cube.visible = False
        for cube in tabCubesPiece:
            cube.visible = False
        for cube in tabCubesPieceProjection:
            cube.visible = False
            
#-------------------------------------------------------------------------------
def choix_resolution():
    """Méthode qui incrémente l'indice de résolution."""
    global indiceResolution,pause

    pause = True
    indiceResolution += 1
    if indiceResolution == 4:
        indiceResolution = 0

    changement_resolution()

#-------------------------------------------------------------------------------    
def aide_on_off():
    """Affiche ou non la projection de la pièce."""
    global aide,tabCubesPieceProjection

    if aide:
        aide = False
        if tabCubesPieceProjection:
            for cube in tabCubesPieceProjection:
                cube.visible = False
                del cube
            tabCubesPieceProjection = []
            
    else:
        aide = True
        projection_image()

#-------------------------------------------------------------------------------
def changement_matiere():
    """Incrémente l'indice du choix de la matière dans le tableau les contenant."""
    global indexMatiere

    indexMatiere += 1 
    if indexMatiere == len(tabMatieres):
        indexMatiere = 0
    for cube in tabCubes:
        cube.material = tabMatieres[indexMatiere]
    
    for cube in tabCubesNext:
        cube.material = tabMatieres[indexMatiere]

#-------------------------------------------------------------------------------
def clignotement_on_off():
    """Active ou non le clignotement des lignes complètes."""
    global cligno

    cligno = not cligno
        
initialisation()
