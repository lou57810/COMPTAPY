import os

print("\n===== VARIABLES D'ENVIRONNEMENT DISPONIBLES =====\n")
for key, value in sorted(os.environ.items()):
    if "KEY" in key or "PASS" in key or "SECRET" in key:
        # on masque les infos sensibles
        print(f"{key}=********")
    else:
        print(f"{key}={value}")

print("\n===============================================\n")
