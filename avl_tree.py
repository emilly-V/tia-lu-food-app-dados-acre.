class AVLNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None
    
    def _get_height(self, node):
        if not node:
            return 0
        return node.height
    
    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _update_height(self, node):
        if node:
            node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
    
    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        
        # Realizar rotação
        x.right = y
        y.left = T2
        
        # Atualizar alturas
        self._update_height(y)
        self._update_height(x)
        
        return x
    
    def _rotate_left(self, x):
        y = x.right
        T2 = y.left
        
        # Realizar rotação
        y.left = x
        x.right = T2
        
        # Atualizar alturas
        self._update_height(x)
        self._update_height(y)
        
        return y
    
    def _insert_node(self, node, key, value):
        # Passo 1: Inserção normal de BST
        if not node:
            return AVLNode(key, value)
        
        if key < node.key:
            node.left = self._insert_node(node.left, key, value)
        elif key > node.key:
            node.right = self._insert_node(node.right, key, value)
        else:
            # Chaves duplicadas não são permitidas (atualiza o valor)
            node.value = value
            return node
        
        # Passo 2: Atualizar altura do nó ancestral
        self._update_height(node)
        
        # Passo 3: Obter o fator de balanceamento
        balance = self._get_balance(node)
        
        # Passo 4: Casos de desbalanceamento
        
        # Caso Left Left
        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)
        
        # Caso Right Right
        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)
        
        # Caso Left Right
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        # Caso Right Left
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def insert(self, key, value):
        """Insere um nó na árvore AVL"""
        self.root = self._insert_node(self.root, key, value)
    
    def _search_node(self, node, key):
        if not node or node.key == key:
            return node.value if node else None
        
        if key < node.key:
            return self._search_node(node.left, key)
        else:
            return self._search_node(node.right, key)
    
    def search(self, key):
        """Busca um nó na árvore AVL"""
        return self._search_node(self.root, key)
    
    def _in_order_traversal(self, node, result):
        if node:
            self._in_order_traversal(node.left, result)
            result.append(node.value)
            self._in_order_traversal(node.right, result)
    
    def get_sorted_items(self):
        """Retorna todos os itens em ordem crescente de chave"""
        result = []
        self._in_order_traversal(self.root, result)
        return result
    
    def _print_tree(self, node, level=0, prefix="Root: "):
        if node:
            print(" " * (level * 4) + prefix + str(node.key))
            if node.left or node.right:
                if node.left:
                    self._print_tree(node.left, level + 1, "L--- ")
                if node.right:
                    self._print_tree(node.right, level + 1, "R--- ")
    
    def print_tree(self):
        """Imprime a árvore de forma hierárquica"""
        print("\n--- Estrutura da Árvore AVL ---")
        self._print_tree(self.root)
        print()

# Exemplo de uso
if __name__ == "__main__":
    avl = AVLTree()
    
    # Inserir alguns valores
    valores = [10, 20, 30, 40, 50, 25]
    for val in valores:
        avl.insert(val, f"valor_{val}")
    
    # Buscar valores
    print("Buscar 30:", avl.search(30))
    print("Buscar 99:", avl.search(99))
    
    # Imprimir árvore
    avl.print_tree()
    
    # Obter itens ordenados
    print("Itens ordenados:", [item for item in avl.get_sorted_items()])