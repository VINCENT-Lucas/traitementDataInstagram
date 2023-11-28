def generateColors(amount):
        # TODO Augmenter la gamme de couleurs atteignables
        ''' Génère amount couleurs sous forme rgba(255, 99, 132, 1)'''
        colorsList = []
        step = int(255/((amount//7)+1))
        intensity = 0
        while len(colorsList) < amount:
            intensity += step

            colorsList.append(f"rgba({intensity}, {0}, {0}, 1)")
            colorsList.append(f"rgba({0}, {intensity}, {0}, 1)")
            colorsList.append(f"rgba({0}, {0}, {intensity}, 1)")
            colorsList.append(f"rgba({intensity}, {intensity}, {0}, 1)")
            colorsList.append(f"rgba({0}, {intensity}, {intensity}, 1)")
            colorsList.append(f"rgba({intensity}, {0}, {intensity}, 1)")
            colorsList.append(f"rgba({intensity}, {intensity}, {intensity}, 1)")

        return colorsList[:amount]

print(generateColors(14))