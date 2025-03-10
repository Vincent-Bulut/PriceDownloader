# PriceDownloader
## Prérequis
- Toutes les dépendances nécessaires sont listées dans le fichier `requirements.txt`.
### Installer les dépendances avec `pip` :
Assurez-vous d'avoir Python installé sur votre machine, puis exécutez cette commande pour installer les dépendances :
```bash
  pip install -r requirements.txt
```
- **Important** : 
  1. Assurez-vous que le fichier **`tickers.csv`** est toujours placé à la **racine du projet**
  2. Le fichier **`tickers.csv`** doit contenir une liste de tickers **sans header**.  
     Exemple de contenu du fichier `tickers.csv` :
     ```csv
     AAPL
     TSLA
     MSFT
     GOOGL
     ```
## Utilisation

1. Exécutez le fichier `yahoo_prices_downloader.py` (ou utilisez l'exécutable généré) dans le dossier ./dist.

2. Le fichier contenant les prix historiques sera généré dans le dossier `output` sous le nom **`historical_prices.xlsx`**.

---
## Résultat

- Une fois l'application terminée, le fichier Excel contenant les données sera situé dans le dossier suivant :
  ```
  output/historical_prices.xlsx
  ```
---

## Générer un exécutable unique

Si vous souhaitez transformer le script Python en un exécutable autonome (par exemple, pour une distribution ou pour un usage sur une machine sans Python installé) :

1. Installez **PyInstaller** si ce n'est pas déjà fait :
   ```bash
   pip install pyinstaller
   ```

2. Utilisez la commande suivante pour générer un exécutable unique :
   ```bash
   pyinstaller --onefile yahoo_prices_downloader.py
   ```

3. Une fois la commande terminée, l'exécutable sera situé dans le dossier `dist/` sous le nom **`yahoo_prices_downloader`** (ou `yahoo_prices_downloader.exe` sous Windows).
     