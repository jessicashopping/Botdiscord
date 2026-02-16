"""
Gestione configurazione per server (guild).
Salva e carica le impostazioni in un file JSON.
"""

import json
import os
from pathlib import Path

CONFIG_PATH = Path("data/server_configs.json")

# Configurazione predefinita per ogni server
DEFAULT_CONFIG = {
    "welcome_enabled": False,
    "welcome_channel_id": None,
    "welcome_message": (
        "Benvenuto nella taverna, {member}! 🍺\n"
        "Preparati per le avventure che ti aspettano.\n"
        "Usa `!help` per scoprire tutti i comandi."
    ),
    "welcome_embed": True,
    "welcome_color": "8B4513",  # marrone medievale
    "goodbye_enabled": False,
    "goodbye_channel_id": None,
    "goodbye_message": "{member} ha lasciato la taverna. Che i dadi ti siano favorevoli, avventuriero! 🫡",
    "auto_role_id": None,
    "fun_replies_enabled": True,
    "fun_replies_chance": 20,  # percentuale per i saluti
}


def _ensure_file():
    """Crea il file se non esiste."""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text("{}", encoding="utf-8")


def load_all() -> dict:
    """Carica tutte le configurazioni."""
    _ensure_file()
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_all(data: dict):
    """Salva tutte le configurazioni."""
    _ensure_file()
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_guild_config(guild_id: int) -> dict:
    """Restituisce la configurazione di un server (con valori predefiniti)."""
    all_configs = load_all()
    guild_key = str(guild_id)

    if guild_key not in all_configs:
        all_configs[guild_key] = DEFAULT_CONFIG.copy()
        save_all(all_configs)

    # Assicura che tutte le chiavi predefinite esistano
    config = all_configs[guild_key]
    for key, value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = value

    return config


def update_guild_config(guild_id: int, **kwargs):
    """Aggiorna una o più impostazioni per un server."""
    all_configs = load_all()
    guild_key = str(guild_id)

    if guild_key not in all_configs:
        all_configs[guild_key] = DEFAULT_CONFIG.copy()

    for key, value in kwargs.items():
        if key in DEFAULT_CONFIG:
            all_configs[guild_key][key] = value

    save_all(all_configs)
    return all_configs[guild_key]


def reset_guild_config(guild_id: int) -> dict:
    """Ripristina la configurazione predefinita di un server."""
    all_configs = load_all()
    all_configs[str(guild_id)] = DEFAULT_CONFIG.copy()
    save_all(all_configs)
    return all_configs[str(guild_id)]
