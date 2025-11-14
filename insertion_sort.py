def insertion_sort(arr, key=lambda x: x):
    """
    Implementação do algoritmo Insertion Sort
    
    Args:
        arr: Lista a ser ordenada
        key: Função para extrair a chave de ordenação (padrão: o próprio elemento)
    
    Returns:
        Lista ordenada
    """
    # Criar uma cópia para não modificar a lista original
    sorted_arr = arr.copy()
    
    # Percorrer da posição 1 até o final
    for i in range(1, len(sorted_arr)):
        current = sorted_arr[i]
        current_key = key(current)
        j = i - 1
        
        # Mover elementos maiores que a chave atual para a direita
        while j >= 0 and key(sorted_arr[j]) > current_key:
            sorted_arr[j + 1] = sorted_arr[j]
            j -= 1
        
        # Inserir o elemento na posição correta
        sorted_arr[j + 1] = current
    
    return sorted_arr

# Exemplo de uso e teste
if __name__ == "__main__":
    # Teste com números
    numeros = [64, 34, 25, 12, 22, 11, 90]
    print("Lista original:", numeros)
    print("Lista ordenada:", insertion_sort(numeros))
    
    # Teste com dicionários
    pedidos = [
        {'order_number': 3, 'total': 50.0},
        {'order_number': 1, 'total': 30.0},
        {'order_number': 2, 'total': 40.0}
    ]
    print("\nPedidos originais:", [p['order_number'] for p in pedidos])
    pedidos_ordenados = insertion_sort(pedidos, key=lambda x: x['order_number'])
    print("Pedidos ordenados:", [p['order_number'] for p in pedidos_ordenados])