import cv2 as cv
import sys


def main():
    print("Partenza programma")
    # Cartella di elaborazione
    img_folder = input("Cartella immagini")
    print(img_folder)
    # Immagine di base
    img_base_path = input("Percorso immagine base")
    print(img_base_path)

    # Carico l'immagine di base
    img_base = cv.imread(img_base_path)

    # Apri l'immagine
    cv.imshow("Immagine", img_base)
    k = cv.waitKey(0)  # Wait for a keystroke in the window


if __name__ == "__main__":
    main()
