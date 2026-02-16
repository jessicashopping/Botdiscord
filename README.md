# 🧙 Grimory Bot — D&D Discord Bot

Bot Discord per server medievali a tema D&D 5e.

## Comandi disponibili

### 🎲 Dadi (`cogs/dice.py`)
| Comando | Descrizione |
|---------|-------------|
| `!roll 2d6+3` | Tira dadi con modificatori |
| `!adv [mod]` | Tiro con **vantaggio** (2d20, prendi il più alto) |
| `!dis [mod]` | Tiro con **svantaggio** (2d20, prendi il più basso) |
| `!stats` | Genera 6 statistiche (metodo 4d6 drop lowest) |
| `!init [mod]` | Tiro di **iniziativa** |
| `!perc` | Dado percentuale (d100) |
| `!ts [mod] [CD]` | **Tiro salvezza** con CD opzionale |

### 📚 Compendio (`cogs/compendium.py`)
| Comando | Descrizione |
|---------|-------------|
| `!classinfo <classe>` | Scheda completa di una classe D&D |
| Classi: | Barbaro, Bardo, Chierico, Druido, Guerriero, Ladro, Mago, Monaco, Paladino, Ranger, Stregone, Warlock |

### 📖 Lore (`cogs/lore.py`)
| Comando | Descrizione |
|---------|-------------|
| `!lore` | Elenco argomenti disponibili |
| `!lore <argomento>` | Lore di classi, razze, creature, piani |

### 🧙 NPC (`cogs/npc.py`)
| Comando | Descrizione |
|---------|-------------|
| `!npc` | Genera un NPC casuale completo (con segreto sotto spoiler!) |

### 🍺 Taverna (`cogs/taverna.py`) — NUOVO
| Comando | Descrizione |
|---------|-------------|
| `!taverna` | Genera una taverna con barista, menù, atmosfera e dicerie |

### ⚔️ Incontri (`cogs/encounter.py`) — NUOVO
| Comando | Descrizione |
|---------|-------------|
| `!encounter` | Incontro casuale (difficoltà random) |
| `!encounter facile` | Incontro facile |
| `!encounter mortale` | Incontro mortale |

### 🤣 Altro
| Comando | Descrizione |
|---------|-------------|
| `!joke` | Battuta casuale a tema D&D |
| `!riddle` | Indovinello medievale (risposta sotto spoiler) |
| `!coin` | Lancio della moneta |
| `!oracle` | Profezia misteriosa |
| `!destino8 <domanda>` | Dado del destino (tipo 8-ball) |
| `!help` | Menu comandi personalizzato |

### 💬 Risposte automatiche
- **Parolacce** → risposte divertenti a tema D&D
- **Saluti** → risposta amichevole (20% probabilità)

## Hosting
Hostato su **Railway**. Assicurati di avere la variabile d'ambiente `TOKEN` configurata.
