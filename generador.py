# Número inicial
numero = 74

# Abre el archivo en modo escritura ('w')
with open('secuencia.txt', 'w') as archivo:
    # Ciclo para generar la secuencia
    for i in range(161):  # Generar 15 números en total (4 repeticiones x 15 números = 60)
        for j in range(4):  # Repetir cuatro veces el mismo número
            archivo.write(f"{numero}\n")  # Escribe el número actual con un salto de línea
        numero += 1  # Incrementar el número en 1 para la siguiente secuencia

