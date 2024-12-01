import cv2 as cv
import os
import numpy as np


#
# ATTENZIONE. Si parte dal presupposto che le immagini siano tutte della stessa dimensione di quella di base
#
def main():
    print("Partenza programma")

    # Cartella di elaborazione
    img_folder = input("Cartella immagini: ")
    img_ref_path_list = [
        f for f in os.listdir(img_folder) if os.path.isfile(os.path.join(img_folder, f))
    ]
    print()

    # Immagine di base
    img_base_path = input("Percorso immagine base: ")

    # Carico l'immagine di base
    img_base = cv.imread(img_base_path)

    # Apri l'immagine
    # Essenzialmente sono coordinate x,y. Questo da il vettore contente RGB
    cv.imshow("Immagine", img_base)
    # Prendo l'altezza e la larghezza
    y, x = img_base.shape[:2]
    print(y, x)
    k = cv.waitKey(0)  # Wait for a keystroke in the window

    # Vettore di differenze percentuali tra le varie immagini
    # La differenza è definita da colore (abs(immagine_lista + colore immagine_base) / 2) * 100 ?? Forse
    diff_list = []

    # Iteratore per la lista delle immagini
    for img_ref_path in np.array(img_ref_path_list):
        # x[y[RGB[]]]
        result = [[[]]]
        # Carico l'immagine di riferimento
        img_ref = cv.imread(img_ref_path)

        for i in range(0, x):
            for j in range(0, y):
                pixel_mean = np.sum([img_base[y][x], img_ref[y][x]], axis=0)
                print(pixel_mean)


if __name__ == "__main__":
    main()
