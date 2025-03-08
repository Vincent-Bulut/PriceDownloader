
import os
import pandas as pd
import yfinance as yf
import sys


# Fonction pour détecter la racine du projet
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


def get_historical_prices(ticker, start_date='1900-01-01', interval='1d'):
    """
    Récupère les prix historiques d'un ticker via Yahoo Finance.

    :param ticker: Symbole boursier (ex: 'AAPL' pour Apple)
    :param start_date: Date de début (au format 'YYYY-MM-DD').
    :param interval: Intervalle des données ('1d', '1wk', '1mo', etc.).
    :return: DataFrame des prix historiques.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, interval=interval)

    if data.index.tzinfo is not None:
        data.index = data.index.tz_localize(None)  # Supprime le fuseau horaire (pour compatibilité Excel)

    return data


def process_csv_and_generate_excel(csv_file, output_excel, start_date='1900-01-01'):
    """
    Gère un fichier CSV contenant des tickers, récupère leurs prix historiques et génère un fichier Excel.

    :param csv_file: Chemin vers le fichier CSV contenant les tickers.
    :param output_excel: Chemin où écrire le fichier Excel généré.
    :param start_date: Date de début pour récupérer les données (au format YYYY-MM-DD).
    """
    try:
        tickers = pd.read_csv(csv_file, header=None)[0]  # Chargement des tickers depuis test.csv
    except FileNotFoundError:
        print(f"Erreur : le fichier '{csv_file}' n'a pas été trouvé.")
        return

    data_dict = {}

    for ticker in tickers:
        print(f"Récupération des données pour {ticker}...")
        try:
            data = get_historical_prices(ticker, start_date=start_date)
            data_dict[ticker] = data
        except Exception as e:
            print(f"Erreur lors de la récupération des données pour {ticker} : {e}")
            continue

    print("Écriture des données dans le fichier Excel...")
    with pd.ExcelWriter(output_excel) as writer:
        for ticker, data in data_dict.items():
            data.to_excel(writer, sheet_name=ticker[:31])  # Limite les noms de feuille à 31 caractères

    print(f"Fichier Excel généré : {output_excel}")


if __name__ == '__main__':
    # Obtient la racine du projet
    project_root = get_project_root()

    # Chemins des fichiers
    input_csv = os.path.join(project_root, "tickers.csv")  # test.csv se trouve dans la racine du projet
    output_excel = os.path.join(project_root, "historical_prices.xlsx")  # Output dans la racine du projet

    # Définir la date de début si nécessaire
    start_date = "1900-01-01"

    # Début du traitement
    process_csv_and_generate_excel(input_csv, output_excel, start_date)
    print('end of process')
