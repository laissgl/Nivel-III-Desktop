from sqlalchemy.orm import joinedload
from banco import (
    criar_banco, Restaurante, Produto, Cliente,
    Funcionario, Pedido, Pagamento
)

import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


session = criar_banco()


def criar_restaurantes_padrao():
    if session.query(Restaurante).count() > 0:
        return
    r1 = Restaurante(categoria="Pizzaria", nome="Fratello Uno")
    r1.produtos = [
        Produto(nome="Pizza Margherita", preco=75.00),
        Produto(nome="Pizza Calabresa", preco=80.00),
        Produto(nome="Refrigerante", preco=6.00)
    ]
    r2 = Restaurante(categoria="Cafeteria", nome="Studio Grão")
    r2.produtos = [
        Produto(nome="Toast Presunto de Parma", preco=32.00),
        Produto(nome="Brownie", preco=24.00),
        Produto(nome="Café Gelado", preco=17.00)
    ]
    r3 = Restaurante(categoria="Japonesa", nome="Gurume")
    r3.produtos = [
        Produto(nome="Combo Sushi 20 peças", preco=90.00),
        Produto(nome="Temaki Salmão", preco=30.00),
        Produto(nome="Água com gás", preco=5.00)
    ]
    r4 = Restaurante(categoria="Italiana", nome="Babbo")
    r4.produtos = [
        Produto(nome="Gnocchi de Abóbora", preco=75.00),
        Produto(nome="Lasanha de Filé", preco=70.00),
        Produto(nome="Suco Natural", preco=9.00)
    ]
    session.add_all([r1, r2, r3, r4])
    session.commit()



def submenu_restaurantes():
    while True:
        print("\n----- RESTAURANTES E CARDÁPIOS -----")
        print("[1] Ver os restaurantes e seus cardápios")
        print("[0] Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")
        clear()

        if opcao == "1":
            restaurantes = session.query(Restaurante).options(joinedload(Restaurante.produtos)).all()
            print("\n----- LISTA COMPLETA DE RESTAURANTES E CARDÁPIOS -----")
            for r in restaurantes:
                print(f"\n🍽️  {r.nome} ({r.categoria})")
                print("-" * (len(r.nome) + len(r.categoria) + 6))
                for item in r.produtos:
                    print(f"• {item.nome} - R${item.preco:.2f}")
            print("\n-------------------------------------------")

        elif opcao == "0":
            break
        else:
            print("Opção inválida!")



def perguntar_clube():
    while True:
        resposta = input("É membro do clube? (Sim/Não): ").strip().lower()
        if resposta in ["sim", "s"]:
            return True
        elif resposta in ["não", "nao", "n"]:
            return False
        else:
            print("Resposta inválida! Digite 'Sim' ou 'Não'.")



def submenu_clientes():
    while True:
        print("\n----- CADASTRO DE CLIENTES -----")
        print("[1] Cadastrar novo cliente")
        print("[2] Listar clientes cadastrados")
        print("[0] Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")
        clear()

        if opcao == "1":
            while True:
                nome = input("Digite o nome do cliente: ")
                if any(char.isdigit() for char in nome):
                    print("Nome inválido! Não pode conter números. Tente novamente.")
                elif nome.strip() == "":
                    print("Nome não pode ser vazio. Tente novamente.")
                else:
                    break

            while True:
                cpf = input("Digite o CPF: ")
                cpf_limpo = cpf.replace(".", "").replace("-", "").replace(" ", "")
                if not cpf_limpo.isdigit():
                    print("CPF inválido! Não pode conter letras. Tente novamente.")
                elif len(cpf_limpo) < 11 or len(cpf_limpo) > 14:
                    print("CPF inválido! Deve conter entre 11 e 14 dígitos. Tente novamente.")
                else:
                    break

            while True:
                numero = input("Digite o número de telefone: ")
                numero_limpo = numero.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                if not numero_limpo.isdigit():
                    print("Número inválido! Não pode conter letras ou caracteres especiais. Tente novamente.")
                elif len(numero_limpo) < 9 or len(numero_limpo) > 15:
                    print("Número inválido! Deve conter entre 9 e 15 dígitos. Tente novamente.")
                else:
                    break

            clube = perguntar_clube()
            cliente = Cliente(nome=nome, cpf=cpf, telefone=numero, clube=clube)
            session.add(cliente)
            session.commit()
            print(f"\nCliente {nome} cadastrado com sucesso!")

        elif opcao == "2":
            clientes = session.query(Cliente).all()
            if not clientes:
                print("\nNenhum cliente cadastrado ainda.")
            else:
                print("\n--- CLIENTES ---")
                for c in clientes:
                    status = "Clube" if c.clube else "Comum"
                    print(f"- {c.nome} ({status})")

        elif opcao == "0":
            break
        else:
            print("Opção inválida!")



