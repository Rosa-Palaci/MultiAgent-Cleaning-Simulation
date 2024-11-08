import matplotlib.pyplot as plt
import numpy as np
from aspiradora_modelo import AspiradoraModelo

def representar_aspiradoras(modelo):
    """Con esta funcion asignamos la posicion de nuestras aspiradoras y de las celdas sucias."""
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

# Número de pasos de nuestra simulación
for i in range(100):
    modelo.step()  # Vamos avanzando por pasos

    # Obtenemos las posiciones de nuestros agentes y de las celdas sucias
    posiciones_aspiradoras, celdas_sucias = representar_aspiradoras(modelo)

    # Para que limpiemos el gráfico
    ax.clear()

    # Mostramos nuestras celdas sucias como puntos rojos
    if celdas_sucias:
        x_sucias, y_sucias = zip(*celdas_sucias)
        ax.scatter(x_sucias, y_sucias, color='red', label='Celdas Sucias', s=100)

    # Mostramos nuestras aspiradoras como los puntos azules
    if posiciones_aspiradoras:
        x_aspiradoras, y_aspiradoras = zip(*posiciones_aspiradoras)
        ax.scatter(x_aspiradoras, y_aspiradoras, color='blue', label='Aspiradoras', s=200)

    # Configuraciones de nuestro gráfico
    ax.set_xlim(-1, ancho)
    ax.set_ylim(-1, alto)
    ax.set_title(f"Paso de simulación: {i+1}")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_xticks(range(ancho))
    ax.set_yticks(range(alto))
    ax.grid(True)
    ax.legend()

    # Hacemos pausas para que se vea el efecto de la animación
    plt.pause(0.1)

    # Verificamos si todas las celdas están limpias y terminamos la simulación en dado caso
    if not celdas_sucias:
        print("Todas las celdas están limpias. Terminando la simulación.")
        break

# Obtenemos los resultados finales
completado, porcentaje_limpio, total_movimientos, tiempo_ejecucion = modelo.obtener_resultados()

# Una vez que se haya terminado la simulación limpiamos el gráfico para enseñar los resultados
ax.clear()

# Mostramos las celdas que quedaron sucias
if modelo.celdas_sucias:
    x_sucias, y_sucias = zip(*modelo.celdas_sucias)
    ax.scatter(x_sucias, y_sucias, color='red', label='Celdas Sucias', s=100)

# Mostramos a nuestras aspiradoras en su posición final
if posiciones_aspiradoras:
    x_aspiradoras, y_aspiradoras = zip(*posiciones_aspiradoras)
    ax.scatter(x_aspiradoras, y_aspiradoras, color='blue', label='Aspiradoras', s=200)

# Configuraciones para mostrar los resultados obtenidos
ax.set_xlim(-1, ancho)
ax.set_ylim(-1, alto)
ax.set_xticks(range(ancho))
ax.set_yticks(range(alto))
ax.grid(True)
ax.legend()

# Finalmente mostramos nuestros resultados obtenidos
ax.set_title(f"Simulación Finalizada\n"
             f"Porcentaje Limpio: {porcentaje_limpio:.2f}%\n"
             f"Movimientos Totales: {total_movimientos}\n"
             f"Tiempo de Ejecución: {tiempo_ejecucion:.2f} segundos")

plt.draw()
plt.show()
