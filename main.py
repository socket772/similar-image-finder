import cv2 as cv
import os
import numpy
import sys
import skimage


def absolute_file_paths(directory: str):
    path: str = os.path.abspath(directory)
    return [entry.path for entry in os.scandir(path) if entry.is_file()]


def img_difference(img_base: cv.typing.MatLike, img_target_path: str):
    # Carico l'immagine di riferimento
    # img_ref: numpy.ndarray = cv.cvtColor(cv.imread(img_target_path), cv.COLOR_RGB2GRAY)
    img_ref: numpy.ndarray = cv.imread(img_target_path)
    # calcolo i punteggi
    score_r: numpy.float64 = skimage.metrics.structural_similarity(
        img_base[:, :, 0], img_ref[:, :, 0]
    )
    score_g: numpy.float64 = skimage.metrics.structural_similarity(
        img_base[:, :, 1], img_ref[:, :, 1]
    )
    score_b: numpy.float64 = skimage.metrics.structural_similarity(
        img_base[:, :, 2], img_ref[:, :, 2]
    )
    # Calcolo la media
    score_mean = (score_r + score_g + score_b) / 3
    diff_list.append(score_mean)
    print("{};{}".format(score_mean, img_target_path), file=sys.stderr)
    print("{};{}".format(score_mean, img_target_path))


if len(sys.argv) != 3:
    exit()

# Cartella di elaborazione
img_folder: str = sys.argv[1]
img_ref_path_list: list[str] = absolute_file_paths(img_folder)
# print(img_ref_path_list)

# Immagine di base
img_base_path: str = sys.argv[2]

# Carico l'immagine di base
# img_base: cv.typing.MatLike = cv.cvtColor(cv.imread(img_base_path), cv.COLOR_RGB2GRAY)
img_base: cv.typing.MatLike = cv.imread(img_base_path)

# Apri l'immagine
# Essenzialmente sono coordinate x,y. Questo da il vettore contente RGB
# Prendo l'altezza e la larghezza
(y, x) = img_base.shape[:2]
# print(y, x)

# Vettore di differenze percentuali tra le varie immagini
# La differenza è definita da colore (abs(immagine_lista + colore immagine_base) / 2) * 100 ?? Forse
diff_list: list[numpy.float64] = []
for img_ref_path in numpy.array(img_ref_path_list):
    img_difference(img_base, img_ref_path)
for i in range(len(diff_list)):
    print(
        "{},{}".format(
            diff_list[i],
            img_ref_path_list[i],
        )
    )
