import cv2
import numpy as np
import easyocr

image_path = r'C:\Users\hmeisson\Board.png'


image = cv2.imread(image_path)
image_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#RGB + Tolérance zones intéressantes
valeurs_RGB_cibles = [
    (100, 90, 90),
    (110, 90, 80),
    (70, 50, 50),
    (50, 30, 30),
    (110, 100, 90),
    (80, 80, 70),
    (80, 70, 70),
    (60, 30, 20),
    (100, 100, 100),
    (20, 20, 20),
    (120, 110, 100),
    #Valeur à adapter en fonction des tests
]

tolérance = 40

#image vide => stocke pixels correspondants
resultat = np.zeros_like(image_RGB)

for RGB_cible in valeurs_RGB_cibles:
    RGB_bas = np.array([RGB_cible[0] - tolérance, RGB_cible[1] - tolérance, RGB_cible[2] - tolérance])
    RGB_haut = np.array([RGB_cible[0] + tolérance, RGB_cible[1] + tolérance, RGB_cible[2] + tolérance])
    masque = cv2.inRange(image_RGB, RGB_bas, RGB_haut)
    resultat = cv2.bitwise_or(resultat, cv2.merge((masque, masque, masque)))

cv2.imwrite("contours.jpg", resultat)

reader = easyocr.Reader(['en'])
texte_liste = reader.readtext(resultat)

resultat = cv2.imread("contours.jpg")
couleur_rouge = (0, 0, 255)

#Trace txt
with open("resultat_texte.txt", "w", encoding="utf-8") as fichier_texte:
    for result in texte_liste:
        texte = result[1]
        #filtrage
        if texte.isalpha() and texte.isupper():
            top_left = result[0][0]
            bottom_right = result[0][2]
            top_left = tuple(map(int, top_left))
            bottom_right = tuple(map(int, bottom_right))
            cv2.rectangle(resultat, top_left, bottom_right, couleur_rouge, 2)
            fichier_texte.write(texte + "\n")

#sortie
cv2.imwrite("ville.jpg", resultat)

print("Le texte reconnu (majuscules uniquement) a été enregistré dans 'resultat_texte.txt'")
