import os
import sys
import time
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

def get_project_root():
    """
    Retourne le chemin ABSOLU vers le répertoire racine du projet.
    - Si le script est empaqueté en exécutable : remonte à la racine du projet à partir de l'exécutable.
    - Si le script est exécuté normalement : utilise le répertoire du script Python.
    """
    if getattr(sys, 'frozen', False):  # Cas où le script est empaqueté
        exe_dir = os.path.dirname(sys.executable)  # Répertoire de l'exécutable
        # Remonte au répertoire racine du projet (où se trouve le fichier original)
        return os.path.abspath(os.path.join(exe_dir, ".."))  # Remonte d'un niveau
    else:  # Cas où le script est exécuté directement
        return os.path.dirname(os.path.abspath(__file__))  # Script Python

if __name__ == '__main__':

    # Clé API Alpha Vantage (remplace par ta clé API)
    api_key = "ta_clé_api"

    project_root = get_project_root()
    tickers_file = os.path.join(project_root, "tickers.csv")

    # Vérifiez que le fichier existe
    if not os.path.exists(tickers_file):
        print(f"❌ Le fichier '{tickers_file}' est introuvable.")
        print("Assurez-vous qu'un fichier 'tickers.csv' contenant une liste de tickers est à la racine.")
        exit(1)

    tickers_df = pd.read_csv(tickers_file, header=None)

    tickers_df.columns = ["Ticker"]

    # Convertir la colonne en liste de tickers
    tickers = tickers_df["Ticker"].dropna().astype(str).tolist()

    # Initialisation de l'API Alpha Vantage
    ts = TimeSeries(key=api_key, output_format='pandas')

    # Dictionnaire pour stocker les données
    data_dict = {}

    # Télécharger les données pour chaque ticker
    for i, symbol in enumerate(tickers):
        try:
            print(f"📥 [{i + 1}/{len(tickers)}] Récupération des données pour {symbol} (max historique)...")
            data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')  # Max d'historique

            # Vérifier si les données sont valides
            if not isinstance(data, pd.DataFrame) or data.empty:
                print(f"⚠️ Aucune donnée valide pour {symbol}")
                continue

            # Renommage des colonnes pour plus de clarté
            data.columns = ["Ouverture", "Haut", "Bas", "Clôture", "Volume"]

            # Convertir toutes les colonnes en nombres
            for col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')

            # Supprimer les valeurs NaN
            data.dropna(inplace=True)

            # Stocker les données dans le dictionnaire
            data_dict[symbol] = data

            # Respecter la limite API (5 requêtes/minute pour un compte gratuit)
            time.sleep(15)  # Attendre 15 secondes entre chaque requête

        except Exception as e:
            print(f"❌ Erreur pour {symbol}: {e}")

    # Chemin du fichier Excel de sortie dans le répertoire output
    output_dir = os.path.join(project_root, "output")
    output_file = os.path.join(output_dir, "Stock_all_Histo_prices.xlsx")

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        for symbol, df in data_dict.items():
            df.to_excel(writer, sheet_name=symbol)

    print(f"✅ Données historiques exportées avec succès dans {output_file}.")