def submenu_funcionarios():
    while True:
        print("\n----- CADASTRO DE FUNCIONÁRIOS -----")
        print("[1] Cadastrar novo funcionário")
        print("[2] Listar funcionários cadastrados")
        print("[0] Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")
        clear()

        if opcao == "1":
            while True:
                nome = input("Digite o nome: ")
                if any(char.isdigit() for char in nome):
                    print("Nome inválido! Não pode conter números. Tente novamente.")
                elif nome.strip() == "":
                    print("Nome não pode ser vazio. Tente novamente.")
                else:
                    break

            while True:
                cpf = input("Digite o CPF: ")
                cpf_limpo = cpf.replace(".", "").replace("-", "").replace(" ", "")
                if not cpf_limpo.isdigit():
                    print("CPF inválido! Não pode conter letras. Tente novamente.")
                elif len(cpf_limpo) < 11 or len(cpf_limpo) > 14:
                    print("CPF inválido! Deve conter entre 11 e 14 dígitos. Tente novamente.")
                else:
                    break

            while True:
                numero = input("Digite o número de telefone: ")
                numero_limpo = numero.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                if not numero_limpo.isdigit():
                    print("Número inválido! Não pode conter letras ou caracteres especiais. Tente novamente.")
                elif len(numero_limpo) < 9 or len(numero_limpo) > 15:
                    print("Número inválido! Deve conter entre 9 e 15 dígitos. Tente novamente.")
                else:
                    break

            while True:
                cargo = input("Digite o cargo: ").strip()
                if cargo == "":
                    print("Cargo não pode ser vazio. Tente novamente.")
                elif any(char.isdigit() for char in cargo):
                    print("Cargo inválido! Não pode conter números. Tente novamente.")
                else:
                    break

            while True:
                salario_str = input("Digite o salário: R$")
                try:
                    salario = float(salario_str.replace(",", "."))
                    if salario < 0:
                        print("Salário não pode ser negativo. Tente novamente.")
                        continue
                    break
                except ValueError:
                    print("Valor inválido para salário. Tente novamente.")

            funcionario = Funcionario(
                nome=nome, cpf=cpf, telefone=numero,
                cargo=cargo, salario=salario
            )
            session.add(funcionario)
            session.commit()
            print(f"\nFuncionário {nome} cadastrado com sucesso!")

        elif opcao == "2":
            funcionarios = session.query(Funcionario).all()
            if not funcionarios:
                print("Nenhum funcionário cadastrado ainda.")
            else:
                print("\n----- FUNCIONÁRIOS -----")
                for f in funcionarios:
                    print(f"- {f.nome} ({f.cargo})")

        elif opcao == "0":
            break
        else:
            print("Opção inválida!")



