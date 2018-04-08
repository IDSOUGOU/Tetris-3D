# -*- coding: cp1252 -*-
################################################################################
#                                                                              #
#                                Tetris 3D                                     #
#                                                                              #
#           jeu de tetris en 3 dimensions avec la biblioth�que vPython         #
#                                                                              #
################################################################################

from visual import * # <- veillez � bien utiliser le raccourci bureau de vPython pour lancer ce script
from random import randrange
import pickle
from time import clock

#-------------------------------------------------------------------------------
def initialisation():
    """M�thode appel�e une fois au lancement du script initialisant la sc�ne de rendu, le menu �cran, les information de jeu les cadres de jeu et les pi�ces."""
    global scene2,textScore,textNiveau,textLignes,textTop,textPerdu,textPause,tabMurs,tabCubes,tabCubesPiece,tabCubesPieceProjection,tabCubesNext,tabCouleurs,tabMatieres,indexMatiere,hauteur,largeur,indiceResolution,tabdimCube,posXoNext,posYoNext,premierePartie,tabPieces

    #------------------------ la sc�ne -----------------------------
    scene2 = display(title='TetrisPythonPrincipe3D',x=0, y=0, width=600, height=600,center=(5,0,0), background=(0,0,0))
    scene2.visible = False
    scene2.fullscreen = True
    scene2.bind('keydown',key_input)
    scene2.bind('keyup',key_input2)
    scene2.visible = True

    #------------------------ le menu gauche -----------------------------
    menu = text(pos=(-300,240,0),text="N - Nouvelle Partie\n\nR - R�solution\n\nP - Pause\n\nA - Aide\n\nM - Mati�re\n\nC - Clignotement", height= 24,align='center', depth=-10, color=color.blue)
    
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

    #------------------------ cadres du jeu et de la pi�ce suivante -----------------------------
    #--- cadre du jeu
    tabMurs = []
    murGauche = box(pos=(-139,0,0),size=(18,520,dimCube),color=color.orange,material=materials.wood)
    murDroit = box(pos=(139,0,0),size=(18,520,dimCube),color=color.orange,material=materials.wood)
    murBas = box(pos=(0,-269,0),size=(296,18,dimCube),color=color.orange,material=materials.wood)
    tabMurs.append(murGauche)
    tabMurs.append(murDroit)
    tabMurs.append(murBas)
    #--- cadre de la pi�ce suivante
    posXoNext, posYoNext = 250, (260-10-52)
    murGaucheNext = box(pos=(posXoNext-52-5,posYoNext,0),size=(10,104,dimCube),color=color.white,material=materials.wood)
    murDroitNext = box(pos=(posXoNext+52+5,posYoNext,0),size=(10,104,dimCube),color=color.white,material=materials.wood)
    murHautNext = box(pos=(posXoNext,posYoNext+52+5,0),size=(104+10+10,10,dimCube),color=color.white,material=materials.wood)
    murBasNext = box(pos=(posXoNext,posYoNext-52-5,0),size=(104+10+10,10,dimCube),color=color.white,material=materials.wood)

    #--- tableau contenant les diff�rents cubes cr��s, afin de pouvoir les supprimer de la sc�ne
    tabCubes = [] #<- pour le jeu
    tabCubesPiece = []
    tabCubesPieceProjection = []    
    tabCubesNext = [] #<- pour la pi�ce suivante
    
    #----- D�finition des pi�ces --------------------------------------------------#                                           
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

    premierePartie = True # cette variable ne donnera acc�s qu'� la touche 'n'(nouvelle partie) lors du premier lancement(cf:KeyInput())
    
    # les variables de rendu graphique viennent d'�tre initialis�es pour la 1�re fois
    # cependant on op�re comme si un changement de r�solution venait d'avoir lieu
    # ceci afin de reduire la taille du code
    changement_resolution()  

