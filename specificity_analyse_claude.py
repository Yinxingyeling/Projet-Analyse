import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ========================================================
# 1. Configuration et Données
# ========================================================
df = pd.read_csv('Specificities_word.csv', sep='\t', quoting=3)

sns.set_context("talk")
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# Dictionnaire de traduction
translation_dict = {
    # Objectification visuelle
    '美貌': 'Beauté', '娇': 'Grâce', '女子': 'Femme',
    '容颜': 'Traits', '打扮': 'Se parer', '娇媚': 'Séduisante',
    '娇滴滴': 'Mièvrerie', '娇声': 'Voix douce',
    # Agentivité / Combat
    '打': 'Frapper', '杀': 'Tuer', '棒': 'Bâton',
    '金箍棒': 'Bâton magique', '斗': 'Combattre',
    '举棒': 'Lever le bâton', '一棒': 'Un coup',
    # Fragilisation émotionnelle
    '怕': 'Peur', '羞': 'Honte', '愁': 'Souci',
    '泪': 'Larmes', '含泪': 'Les larmes aux yeux',
    # Domestication sociale
    '娘子': 'Épouse', '姻缘': 'Destin matrimonial',
    '姐姐': 'Sœur aînée',
}

# ========================================================
# 2. Préparation des données
# ========================================================
all_test_words = list(translation_dict.keys())
bias_df = df[df['Unit'].isin(all_test_words)].copy()

# Delta_A : écart feminin vs original (manuel)
bias_df['Delta_A'] = bias_df['score_feminin'] - bias_df['score_manuel']

# Delta_B : double standard feminin vs masculin
bias_df['Delta_B'] = bias_df['score_feminin'] - bias_df['score_masculin']

bias_df['Label_FR'] = bias_df['Unit'].apply(
    lambda x: f"{x} | {translation_dict.get(x, '')}"
)

print("Mots trouvés dans le CSV :")
print(bias_df[['Unit', 'score_feminin', 'score_masculin', 'score_manuel', 'Delta_A', 'Delta_B']].to_string())

# ========================================================
# 3. Visualisation
# ========================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(26, 16))
fig.patch.set_facecolor('#fdfdfd')

def plot_styled_bar(ax, data, column, title):
    data_sorted = data.sort_values(by=column, ascending=False)
    colors = ['#d65f5f' if x > 0 else '#4878d0' for x in data_sorted[column]]

    sns.barplot(ax=ax, x=column, y='Label_FR', data=data_sorted,
                palette=colors, alpha=0.85, edgecolor='black', linewidth=0.5)

    ax.set_title(title, fontsize=20, fontweight='bold', pad=25, color='#2c3e50')
    ax.set_xlabel('Intensité du Biais (Score Delta)', fontsize=14, labelpad=15)
    ax.set_ylabel('')
    ax.axvline(0, color='black', linewidth=1.5, alpha=0.7)
    ax.grid(axis='x', linestyle='--', alpha=0.4)
    sns.despine(ax=ax, left=True, bottom=False)

plot_styled_bar(ax1, bias_df, 'Delta_A', 'Delta A : Écart Féminin vs Original')
plot_styled_bar(ax2, bias_df, 'Delta_B', 'Delta B : Double Standard (Féminin vs Masculin)')

plt.suptitle("Biais de Genre dans la Génération Textuelle par IA",
             fontsize=28, fontweight='bold', y=0.98, color='#1a1a1a')

plt.subplots_adjust(left=0.22, wspace=0.35, top=0.90)
plt.savefig('Biais_IA.png', bbox_inches='tight', dpi=300)
plt.show()
print("\nGraphique sauvegardé : Biais_IA.png")