def submenu_pedidos():
    clear()
    clientes = session.query(Cliente).all()
    if not clientes:
        print("\nNenhum cliente cadastrado! Cadastre-se antes de fazer um pedido.")
        return

    
    print("\n----- CLIENTES CADASTRADOS -----")
    for i, c in enumerate(clientes, 1):
        print(f"{i}. {c.nome}")
    try:
        indice_cliente = int(input("Escolha o cliente: ")) - 1
        cliente_escolhido = clientes[indice_cliente]
    except (ValueError, IndexError):
        print("Escolha inválida.")
        return

    
    pedidos_anteriores = session.query(Pedido).filter_by(cliente_id=cliente_escolhido.id).all()
    if pedidos_anteriores:
        print(f"\nPedidos anteriores de {cliente_escolhido.nome}:")
        for i, p in enumerate(pedidos_anteriores, 1):  
            
            if p.pagamento:
                tipo_pagamento = p.pagamento.tipo.lower()
            else:
                tipo_pagamento = "pix"

            valor_entrega = 5.0 if tipo_pagamento in ["cartao", "cartão"] else 3.0
            total_produtos = sum(item.preco for item in p.produtos)
            total = total_produtos + valor_entrega
            if p.cliente.clube:
                total *= 0.9

            print(f"\nPedido #{i}")
            print(f"Restaurante: {p.restaurante.nome}")
            print(f"Forma de pagamento: {tipo_pagamento.title()}")
            print(f"Valor da entrega: R${valor_entrega:.2f}")
            print(f"Total: R${total:.2f} {'(desconto 10% clube)' if p.cliente.clube else ''}")
            print("Itens do pedido:")
            produtos_contagem = {}
            for item in p.produtos:
                produtos_contagem[item.nome] = produtos_contagem.get(item.nome, 0) + 1
            for nome, qtd in produtos_contagem.items():
                preco_unit = next(prod.preco for prod in p.restaurante.produtos if prod.nome == nome)
                print(f"• {nome} - R${preco_unit * qtd:.2f}")

    
    restaurantes = session.query(Restaurante).options(joinedload(Restaurante.produtos)).all()
    print("\n----- RESTAURANTES DISPONÍVEIS -----")
    for i, r in enumerate(restaurantes, 1):
        print(f"{i}. {r.nome} ({r.categoria})")
    try:
        indice_restaurante = int(input("Escolha o restaurante: ")) - 1
        restaurante_escolhido = restaurantes[indice_restaurante]
    except (ValueError, IndexError):
        print("Escolha inválida.")
        return

    
    pedido = Pedido(cliente=cliente_escolhido, restaurante=restaurante_escolhido)
    session.add(pedido)
    session.commit()

    
    while True:
        clear()
        print(f"\nCardápio de {restaurante_escolhido.nome}:")
        for i, p in enumerate(restaurante_escolhido.produtos, 1):
            print(f"{i}. {p.nome} - R${p.preco:.2f}")
        try:
            escolha = int(input("Escolha o número do produto (0 para finalizar): "))
        except ValueError:
            print("Entrada inválida! Digite um número.")
            continue

        if escolha == 0:
            break

        if 1 <= escolha <= len(restaurante_escolhido.produtos):
            item = restaurante_escolhido.produtos[escolha - 1]
            pedido.produtos.append(item)
            print(f"'{item.nome}' adicionado ao pedido.")
        else:
            print("Número inválido.")

    if not pedido.produtos:
        print("Pedido vazio! Nenhum item selecionado.")
        session.delete(pedido)
        session.commit()
        return

    while True:
        tipo_pagamento = input("\nForma de pagamento (Pix ou Cartão): ").strip().lower()
        if tipo_pagamento in ["pix", "cartao", "cartão"]:
            break
        print("Pagamento inválido! Digite 'Pix' ou 'Cartão'.")

    valor_entrega = 5.0 if tipo_pagamento in ["cartao", "cartão"] else 3.0
    total_produtos = sum(p.preco for p in pedido.produtos)
    total = total_produtos + valor_entrega
    if cliente_escolhido.clube:
        total *= 0.9
        print("\nDesconto de 10% aplicado para cliente do clube!")

    pagamento = Pagamento(tipo=tipo_pagamento, valor_total=total)
    pedido.pagamento = pagamento
    session.commit()

    
    clear()
    print("\n----- RESUMO DO PEDIDO -----")
    print(f"Cliente: {cliente_escolhido.nome}")
    print(f"Restaurante: {restaurante_escolhido.nome}")
    print("Itens do pedido:")
    produtos_contagem = {}
    for item in pedido.produtos:
        produtos_contagem[item.nome] = produtos_contagem.get(item.nome, 0) + 1
    for nome, qtd in produtos_contagem.items():
        preco_unit = next(p.preco for p in restaurante_escolhido.produtos if p.nome == nome)
        print(f"• {nome} - R${preco_unit * qtd:.2f}")
    print(f"\nForma de pagamento: {pagamento.tipo.title()}")
    print(f"Valor da entrega: R${valor_entrega:.2f}")
    print(f"Total final: R${pagamento.valor_total:.2f} {'(desconto 10% clube)' if cliente_escolhido.clube else ''}")
    print("\nObrigado por escolher nosso sistema de restaurante! Volte sempre!")
    input("\nPressione Enter para voltar ao menu principal")



def main():
    criar_restaurantes_padrao()
    while True:
        print("\n----- SISTEMA DE RESTAURANTE -----")
        print("[1] Restaurantes e Cardápios")
        print("[2] Cadastro de Clientes")
        print("[3] Cadastro de Funcionários")
        print("[4] Fazer Pedido")
        print("[0] Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            submenu_restaurantes()
        elif opcao == "2":
            submenu_clientes()
        elif opcao == "3":
            submenu_funcionarios()
        elif opcao == "4":
            submenu_pedidos()
        elif opcao == "0":
            print("Encerrando o sistema. Até mais!")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