#-------------------------------------------------------------------------------
def changement_resolution():
    """M�thode qui modifie la taille de la matrice en fonction de l'indice de r�solution."""
    global dimCube,nbrLignesTotales,nbrColonnesTotales,matriceJeu

    dimCube = tabdimCube[indiceResolution]
    nbrLignesTotales = 520/dimCube
    nbrColonnesTotales = 260/dimCube

    matriceJeu = []
    for i in range(nbrLignesTotales):
        matriceJeu.append([0]*nbrColonnesTotales)

    # les murs du jeu prennent une profondeur �gale � celle d'un cube
    for mur in tabMurs:
        mur.width = dimCube

    dessine_bloques()

    charger_top() #<- chargement du top score correspondant � la r�solution choisie

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
    """Tirage au hazard d'une pi�ce m�moris�e dans pieceSuivante.
       Affichage de cette pi�ce dans la partie information.Lorsque la pi�ce
       courante ne peut plus descendre, cette pi�ce devient la pi�ce courante"""
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
    """A chaque nouvelle partie on r�initialise la matrice et certaines
       variables de jeu.On tire au hazard une pi�ce m�moris�e dans pieceCourante."""
    global pieceCourante,pieceSuivante,matriceJeu,tabCubes,tabCubesPiece,tabCubesPieceProjection,score,niveau,nbrLignes,aide,pause,cligno,partieTerminee,premierePartie

    pieceCourante = []
    pieceSuivante = []    
    for ligne in range(nbrLignesTotales):
        for colonne in range(nbrColonnesTotales):
            matriceJeu[ligne][colonne] = 0

    #--- on efface tous les cubes de l'�cran et on vide les tableaux qui les contiennent
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
    """ Mise en place d'une nouvelle pi�ce dans l'air de jeu.""" 
    global coordCourante,sens,vitesse,tabCubesPiece,tabCubesPieceProjection,pause,top,tempsInit,partieTerminee

    # C'est par le biais de coordCourante que l'on va se d�placer
    # dans la matrice soit horizontalement (gauche:decalColonne=-1,droite:decalColonne=1)
    # soit verticalement (descente:decalLigne=1)
    coordCourante = [0,(nbrColonnesTotales/2)-2]

    # 'Sens' repr�sente l'indice de l'orientation de la pi�ce courante 
    sens = 0

    # La vitesse de descente est d�pendante du niveau    
    vitesse = 1.05 - (niveau*0.05)

    # On d�termine la pi�ce suivante
    tirage_affichage_piece_suivante()  

    tabCubesPiece = []
    tabCubesPieceProjection = []
    
    # A cet instant, si la pi�ce courante ne peut �tre imprim�e dans la matrice, alors
    # la partie est termin�e
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
    """Avant n'importe quel d�placement de la pi�ce courante, une image de celle-ci est
       projet�e jusqu'� sa position la plus basse atteignable par rapport � la verticale
       de la pi�ce."""
    global coordCouranteImage

    # On positionne la pi�ce image aux coordon�es de la pi�ce courante
    coordCouranteImage = coordCourante[:]

    # On d�place la pi�ce image de ligne en ligne tant que c'est possible
    while verif_deplacement(1,0,0,coordCouranteImage):
        coordCouranteImage[0] += 1

    # Puis on la dessine
    dessine_projection()

#-------------------------------------------------------------------------------  
def cycle():
    """Boucle qui compare l'instant t � l'instant de la derni�re position d'une pi�ce.
    et ce � une fr�quence de f = rate(n) = 1/n. Quand leur diff�rence d�passe la vitesse
    du niveau la pi�ce essaie de descendre."""
    global pause,tempsPresent
    
    while not partieTerminee:
        rate(50)
        tempsPresent = clock()
        if tempsPresent - tempsInit >= vitesse and not pause:
            pause = True
            descente()
    
