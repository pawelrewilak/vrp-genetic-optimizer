import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
import os
import numpy as np

# Konfiguracja stylu wykresów
sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
RESULTS_DIR = 'tests_results'

def load_data():
    csv_path = os.path.join(RESULTS_DIR, 'benchmark_results.csv')
    json_path = os.path.join(RESULTS_DIR, 'convergence_data.json')
    
    if not os.path.exists(csv_path):
        print("Brak pliku CSV z wynikami!")
        return None, None
        
    df = pd.read_csv(csv_path)
    
    try:
        with open(json_path, 'r') as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []
        
    return df, logs

def plot_fitness_boxplots(df):
    """Generuje wykresy pudełkowe dla każdego rozmiaru problemu osobno."""
    sizes = sorted(df['size'].unique())
    
    for size in sizes:
        subset = df[df['size'] == size]
        
        plt.figure(figsize=(12, 6))
        
        # POPRAWKA: Sortujemy malejąco (ascending=False), 
        # bo chcemy, aby konfiguracja z NAJWYŻSZYM zyskiem była pierwsza z lewej.
        order = subset.groupby(["config"])["fitness"].median().sort_values(ascending=False).index
        
        # Rysowanie Boxplota
        ax = sns.boxplot(data=subset, x='config', y='fitness', order=order, palette="viridis")
        
        # Dodanie punktów (swarmplot) pokazuje rzeczywisty rozrzut prób
        sns.stripplot(data=subset, x='config', y='fitness', order=order, 
                     color='black', alpha=0.3, size=3, jitter=True)

        plt.title(f'Rozkład Zysku (Fitness) - {size} Szkół')
        plt.ylabel('Całkowity Zysk (więcej = lepiej)') # Zmieniony opis osi
        plt.xlabel('Konfiguracja')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        save_path = os.path.join(RESULTS_DIR, f'boxplot_fitness_{size}.png')
        plt.savefig(save_path, dpi=300)
        print(f"Zapisano: {save_path}")
        plt.close()

def plot_convergence_aggregated(logs):
    """Rysuje uśrednione krzywe zbieżności dla największych instancji."""
    if not logs:
        return

    # Wybieramy tylko największy rozmiar problemu do analizy zbieżności
    max_size = max(log['size'] for log in logs)
    target_logs = [log for log in logs if log['size'] == max_size]
    
    # Przygotowanie danych
    data = []
    for log in target_logs:
        for gen, fit in enumerate(log['history']):
            data.append({
                'Generation': gen,
                'Fitness': fit,
                'Config': log['config']
            })
    
    df_conv = pd.DataFrame(data)

    plt.figure(figsize=(12, 7))
    
    sns.lineplot(data=df_conv, x='Generation', y='Fitness', hue='Config', palette="tab10")
    
    plt.title(f'Wzrost Zysku w czasie (Średnia z prób) - {max_size} Szkół')
    plt.ylabel('Fitness (Zysk)')
    plt.xlabel('Generacja')
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    plt.tight_layout()
    
    save_path = os.path.join(RESULTS_DIR, f'convergence_curve_{max_size}.png')
    plt.savefig(save_path, dpi=300)
    print(f"Zapisano: {save_path}")
    plt.close()

def plot_time_comparison(df):
    """Porównanie czasu wykonania."""
    plt.figure(figsize=(10, 6))
    
    sns.barplot(data=df, x='size', y='time', hue='config', errorbar=None, palette="muted")
    
    plt.title('Średni Czas Obliczeń')
    plt.ylabel('Czas [s]')
    plt.xlabel('Liczba Szkół')
    plt.legend(title='Konfiguracja', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    save_path = os.path.join(RESULTS_DIR, 'time_comparison.png')
    plt.savefig(save_path, dpi=300)
    print(f"Zapisano: {save_path}")
    plt.close()

if __name__ == "__main__":
    print("Generowanie wykresów...")
    df, logs = load_data()
    
    if df is not None:
        plot_fitness_boxplots(df)
        plot_time_comparison(df)
    
    if logs is not None:
        plot_convergence_aggregated(logs)
        
    print("Gotowe!")