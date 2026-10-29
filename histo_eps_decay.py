import matplotlib.pyplot as plt

# Tes 4 valeurs
values = [8.858865, 9.74003, 17.50607, 9.715845]

# Labels (optionnels)
labels = ['0.95', '0.995', '0.9995', '0.99995']

plt.figure(figsize=(6, 4))
plt.bar(labels, values)

plt.xlabel("eps_decay")
plt.ylabel("Score moyen")
plt.title("Score moyen en fonction de eps_decay")

plt.tight_layout()
plt.show()