#-------------------------------------------------------------------------------    
def descente():
    """Appel�e par la m�thode cycle quand l'interval de temps entre 2 positions de descente
    est atteint, cette m�thode est charg�e de faire descendre la pi�ce d'une ligne si c'est possible."""
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
    """Quand la pi�ce ne peut plus descendre, on l'imprime dans la matrice par rapport � sa coordonn�e courante."""
    global tabCubes
    
    for ligne in range(4):
        for colonne in range(4):
            if pieceCourante[sens][ligne][colonne] != 0:
                matriceJeu[coordCourante[0]+ligne][coordCourante[1]+colonne] = pieceCourante[sens][ligne][colonne]

    # on ajoute le tableau de cubes de la pi�ce a celui de tous les cubes de l'air de jeu pour pouvoir les effacer
    # via la m�thode 'dessine_bloques', quand au moins une ligne sera compl�te. Sinon ils seront toujours visibles,
    # � moins de les effacer ici mais de faire appel � 'dessine_bloques' apr�s chaque pose de pi�ce (un peu lourd).
    tabCubes.extend(tabCubesPiece) 

    # on efface la projection
    for cube in tabCubesPieceProjection:
        cube.visible = False
        del cube
        
#-------------------------------------------------------------------------------            
def verif_deplacement(decalLigne,decalColonne,pivot,coord):
    """V�rification par anticipation de la possibilit� de d�placement de la pi�ce ou sa projection."""

##       verif_deplacement(1,0,0,coord) : d�placement vers le bas possible ?
##       verif_deplacement(0,-1,0,coord) : d�placement vers la gauche possible ?
##       verif_deplacement(0,1,0,coord) : d�placement vers la droite possible ?
##       verif_deplacement(0,0,1,coord) : rotation possible ?

##       Pour chaque v�rification, on se place � la coordonn�e courante de la pi�ce(ou projection)
##       � laquelle on ajoute le d�calage demand� (dans le cas de la rotation aucun d�calage, on prend
##       la d�finition suivante de la pi�ce en cours).    
##       Puis on boucle en ligne et colonne dans celle-ci(par it�ration) et pour chaque valeur diff�rente
##       de z�ro on v�rifie si on sort pas de la matrice de jeu et sinon, si la pi�ce ne chevauchera pas une pi�ce d�ja plac�e.

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
    """M�thode qui redessine la pi�ce apr�s chaque changement de coordonn�e matricielle."""    
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
    """M�thode qui redessine la projection de la pi�ce lorsque sa coordonn�e matricielle la plus basse a �t� trouv�e."""    
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
    """M�thode qui met � jour le rendu graphique en fonction des changements effectu�s dans la matrice."""
    global tabCubes,tempsInit,pause

    # on commence par effacer tous les cubes de l'�cran
    for cube in tabCubes:
        cube.visible = False
        del cube
    tabCubes = []

    # pour chaque valeur de la matrice diff�rent de 0, on cr�e un cube
    for ligne in range(nbrLignesTotales):
        for colonne in range(nbrColonnesTotales):
            if matriceJeu[ligne][colonne] != 0 :
                couleur = tabCouleurs[matriceJeu[ligne][colonne]]                
                cube = box(pos=(-130+(colonne*dimCube)+(dimCube/2),260-(ligne*dimCube)-(dimCube/2),0),size=(dimCube-1,dimCube-1,dimCube-1),color=couleur,material=tabMatieres[indexMatiere])
                tabCubes.append(cube)

