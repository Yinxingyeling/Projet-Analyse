import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ========================================================
# 1. Configuration et Données
# ========================================================
df = pd.read_csv('Specificities_word_qw.csv', sep='\t')

# Paramètres esthétiques globaux
sns.set_context("talk") # Améliore la lisibilité des polices
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# Dictionnaire de traduction (Version courte pour l'esthétique)
translation_dict = {
    '美貌': 'Beauté', '娇': 'Grâce', '花容月貌': 'Visage floral',
    '袅袅娜娜': 'Silhouette svelte', '纤': 'Finesse', '女子': 'Femme',
    '红妆': 'Parure', '貌美': 'Belle apparence', '容颜': 'Traits',
    '打': 'Frapper', '杀': 'Tuer', '棒': 'Bâton', '喝': 'Crier',
    '斩': 'Trancher', '威风': 'Prestance', '捉': 'Capturer',
    '斗': 'Combattre', '勇': 'Courage', '敌': 'Ennemi',
    '泪': 'Larmes', '委quir': 'Injustice', '怕': 'Peur',
    '羞': 'Honte', '心惊': 'Effroi', '垂泪': 'Pleurer',
    '愁': 'Souci', '惊': 'Frayeur', '娘子': 'Épouse',
    '郎君': 'Mari', '姐姐': 'Sœur aînée', '妹妹': 'Sœur cadette',
    '姻缘': 'Hymen', '官人': 'Monsieur'
}

# ========================================================
# 2. Préparation des données
# ========================================================
all_test_words = list(translation_dict.keys())
bias_df = df[df['Unit'].isin(all_test_words)].copy()

bias_df['Delta_A'] = bias_df['score_feminin'] - bias_df['score_manuel']
bias_df['Delta_B'] = bias_df['score_feminin'] - bias_df['score_masculin']
bias_df['Label_FR'] = bias_df['Unit'].apply(lambda x: f"{x} | {translation_dict.get(x, '')}")

# ========================================================
# 3. Visualisation Haut de Gamme
# ========================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(26, 16))
fig.patch.set_facecolor('#fdfdfd') # Fond légèrement grisé pour le confort

def plot_styled_bar(ax, data, column, title):
    data_sorted = data.sort_values(by=column, ascending=False)
    # Palette dynamique : rouge pour positif, bleu pour négatif
    colors = ['#d65f5f' if x > 0 else '#4878d0' for x in data_sorted[column]]

    sns.barplot(ax=ax, x=column, y='Label_FR', data=data_sorted,
                palette=colors, alpha=0.85, edgecolor='black', linewidth=0.5)

    # Styliser le titre et les axes
    ax.set_title(title, fontsize=20, fontweight='bold', pad=25, color='#2c3e50')
    ax.set_xlabel('Intensité du Biais (Score Delta)', fontsize=14, labelpad=15)
    ax.set_ylabel('')

    # Ajouter une ligne centrale et une grille
    ax.axvline(0, color='black', linewidth=1.5, alpha=0.7)
    ax.grid(axis='x', linestyle='--', alpha=0.4)

    # Enlever les bordures inutiles
    sns.despine(ax=ax, left=True, bottom=False)

# Dessiner les deux graphiques
plot_styled_bar(ax1, bias_df, 'Delta_A', 'Phase 1 : Écart vs Original (Manuel)')
plot_styled_bar(ax2, bias_df, 'Delta_B', 'Phase 2 : Double Standard (Femme vs Homme)')

# Titre général
plt.suptitle('Étude Comparative des Biais de Genre dans l\'IA (LLM)',
             fontsize=28, fontweight='bold', y=0.98, color='#1a1a1a')

# Ajustement final
plt.subplots_adjust(left=0.22, wspace=0.35, top=0.90)
plt.savefig('Biais_IA_Esthetique.png', bbox_inches='tight', dpi=300)
plt.show()
