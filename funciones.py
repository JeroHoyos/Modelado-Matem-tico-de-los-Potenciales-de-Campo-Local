import networkx as nx
import random
import matplotlib.pyplot as plt

def crear_conexion(somas,conexiones):

    # Lista de todos los nodos
    todos = somas + conexiones

    # Inicializar grafo
    G = nx.MultiGraph()
    G.add_nodes_from(todos)

    # Inicializar parametros
    grados = {n: 0 for n in todos}
    conexiones_iniciales = {n: set() for n in somas}
    max_grado = 3
    grado_minimo_inicial = 2

    # Inicializar los Somas con su conectividad mínima
    for n in somas:
        # Analizar las posibles coneciones
        posibles = [x for x in conexiones if grados[x] < max_grado and x not in conexiones_iniciales[n]]

        if len(posibles) < grado_minimo_inicial:
            print(f"No es posible conectar {n} a {grado_minimo_inicial} nodos distintos sin exceder grado 3.")
            exit()

        #Seleciona el la denditra y axón 
        seleccionados = random.sample(posibles, grado_minimo_inicial)
        
        # Crear la conexión
        for destino in seleccionados:
            # Crear arista
            G.add_edge(n, destino)
            # Actualizar parametros
            grados[n] += 1
            grados[destino] += 1
            conexiones_iniciales[n].add(destino)

    # Inicializar las conexiones
    for nodo in conexiones:
        while grados[nodo] < max_grado:
    
            posibles = [x for x in conexiones if x != nodo and grados[x] < max_grado]

            if not posibles:
                break

            destino = random.choice(posibles)
            # Actualizar parametros
            G.add_edge(nodo, destino)
            grados[nodo] += 1
            grados[destino] += 1

    # Verificar conectividad
    componentes = list(nx.connected_components(nx.Graph(G)))
    no_conexo = False
    if len(componentes) > 1:
        # Intentar conectar componentes sin romper restricciones
        for i in range(1, len(componentes)):
            c1 = list(componentes[i - 1])
            c2 = list(componentes[i])
            nodo1 = next((n for n in c1 if grados[n] < max_grado), None)
            nodo2 = next((n for n in c2 if grados[n] < max_grado and n != nodo1), None)
            if nodo1 and nodo2 and not (nodo1 in somas and nodo2 in somas):
                G.add_edge(nodo1, nodo2)
                grados[nodo1] += 1
                grados[nodo2] += 1
            else:
                no_conexo = True
                break

    if no_conexo:
        print("No es posible generar un grafo conexo sin violar las restricciones de grado.")
        exit()


    plt.figure(figsize=(8, 8))
    pos = nx.spring_layout(G)

    # Colorear nodos
    colors = ['#BAE1FF' if n in somas else '#BFFCC6' for n in G.nodes]
    # Colorear nodos
    nx.draw_networkx_nodes(G, pos, node_size=1000, node_color=colors)
    nx.draw_networkx_labels(G, pos, font_size=14)

    # Aristas con curvatura
    for i, (u, v, k) in enumerate(G.edges(keys=True)):
        nx.draw_networkx_edges(
            G, pos,
            edgelist=[(u, v)],
            connectionstyle=f'arc3,rad={(0.2 * (k + 1))}', # Acá se controla la curvatura
            edge_color='gray'
        )

    plt.title("Multigrafo neuronal")
    plt.axis('off')
    plt.show()
    # Mostrar grados
    print("\nGrados finales:")
    for nodo in G.nodes:
        print(f"{nodo}: {G.degree(nodo)}")

    # Matriz de adyacencia
    adj_matrix = nx.to_numpy_array(G)
    print("Matriz de adyacencia:")
    print(adj_matrix)

    # Matriz de incidencia
    inc_matrix = nx.incidence_matrix(G, oriented=False).toarray()
    print("\nMatriz de incidencia:")
    print(inc_matrix)

    # Mostrar grados
    print("\nGrados finales:")
    for nodo in G.nodes:
        print(f"{nodo}: {G.degree(nodo)}")
