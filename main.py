import json
import os
from insertion_sort import insertion_sort
from avl_tree import AVLTree

# Arquivo para persistência dos dados
DATA_FILE = "restaurant_data.json"

class RestaurantSystem:
    def __init__(self):
        self.items = []
        self.orders = []
        self.items_tree = AVLTree()
        self.orders_tree = AVLTree()
        self.next_order_id = 1
        self.load_data()
    
    def load_data(self):
        """Carrega os dados do arquivo JSON"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    
                    # Carregar itens
                    self.items = data.get('items', [])
                    for item in self.items:
                        self.items_tree.insert(item['id'], item)
                    
                    # Carregar pedidos
                    self.orders = data.get('orders', [])
                    for order in self.orders:
                        self.orders_tree.insert(order['order_number'], order)
                    
                    # Definir próximo ID de pedido
                    if self.orders:
                        self.next_order_id = max(order['order_number'] for order in self.orders) + 1
                        
            except Exception as e:
                print(f"Erro ao carregar dados: {e}")
                self.items = []
                self.orders = []
    
    def save_data(self):
        """Salva os dados no arquivo JSON"""
        try:
            data = {
                'items': self.items,
                'orders': self.orders
            }
            with open(DATA_FILE, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
    
    def registrar_item(self):
        """Registra um novo item no menu"""
        print("\n--- Registrar Novo Item ---")
        
        item_id = len(self.items) + 1
        nome = input("Nome do item: ")
        preco = float(input("Preço do item: "))
        categoria = input("Categoria do item: ")
        descricao = input("Descrição do item: ")
        
        item = {
            'id': item_id,
            'nome': nome,
            'preco': preco,
            'categoria': categoria,
            'descricao': descricao
        }
        
        self.items.append(item)
        self.items_tree.insert(item_id, item)
        self.save_data()

        print(f"Item '{nome}' registrado com sucesso! (ID: {item_id})")
    
    def listar_itens(self):
        """Lista todos os itens do menu"""
        print("\n--- ITENS DO MENU ---")
        if not self.items:
            print("Nenhum item cadastrado.")
            return
        
        for item in self.items:
            print(f"ID: {item['id']} | Nome: {item['nome']} | Preço: R${item['preco']:.2f} | Categoria: {item['categoria']}")
    
    def realizar_pedido(self):
        """Realiza um novo pedido"""
        print("\n--- Realizar Novo Pedido ---")
        
        if not self.items:
            print("Não há itens disponíveis no menu.")
            return
        
        self.listar_itens()
        
        order_items = []
        while True:
            try:
                item_id = int(input("\nDigite o ID do item (0 para finalizar): "))
                if item_id == 0:
                    break
                
                # Buscar item na árvore
                item = self.items_tree.search(item_id)
                if item:
                    quantidade = int(input(f"Quantidade de '{item['nome']}': "))
                    order_items.append({
                        'item_id': item_id,
                        'nome': item['nome'],
                        'preco': item['preco'],
                        'quantidade': quantidade
                    })
                    print(f"Item '{item['nome']}' adicionado ao pedido.")
                else:
                    print("Item não encontrado!")
            
            except ValueError:
                print("Por favor, digite um número válido.")
        
        if not order_items:
            print("Nenhum item adicionado ao pedido.")
            return
        
        # Calcular total
        total = sum(item['preco'] * item['quantidade'] for item in order_items)
        
        order = {
            'order_number': self.next_order_id,
            'items': order_items,
            'total': total,
            'status': 'pendente',
            'cliente': input("Nome do cliente: ")
        }
        
        self.orders.append(order)
        self.orders_tree.insert(self.next_order_id, order)
        self.next_order_id += 1
        self.save_data()
        
        print(f"\nPedido #{order['order_number']} realizado com sucesso!")
        print(f"Total: R${total:.2f}")
        print(f"Status: {order['status']}")
    
    def adicionar_item_pedido(self):
        """Adiciona um item a um pedido existente"""
        print("\n--- Adicionar Item ao Pedido ---")
        
        if not self.orders:
            print("Não há pedidos cadastrados.")
            return
        
        try:
            order_number = int(input("Número do pedido: "))
            order = self.orders_tree.search(order_number)
            
            if not order:
                print("Pedido não encontrado!")
                return
            
            self.listar_itens()
            item_id = int(input("ID do item a adicionar: "))
            item = self.items_tree.search(item_id)
            
            if not item:
                print("Item não encontrado!")
                return
            
            quantidade = int(input(f"Quantidade de '{item['nome']}': "))
            
            # Adicionar item ao pedido
            new_item = {
                'item_id': item_id,
                'nome': item['nome'],
                'preco': item['preco'],
                'quantidade': quantidade
            }
            
            order['items'].append(new_item)
            order['total'] += item['preco'] * quantidade
            
            self.save_data()
            print(f"Item '{item['nome']}' adicionado ao pedido #{order_number}")
            
        except ValueError:
            print("Por favor, digite um número válido.")
    
    def aceitar_pedido(self):
        """Aceita um pedido pendente"""
        print("\n--- Aceitar Pedido ---")
        
        pending_orders = [order for order in self.orders if order['status'] == 'pendente']
        
        if not pending_orders:
            print("Não há pedidos pendentes.")
            return
        
        print("Pedidos pendentes:")
        for order in pending_orders:
            print(f"Pedido #{order['order_number']} - Cliente: {order['cliente']} - Total: R${order['total']:.2f}")
        
        try:
            order_number = int(input("\nNúmero do pedido a aceitar: "))
            order = self.orders_tree.search(order_number)
            
            if order and order['status'] == 'pendente':
                order['status'] = 'aceito'
                self.save_data()
                print(f"Pedido #{order_number} aceito com sucesso!")
            else:
                print("Pedido não encontrado ou já foi processado!")
                
        except ValueError:
            print("Por favor, digite um número válido.")
    
    def listar_pedidos_ordenados(self):
        """Lista pedidos ordenados por número usando Insertion Sort"""
        print("\n--- Pedidos (Ordenados por Número) ---")
        
        if not self.orders:
            print("Nenhum pedido cadastrado.")
            return
        
        # Ordenar pedidos usando Insertion Sort
        sorted_orders = insertion_sort(self.orders, key=lambda x: x['order_number'])
        
        for order in sorted_orders:
            print(f"\nPedido #{order['order_number']}")
            print(f"Cliente: {order['cliente']}")
            print(f"Status: {order['status']}")
            print(f"Total: R${order['total']:.2f}")
            print("Itens:")
            for item in order['items']:
                print(f"  - {item['nome']} (x{item['quantidade']}) - R${item['preco'] * item['quantidade']:.2f}")
    
    def buscar_pedido(self):
        """Busca um pedido usando a árvore AVL"""
        print("\n--- Buscar Pedido ---")
        
        try:
            order_number = int(input("Número do pedido: "))
            order = self.orders_tree.search(order_number)
            
            if order:
                print(f"\nPedido #{order['order_number']} encontrado!")
                print(f"Cliente: {order['cliente']}")
                print(f"Status: {order['status']}")
                print(f"Total: R${order['total']:.2f}")
                print("Itens:")
                for item in order['items']:
                    print(f"  - {item['nome']} (x{item['quantidade']}) - R${item['preco'] * item['quantidade']:.2f}")
            else:
                print("Pedido não encontrado!")
                
        except ValueError:
            print("Por favor, digite um número válido.")
    
    def buscar_item(self):
        """Busca um item usando a árvore AVL"""
        print("\n--- Buscar Item ---")
        
        try:
            item_id = int(input("ID do item: "))
            item = self.items_tree.search(item_id)
            
            if item:
                print(f"\nItem encontrado!")
                print(f"ID: {item['id']}")
                print(f"Nome: {item['nome']}")
                print(f"Preço: R${item['preco']:.2f}")
                print(f"Categoria: {item['categoria']}")
                print(f"Descrição: {item['descricao']}")
            else:
                print("Item não encontrado!")
                
        except ValueError:
            print("Por favor, digite um número válido.")

def main():
    system = RestaurantSystem()
    
    while True:
        print("\n=== SISTEMA DE PEDIDOS - RESTAURANTE ===")
        print("1. Registrar item")
        print("2. Listar itens")
        print("3. Realizar pedido")
        print("4. Adicionar item ao pedido")
        print("5. Aceitar pedido")
        print("6. Listar pedidos ordenados")
        print("7. Buscar pedido")
        print("8. Buscar item")
        print("0. Sair")
        
        choice = input("\nEscolha uma opção: ")
        
        if choice == '1':
            system.registrar_item()
        elif choice == '2':
            system.listar_itens()
        elif choice == '3':
            system.realizar_pedido()
        elif choice == '4':
            system.adicionar_item_pedido()
        elif choice == '5':
            system.aceitar_pedido()
        elif choice == '6':
            system.listar_pedidos_ordenados()
        elif choice == '7':
            system.buscar_pedido()
        elif choice == '8':
            system.buscar_item()
        elif choice == '0':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
