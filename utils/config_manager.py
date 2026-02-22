"""
Gestione configurazione per server (guild).
Salva e carica le impostazioni in un file JSON.
"""

import json
from pathlib import Path

CONFIG_PATH = Path("data/server_configs.json")

DEFAULT_CONFIG = {
    # ── Benvenuto ────────────────────────────────────────
    "welcome_enabled": False,
    "welcome_channel_id": None,
    "welcome_message": (
        "Benvenuto nella taverna, {member}! 🍺\n"
        "Preparati per le avventure che ti aspettano.\n"
        "Usa `!help` per scoprire tutti i comandi."
    ),
    "welcome_embed": True,
    "welcome_color": "8B4513",
    # ── Addio ────────────────────────────────────────────
    "goodbye_enabled": False,
    "goodbye_channel_id": None,
    "goodbye_message": "{member} ha lasciato la taverna. Che i dadi ti siano favorevoli! 🫡",
    # ── Auto-ruolo ───────────────────────────────────────
    "auto_role_id": None,
    # ── Staff ────────────────────────────────────────────
    "staff_role_id": None,  # ruolo che può usare !config oltre agli admin
    # ── Risposte divertenti ──────────────────────────────
    "fun_replies_enabled": True,
    "fun_replies_chance": 20,
    # ── Self Roles ───────────────────────────────────────
    "selfroles_channel_id": None,
    "selfroles_message_ids": {},
    "color_roles": {},
    "class_roles": {},
    "unlock_roles": {},
    "selfroles_titles": {
        "color": "💎 Scegli la tua Gemma",
        "class": "⚔️ Scegli la tua Classe",
        "unlock": "🔓 Ruoli Speciali",
    },
    "selfroles_descriptions": {
        "color": "Seleziona una gemma per cambiare il colore del tuo nome!",
        "class": "Scegli la classe del tuo personaggio per mostrare a tutti chi sei!",
        "unlock": "Clicca per ottenere o rimuovere un ruolo!",
    },
    # ── Canali protetti (solo bot) ───────────────────────
    "locked_channels": [],  # lista di channel_id dove solo i bot possono scrivere
}


def _ensure_file():
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text("{}", encoding="utf-8")


def load_all() -> dict:
    _ensure_file()
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_all(data: dict):
    _ensure_file()
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_guild_config(guild_id: int) -> dict:
    all_configs = load_all()
    guild_key = str(guild_id)

    if guild_key not in all_configs:
        all_configs[guild_key] = _deep_copy_default()
        save_all(all_configs)

    config = all_configs[guild_key]
    # Assicura che tutte le chiavi predefinite esistano
    for key, value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = _deep_copy_value(value)
    # Assicura sotto-chiavi dizionari
    for dict_key in ("selfroles_titles", "selfroles_descriptions", "selfroles_message_ids"):
        if isinstance(DEFAULT_CONFIG[dict_key], dict):
            for sub_key, sub_val in DEFAULT_CONFIG[dict_key].items():
                if sub_key not in config[dict_key]:
                    config[dict_key][sub_key] = sub_val

    return config


def update_guild_config(guild_id: int, **kwargs):
    all_configs = load_all()
    guild_key = str(guild_id)

    if guild_key not in all_configs:
        all_configs[guild_key] = _deep_copy_default()

    for key, value in kwargs.items():
        all_configs[guild_key][key] = value

    save_all(all_configs)
    return all_configs[guild_key]


def reset_guild_config(guild_id: int) -> dict:
    all_configs = load_all()
    all_configs[str(guild_id)] = _deep_copy_default()
    save_all(all_configs)
    return all_configs[str(guild_id)]


def _deep_copy_default() -> dict:
    return _deep_copy_value(DEFAULT_CONFIG)


def _deep_copy_value(value):
    if isinstance(value, dict):
        return {k: _deep_copy_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_deep_copy_value(v) for v in value]
    return value
