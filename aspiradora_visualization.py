import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from aspiradora_modelo import AspiradoraModelo

# Cargar las imágenes
aspiradora_img = plt.imread("images\w.png")
celda_sucia_img = plt.imread("images\dust.png")
background_img = plt.imread("images\wood.jpg")

def representar_aspiradoras(modelo):
    """Función para obtener la posición de las aspiradoras y de las celdas sucias."""
    posiciones_aspiradoras = []
    celdas_sucias = modelo.celdas_sucias  

    for agente in modelo.schedule.agents:
        x, y = agente.pos
        posiciones_aspiradoras.append((x, y))

    return posiciones_aspiradoras, celdas_sucias

# Inicializamos nuestro modelo
num_agentes = 5
ancho = 10       
alto = 10     
porcentaje_sucio = 0.3

modelo = AspiradoraModelo(num_agentes, ancho, alto, porcentaje_sucio)
fig, ax = plt.subplots()

# -------- INICIAMOS NUESTRA SIMULACIÓN --------------------

for i in range(100):
    modelo.step()  # Avanzamos un paso en la simulación

    # Obtenemos posiciones de aspiradoras y celdas sucias
    posiciones_aspiradoras, celdas_sucias = representar_aspiradoras(modelo)

    # Limpiar el gráfico para la actualización
    ax.clear()

    # Establecemos la imagen de fondo
    ax.imshow(background_img, extent=[-1, ancho, -1, alto], aspect='auto')

    # Mostramos las celdas sucias como imágenes
    for (x, y) in celdas_sucias:
        imagebox = OffsetImage(celda_sucia_img, zoom=0.1)  # Ajusta zoom según tamaño
        ab = AnnotationBbox(imagebox, (x, y), frameon=False)
        ax.add_artist(ab)

    # Mostramos las aspiradoras como imágenes
    for (x, y) in posiciones_aspiradoras:
        imagebox = OffsetImage(aspiradora_img, zoom=0.05)  # Ajusta zoom según tamaño
        ab = AnnotationBbox(imagebox, (x, y), frameon=False)
        ax.add_artist(ab)

    # Configuraciones del gráfico
    ax.set_xlim(-1, ancho)
    ax.set_ylim(-1, alto)
    ax.set_title(f"Paso de simulación: {i+1}")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_xticks(range(ancho))
    ax.set_yticks(range(alto))
    ax.grid(True)

    # Pausa para animación
    plt.pause(0.1)

    # Finaliza si todas las celdas están limpias
    if not celdas_sucias:
        print("Todas las celdas están limpias. Terminando la simulación.")
        break

# Obtener resultados finales
completado, porcentaje_limpio, total_movimientos, tiempo_ejecucion = modelo.obtener_resultados()

# Mostrar resultados finales en el gráfico
ax.clear()

ax.imshow(background_img, extent=[-1, ancho, -1, alto], aspect='auto')

# Imágenes de celdas sucias restantes
for (x, y) in modelo.celdas_sucias:
    imagebox = OffsetImage(celda_sucia_img, zoom=0.1)
    ab = AnnotationBbox(imagebox, (x, y), frameon=False)
    ax.add_artist(ab)

# Imágenes de aspiradoras en posición final
for (x, y) in posiciones_aspiradoras:
    imagebox = OffsetImage(aspiradora_img, zoom=0.05)
    ab = AnnotationBbox(imagebox, (x, y), frameon=False)
    ax.add_artist(ab)

# Configuración final
ax.set_xlim(-1, ancho)
ax.set_ylim(-1, alto)
ax.set_xticks(range(ancho))
ax.set_yticks(range(alto))
ax.grid(True)
ax.set_title(f"Simulación Finalizada\n"
             f"Porcentaje Limpio: {porcentaje_limpio:.2f}%\n"
             f"Movimientos Totales: {total_movimientos}\n"
             f"Tiempo de Ejecución: {tiempo_ejecucion:.2f} segundos")

plt.draw()
plt.show()