#-------------------------------------------------------------------------------
def verif_ligne_complete():
    """Quand une pi�ce est pos�e on verifie les lignes compl�tes."""
    global tabLignesCompletes,nbrLignes,score,niveau
    
    # variable m�morisant les points pour l'ensemble des lignes complet�es lors de cette v�rification
    points = 0
    # tableau contenant toutes les lignes compl�tes et leur indice(pour l'animation)
    tabLignesCompletes = []
    
    # On analyse chaque ligne de la matrice
    for indiceLigne in range(nbrLignesTotales):
        if 0 not in matriceJeu[indiceLigne]:  #<- si dans une ligne de la matrice,le chiffre '0' n'est pas pr�sent: cette ligne est compl�te
            tabLignesCompletes.append((matriceJeu[indiceLigne],indiceLigne))

    # Si le tableau de lignes compl�tes n'est pas vide
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

        # Puis on compte les points en fonction de l'indice de la ligne(+1 ainsi indice 19 donne 20points) multipli� par 10
        # plus elle est basse dans le jeu plus on a de points
        for memoire in tabLignesCompletes:
            points += (memoire[1]+1)*10
            nbrLignes += 1
            # Quand l'ajout d'une ligne d�passe un multiple de 20 on change de niveau
            if nbrLignes % 20 == 0:
                niveau += 1
                textNiveau.text = str(niveau)
            # On supprime la ligne et on ajoute une ligne de z�ro au debut de la matrice    
            del matriceJeu[memoire[1]]
            matriceJeu[0:0]=[[0]*nbrColonnesTotales]

        # On redessine tout
        dessine_bloques()

        # Bonus lorsqu'on compl�te plusieurs lignes : les points sont multipli�s par le nombre de lignes
        points *= len(tabLignesCompletes)
        score += points
        textScore.text = str(score)
        textLignes.text = str(nbrLignes)

def clignotement(visible = True):
    """Effet de clignotement.Les lignes compl�tes sont simultanement et succesivement remplac�e
    par des z�ro puis par elle-m�me."""
    for memoire in tabLignesCompletes:
        if visible:
            matriceJeu[memoire[1]] = memoire[0]
        else:
            matriceJeu[memoire[1]] = [0]*nbrColonnesTotales
    dessine_bloques()

#-------------------------------------------------------------------------------
#                 Gestion des �v�nements clavier
#-------------------------------------------------------------------------------
def key_input(evt):
    """M�thode qui s'occupe de switch vers la fonction correspondant � la touche press�e."""
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
    """M�thode qui s'occupe de switch vers la fonction correspondant � la touche relach�e."""    

    s = evt.key
    if s== 'down':
        acceleration_relachee()
    
#-------------------------------------------------------------------------------
def acceleration():
    """Touche BAS appuy�e : augmentation de la vitesse."""
    global vitesse
    
    vitesse = 0.01

#-------------------------------------------------------------------------------
def acceleration_relachee():
    """Touche BAS relach�e : la vitesse prend sa valeur d�termin�e par le niveau."""
    global vitesse

    vitesse = 1.05 - (niveau*0.05)

#-------------------------------------------------------------------------------  
def tombe():
    """Touche ESPACE appuy�e : la pi�ce tombe."""
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
    """Touche HAUT : si c'est possible la pi�ce tourne."""
    global sens
 
    if verif_deplacement(0,0,1,coordCourante):
        sens += 1
        if sens == 4:
            sens = 0
        if aide:
            projection_image() # Si la pi�ce peut tourner on recalcule les coordonn�es de sa projection image 
        dessine_piece()        

#-------------------------------------------------------------------------------
def gauche():
    """Touche Gauche : si c'est possible la pi�ce se d�place d'une colonne vers la gauche."""
    global coordCourante

    if verif_deplacement(0,-1,0,coordCourante):
        coordCourante[1] -= 1
        if aide:
            projection_image() # Si la pi�ce peut se d�placer on recalcule les coordonn�es de sa projection image 
        dessine_piece()        

#-------------------------------------------------------------------------------
def droite():
    """Touche Droite : si c'est possible la pi�ce se d�place d'une colonne vers la droite."""
    global coordCourante
    
    if verif_deplacement(0,1,0,coordCourante):
        coordCourante[1] += 1
        if aide:
            projection_image() # Si la pi�ce peut se d�placer on recalcule les coordonn�es de sa projection image 
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
    """M�thode qui incr�mente l'indice de r�solution."""
    global indiceResolution,pause

    pause = True
    indiceResolution += 1
    if indiceResolution == 4:
        indiceResolution = 0

    changement_resolution()

#-------------------------------------------------------------------------------    
def aide_on_off():
    """Affiche ou non la projection de la pi�ce."""
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
    """Incr�mente l'indice du choix de la mati�re dans le tableau les contenant."""
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
    """Active ou non le clignotement des lignes compl�tes."""
    global cligno

    cligno = not cligno
        
initialisation()
