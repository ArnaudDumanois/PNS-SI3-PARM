# Projet PARM • Groupe Archi-tech

## Assembleur
### Tristan LARGUIER

La version finale de l'assembleur est contenue dans le fichier `assembleur.py` et utilise la bibliothèque `PARM_utils.py` pour fonctionner.

Pour tester manuellement le code il faut préalablement créer un objet assembleur depuis la classe du même nom : `assembleur = assembleur()`. On peut entrer des paramètres afin de modifier les fichiers à traiter, les adresses de destination et les paramètres de débuggage.

Pour tester une instruction simple on peut faire `assembleur.compile(["lsls r1, r2, #4"])`
Pour compiler un fichier contenant une liste d'instructions (fichier test) il suffit de modifier le fichier d'entrée et de lancer l'assemblage avec l'adresse de sortie :
```python
assembleur = assembleur()
assembleur.out = "test_integration/tests_personnalises/test_personnaliseOUT.bin"
assembleur.compile_from_file(f"test_integration/tests_personnalises/test_personnalise.s")
```

De même pour compiler un fichier généré avec Clang :
```python
assembleur = assembleur()
assembleur.out = "Tests Présentation/pascalOUT.bin"
assembleur.compile_from_clang(f"Tests Présentation/pascal.s")
```