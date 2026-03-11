import json, random, os

random.seed(42)

COLOR_HEX = {
    "Aqua": "#00CED1", "Black": "#2c3e50", "Blue": "#3498db", "Bronze": "#CD7F32",
    "Brown": "#8B4513", "Chartreuse": "#7FFF00", "Cherry": "#DE3163", "Cyan": "#1abc9c",
    "Emerald": "#50C878", "ExoticPurple": "#8B008B", "Gold": "#FFD700", "Green": "#27ae60",
    "GreenYellow": "#ADFF2F", "Grey": "#7f8c8d", "Indigo": "#4B0082", "Lavender": "#B57EDC",
    "Lime": "#32CD32", "Midnight": "#191970", "Orange": "#e67e22", "Pine": "#01796F",
    "Purple": "#9b59b6", "PurpleBloom": "#A020F0", "Red": "#e74c3c", "RedOriginal": "#C0392B",
    "RoyalPurple": "#7851A9", "Ruby": "#E0115F", "Silver": "#C0C0C0", "Tan": "#D2B48C",
    "Turquoise": "#40E0D0", "Vessel": "#4682B4", "Violet": "#8F00FF", "WaterMelon": "#FC6C85",
    "White": "#ecf0f1", "Yellow": "#f1c40f", "Beige": "#F5F5DC",
}

RARITIES = ["common", "common", "common", "rare", "rare", "epic", "legendary"]

NAME_PREFIXES = [
    "Shadow", "Void", "Nova", "Pulse", "Iron", "Solar", "Storm", "Dark", "Neon", "Quantum",
    "Astral", "Crimson", "Silver", "Ghost", "Plasma", "Zenith", "Obsidian", "Wraith",
    "Photon", "Eclipse", "Titan", "Nebula", "Comet", "Hyper", "Omega", "Alpha", "Delta",
    "Viper", "Phantom", "Raven", "Blaze", "Frost", "Thunder", "Mystic", "Chaos",
    "Apex", "Prism", "Stealth", "Ember", "Drift", "Fury", "Saber", "Onyx", "Azure",
    "Jade", "Cobalt", "Scarlet", "Ivory", "Gilded", "Cosmic",
]
NAME_SUFFIXES = [
    "Vanguard", "Striker", "Drifter", "Phantom", "Fang", "Breaker", "Runner", "Talon",
    "Hawk", "Comet", "Wing", "Blade", "Serpent", "Fury", "Raider", "Interceptor",
    "Ghost", "Corsair", "Arrow", "Storm", "Sentinel", "Warden", "Reaper", "Hunter",
    "Stalker", "Seeker", "Guardian", "Marauder", "Voyager", "Pioneer", "Ranger",
    "Lancer", "Charger", "Cruiser", "Ravager", "Avenger", "Predator", "Spectre",
    "Herald", "Titan", "Monarch", "Phoenix", "Valkyrie", "Pegasus", "Chimera",
]

# Suffixes to append to ship names - mix of marks and cool tags
VARIANT_SUFFIXES = [
    "Mk.I", "Mk.II", "Mk.III", "Mk.IV", "Mk.V",
    "Mk.VI", "Mk.VII", "Mk.VIII", "Mk.IX", "Mk.X",
    "Mk.XI", "Mk.XII", "Mk.XIII", "Mk.XIV", "Mk.XV",
    "Mk.XVI", "Mk.XVII", "Mk.XVIII", "Mk.XIX", "Mk.XX",
    "Alpha", "Beta", "Gamma", "Delta", "Epsilon",
    "Omega", "Prime", "Elite", "Ace", "Zenith",
    "Apex", "Nova", "Neo", "Plus", "Ultra",
    "EX", "GT", "RS", "SE", "X",
]

used_names = set()
def gen_name(variant_index):
    suffix = VARIANT_SUFFIXES[variant_index % len(VARIANT_SUFFIXES)]
    for _ in range(300):
        n = f"{random.choice(NAME_PREFIXES)} {random.choice(NAME_SUFFIXES)} {suffix}"
        if n not in used_names:
            used_names.add(n)
            return n
    return f"Ship-{random.randint(1000,9999)} {suffix}"

SERIES_DATA = {
    "AstroEagle": {"texDir": "AstroEagle/Standard", "prefix": "AstroEagle"},
    "CosmicShark": {"texDir": "CosmicShark", "prefix": "CosmicShark"},
    "CraizanStar": {"texDir": "CraizanStar", "prefix": "CraizanStar"},
    "ForceBadger": {"texDir": "ForceBadger", "prefix": "ForceBadger"},
    "GalacticLeopard": {"texDir": "GalacticLeopard/Main", "prefix": "GalacticLeopard_Main"},
    "GalacticOkamoto": {"texDir": "GalacticOkamoto", "prefix": "GalacticOkamoto"},
    "GalaxyRaptor": {"texDir": "GalaxyRaptor", "prefix": "GalaxyRaptor"},
    "GenericSpaceships": {"texDir": "GenericSpaceships/GenericSpaceships1-8", "prefix": "GenericSpaceships"},
    "HyperFalcon": {"texDir": "HyperFalcon", "prefix": "HyperFalcon"},
    "LightFox": {"texDir": "LightFox", "prefix": "LightFox"},
    "MeteorMantis": {"texDir": "MeteorMantis", "prefix": "MeteorMantis"},
    "NightAye": {"texDir": "NightAye", "prefix": "NightAye"},
    "ProtonLegacy": {"texDir": "ProtonLegacy", "prefix": "ProtonLegacy"},
    "SpaceExcalibur": {"texDir": "SpaceExcalibur", "prefix": "SpaceExcalibur"},
    "SpaceSphinx": {"texDir": "SpaceSphinx", "prefix": "SpaceSphinx"},
    "StarForce": {"texDir": "StarForce", "prefix": "StarForce"},
    "StarSparrow": {"texDir": "StarSparrow", "prefix": "StarSparrow"},
    "StriderOx": {"texDir": "StriderOx", "prefix": "StriderOx"},
    "VoidWhale": {"texDir": "VoidWhale", "prefix": "VoidWhale"},
}

