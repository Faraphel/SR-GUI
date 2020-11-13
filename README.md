# SR-GUI
(Méthodologie) Projet de visualisation de la super-résolution

Ce projet est en lien avec le diaporama de méthodologie. Je n'ai codé que le fichier Super-Résolution.pyw, 
le programme SRCNN a été écrit par yjn870 et est disponible à https://github.com/yjn870/SRCNN-pytorch, et le programme
SRGAN a été écrit par dongheehand disponible sur https://github.com/dongheehand/SRGAN-PyTorch. Les versions dans ce
programme ont été très légèrement corrigé à cause de certaines erreurs présentes à l'intérieur.

Il sera également nécessaire d'installer Pillow ainsi que Tkinter afin de faire fonctionner SR-GUI.

## PRÉ-REQUIS
Le programme ne peut pas fonctionner sans modification : il est nécessaire d'installer conda (pour Python 3.8) (disponible sur https://anaconda.org)
pour installer les librairies de deep-learning, principalement pytorch 1.6.0 (https://pytorch.org/get-started/previous-versions/ pour obtenir la commande de téléchargement).


De plus, il est nécessaire de télécharger les modèles pré-entrainés pour le SRCNN et le SRGAN (ou alors les entrainer soi-même):

SRCNN : https://www.dropbox.com/s/pd5b2ketm0oamhj/srcnn_x4.pth?dl=0 à mettre dans le dossier "SRCNN-pytorch-master/weights/"
SRGAN : https://drive.google.com/open?id=1-HmcV5X94u411HRa-KEMcGhAO1OXAjAc à mettre dans le dossier "SRGAN-PyTorch-master/model/"