DST = "C:/Users/avsh/LocalProjects/_Experiments/TestShipsWeb"
TEX_BASE = f"{DST}/textures"

# Read the existing ships.json to get variant/file info
# (We need to read the OLD format before we overwrite it)
with open(f"{DST}/ships.json") as f:
    existing = json.load(f)

# Build texture groups (shared by ships of same original series)
texture_groups = []
texture_group_map = {}  # series_name -> group_index

for series_entry in existing["ships"]:
    series = series_entry["series"]
    sd = SERIES_DATA.get(series)
    if not sd:
        continue

    tex_dir = f"{TEX_BASE}/{sd['texDir']}"
    prefix = sd["prefix"]

    # Find Normal map
    normal_map = None
    for nc in [f"{prefix}_Normal.png", f"{series}Normal.png", f"{series}_Normal.png"]:
        if os.path.exists(f"{tex_dir}/{nc}"):
            normal_map = f"textures/{sd['texDir']}/{nc}"
            break

    # Find MetallicSmoothness map
    ms_map = None
    for mc in [f"{prefix}_MetallicSmoothness.png", f"{series}_MetallicSmoothness.png"]:
        if os.path.exists(f"{tex_dir}/{mc}"):
            ms_map = f"textures/{sd['texDir']}/{mc}"
            break

    # Find Emission map
    emission_map = None
    for suffix in ["_Emission.png", "_Emission1.png"]:
        for pfx in [prefix, series]:
            candidate = f"{pfx}{suffix}"
            if os.path.exists(f"{tex_dir}/{candidate}"):
                emission_map = f"textures/{sd['texDir']}/{candidate}"
                break
        if emission_map:
            break
    # Special case for GenericSpaceships
    if series == "GenericSpaceships" and not emission_map:
        emission_map = "textures/GenericSpaceships/GenericSpaceships1-8/GenericSpaceships_Emission-1.png"

    # Build skins
    skins = []
    for i, skin in enumerate(series_entry.get("skins", [])):
        name = skin["name"]
        color = COLOR_HEX.get(name, "#888888")
        file_name = f"{prefix}_{name}.png"
        if not os.path.exists(f"{tex_dir}/{file_name}"):
            file_name = f"{series}_{name}.png"
        skins.append({
            "name": name,
            "file": f"textures/{sd['texDir']}/{file_name}",
            "color": color,
            "unlocked": i < 2
        })

    group_idx = len(texture_groups)
    texture_groups.append({
        "normalMap": normal_map,
        "metallicSmoothnessMap": ms_map,
        "emissionMap": emission_map,
        "skins": skins,
    })
    texture_group_map[series] = group_idx

# Build flat ship list
ships = []
global_idx = 0

for series_entry in existing["ships"]:
    series = series_entry["series"]
    sd = SERIES_DATA.get(series)
    if not sd:
        continue

    group_idx = texture_group_map[series]
    variants = series_entry.get("variants", [])

    for vi, v in enumerate(variants):
        rarity = random.choice(RARITIES)
        mult_ranges = {"common": (1, 3), "rare": (4, 6), "epic": (7, 8), "legendary": (9, 10)}
        lo, hi = mult_ranges[rarity]
        mult = random.randint(lo, hi)

        ships.append({
            "id": global_idx,
            "name": gen_name(vi),
            "rarity": rarity,
            "blackholeMultiplicator": mult,
            "glb": f"ships/{series}/{v['file']}",
            "textureGroup": group_idx,
        })
        global_idx += 1

# Write final JSON
output = {
    "textureGroups": texture_groups,
    "ships": ships,
}

with open(f"{DST}/ships.json", "w") as f:
    json.dump(output, f, indent=2)

# Print summary
from collections import Counter
rarities = Counter(s["rarity"] for s in ships)
print(f"Generated ships.json: {len(ships)} ships, {len(texture_groups)} texture groups")
print(f"Rarity: {dict(rarities)}")
for tg_idx, tg in enumerate(texture_groups):
    count = sum(1 for s in ships if s["textureGroup"] == tg_idx)
    print(f"  Group {tg_idx}: {count} ships, {len(tg['skins'])} skins")
print(f"\nSample ships:")
for s in ships[:5]:
    print(f"  [{s['id']:3d}] {s['name']:35s} {s['rarity']:10s} x{s['blackholeMultiplicator']} -> {s['glb']}")
