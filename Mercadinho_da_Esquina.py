import random
import os
import time
import json

def salvar_jogo(dados):
    with open("save_game.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4)
    print("\n💾 Progresso salvo com sucesso!")
    print("Quando desejar pode voltar aqui e continuar seu progresso!")

def carregar_jogo():
    if os.path.exists("save_game.json"):
        with open("save_game.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return None

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_dollar(valor):
    return f"${valor:.2f}"

def jogar_comercio():
    save = carregar_jogo()
    
    # 1. CARREGAR SAVE OU VALORES DE FÁBRICA
    if save:
        confirmar = input("Deseja carregar o jogo salvo? (s/n): ").lower()
        if confirmar == 's':
            saldo = save["saldo"]
            estoque = save["estoque"]
            dia = save["dia"]
            popularidade = save["popularidade"]
            experiencia = save["experiencia"]
            print("✅ Jogo carregado com sucesso!")
            time.sleep(1)
        else:
            save = None

    if not save:
        saldo = 500.0
        estoque = {"Maçã": 10, "Pão": 10, "Leite": 5, "Ovo": 20, "Café": 5, "Chocolate": 5, "Detergente": 5, 'Arroz': 8, 'Carne': 5}
        dia = 1
        popularidade = 10
        experiencia = 0

    # 2. CONFIGURAÇÕES FIXAS
    custo_compra_base = {"Maçã": 2.0, "Pão": 1.5, "Leite": 4.0, "Ovo": 0.50, "Café": 8.0, "Chocolate": 5.0, "Detergente": 4.50, "Arroz": 4.50, "Carne": 15.0}
    custo_compra = custo_compra_base.copy()
    precos_tabela = {k: v * 2 for k, v in custo_compra_base.items()}
    
    duracao_evento = 0
    evento_atual = ""
    msg_evento = ""
    aluguel = 65.0
    total_vendas_valor = 0
    modificador_demanda = 1.0 

    # Funções e configurações movidas para FORA do while para otimização
    def aplicar_roubo():
        total_perdido = 0
        for item in estoque:
            limite_perda = int(estoque[item] // 2.3)
            # Indentação corrigida: o if agora roda dentro do for
            if limite_perda > 0:
                perda = random.randint(1, limite_perda)
                estoque[item] -= perda
                total_perdido += perda
                
        if total_perdido > 0:
            print(f"😨 Você perdeu um total de {total_perdido} itens do seu estoque!")
        return custo_compra_base.copy()

    CONFIG_EVENTOS = {
        "inflacao": {
            "msg": "📈 INFLAÇÃO: Custos subiram 25%!", 
            "dias": 5, 
            "demanda": 1.0,
            "efeito": lambda: {k: v * 1.25 for k, v in custo_compra_base.items()}
        },
        "promocao": {
            "msg": "🏷️ OFERTAS IMPERDÍVEIS: Todos os produtos com 30% de desconto!", 
            "dias": 3, 
            "demanda": 1.0,
            "efeito": lambda: {k: v * 0.70 for k, v in custo_compra_base.items()}
        },
        "chuva": {
            "msg": "⛈️ TEMPESTADE: Menos clientes hoje.", 
            "dias": 7, 
            "demanda": 0.7,
            "efeito": None
        },
        "festa": {
            "msg": "🎉 FESTA NO BAIRRO: Clientes pagam mais!", 
            "dias": 3, 
            "demanda": 2.1,
            "efeito": None
        },
        "roubo": {
            "msg": "🚨 ROUBO: Alguém roubou parte do seu estoque!", 
            "dias": 1, 
            "demanda": 1.0,
            "efeito": aplicar_roubo # Chama a função corretamente agora
        }
    }

    # --- O LOOP DO JOGO COMEÇA AQUI ---
    while saldo > 0:
        limpar_tela()
        nivel = (experiencia // 15) + 1
        
        print("="*48)
        print(f"      🏪 MERCADINHO DA ESQUINA - DIA {dia}")
        print(f"    Nível: {nivel} ⭐ | Popularidade: {popularidade} ❤️")
        print("="*48)
        print(f"💰 SEU SALDO ATUAL É: {format_dollar(saldo)}")
        print(f"📦 SEU ESTOQUE ATUAL É:")
        itens_lista = list(estoque.items())
        for i in range(0, len(itens_lista), 3):
            linha = "  ".join([f"• {k}: {v}".ljust(15) for k, v in itens_lista[i:i+3]])
            print(linha)
        print(f"{'-'*48}")

        # --- LOOP DE EVENTOS (RODADA) ---
        # ERRO CORRIGIDO: Este bloco inteiro estava fora da identação
        if duracao_evento > 0:
            duracao_evento -= 1
            print(f"📢 EVENTO ATIVO: {msg_evento} (Restam {duracao_evento} dias)")
        else:
            evento_atual = ""
            modificador_demanda = 1.0
            custo_compra = custo_compra_base.copy()

        if duracao_evento == 0 and dia > 1 and random.random() < 0.40:
            evento_atual = random.choice(list(CONFIG_EVENTOS.keys()))
            dados = CONFIG_EVENTOS[evento_atual]
            
            msg_evento = dados["msg"]
            duracao_evento = dados["dias"] - 1
            modificador_demanda = dados["demanda"]
            
            print(f"📢 NOVO EVENTO: {msg_evento}")
            
            if dados["efeito"]:
                custo_compra = dados["efeito"]()
            else:
                custo_compra = custo_compra_base.copy()

        # --- MENU ---
        print(f"\n[1] Comprar Estoque  [2] Abrir Loja  [3] Sair do Jogo [4] Salvar Jogo")
        escolha = input(">> Escolha uma Opção: ")
        if escolha == "3": break
        
        if escolha == "4":
            dados_para_salvar = {
                "saldo": saldo,
                "estoque": estoque,
                "dia": dia,
                "popularidade": popularidade,
                "experiencia": experiencia
            }
            salvar_jogo(dados_para_salvar)
            input("Pressione ENTER para continuar...")
            continue

        if escolha == "1":
            while True:
                print(f"\n--- FORNECEDOR (Saldo: {format_dollar(saldo)}) ---")
                for item, preco in custo_compra.items():
                    print(f"• {item.ljust(10)}: {format_dollar(preco)}")
                
                compra_item = input("\nO que gostaria de comprar para o seu estoque? (Ou 'voltar'): ").capitalize()
                
                # ERRO CORRIGIDO: O capitalize() deixa a palavra 'Voltar' com V maiúsculo. 
                if compra_item == "Voltar": break
                
                if compra_item in custo_compra:
                    try:
                        qtd = int(input(f"Adicione a quantidade de {compra_item} que quer comprar: "))
                        if qtd > 0:
                            custo_total = qtd * custo_compra[compra_item]
                            if saldo >= custo_total:
                                saldo -= custo_total
                                estoque[compra_item] += qtd
                                print(f"✅ Compra feita! Foi adicionado {qtd} de {compra_item} ao estoque.")
                            else: print("❌ Sem dinheiro! Não comprou nada.")
                    except ValueError: print("⚠️ Inválido.")
                if input("\nContinuar comprando? (s/n): ").lower() != 's': break

        elif escolha == "2":
            print("\n🔔 Abrindo o Mercadinho...")
            time.sleep(0.7)

            perfis = {
                "Econômico": {"limite": 2.0, "emoji": "💸"},
                "Apressado": {"limite": 2.8, "emoji": "🏃"},
                "Generoso":  {"limite": 3.5, "emoji": "💎"},
                "Chef Gourmet": {"limite": 4.0, "emoji": "👨‍🍳"},
                "Influencer": {"limite": 1.3, "emoji": "📸"},
                "Fiscal":     {"emoji": "👮"},
                "Revendedor": {"limite": 1.8, "emoji": "🚚"},
                "Vizinha chata": {"limite": 1.2, "emoji": "👵"} # Erro de digitação corrigido (Visinha -> Vizinha)
            }
            
            num_clientes = int((popularidade / 4 + nivel) * modificador_demanda)
            clientes_do_dia = random.choices(list(perfis.keys()), k=max(1, num_clientes))

            for nome_perfil in clientes_do_dia:
                perfil = perfis[nome_perfil]
                
                if nome_perfil == "Fiscal":
                    print(f"\n{perfil['emoji']} ATENÇÃO: O FISCAL ENTROU NA LOJA!")
                    item_checado = random.choice(list(precos_tabela.keys()))
                    preco_atual = precos_tabela[item_checado]
                    custo_base = custo_compra_base[item_checado]
                    
                    if preco_atual > custo_base * 3:
                        multa = saldo * 0.15
                        saldo -= multa
                        popularidade -= 3
                        print(f" 🚨 MULTA! Preço abusivo em {item_checado}. Pagou {format_dollar(multa)}!")
                        print(" Se eu ver você fazendo isso de novo!\n Vou fechar seu mercadinho!")
                    else:
                        print(f" ✅ Tudo certo com {item_checado}.")
                        print(f" Fiscal saiu satisfeito.\n Mas pode voltar a qualquer momento...")
                    input("Precione [ENTER] para continuar...")
                    continue

                # ERRO CORRIGIDO: Removida a linha que apagava a escolha 'prod' feita abaixo
                if nome_perfil == "Chef Gourmet":
                    itens_caros = [item for item, custo in custo_compra_base.items() if custo >= 5.00]
                    prod = random.choice(itens_caros)
                else:
                    prod = random.choice(list(estoque.keys()))

                custo_base_venda = custo_compra[prod]
                limite_aceitavel = custo_base_venda * perfil.get("limite", 2.0)
                if evento_atual == "festa": limite_aceitavel *= 1.2

                print(f"\n{perfil['emoji']} {nome_perfil} está a procura de {prod}.\nE está disposto a pagar até: {format_dollar(limite_aceitavel)} pelo produto.")
                
                if estoque[prod] > 0:
                    try:
                        preco_venda = float(input(f"  Preço (Custo: {custo_base_venda:.2f}): "))
                        precos_tabela[prod] = preco_venda
                        
                        if preco_venda <= limite_aceitavel:
                            qtd_venda = random.randint(1, 3)
                            if nome_perfil == "Revendedor": qtd_venda = random.randint(5, 10)
                            
                            if estoque[prod] >= qtd_venda:
                                ganho = preco_venda * qtd_venda
                                saldo += ganho
                                total_vendas_valor += ganho
                                estoque[prod] -= qtd_venda
                                experiencia += 2 if nome_perfil == "Influencer" else 1
                                popularidade += 1
                                print(f" 💰 VENDIDO! ele comprou {qtd_venda} por {format_dollar(ganho)}")
                            else: print(" ⚠️ Estoque insuficiente!")
                        else:
                            print(" 😡 'Muito caro!' Cliente saiu sem nada da loja")
                            popularidade -= 1
                    except ValueError: print(" ⚠️ Erro no valor.")
                else:
                    print(f"  ❌ Falta {prod}!")
                    popularidade -= 1

            # Pagamento do aluguel
            print("\n" + "-"*48)
            print(f"🏠 Pagando aluguel foi descontado: -{format_dollar(aluguel)} do seu saldo.")
            print(f"Clientes do dia: {len(clientes_do_dia)} | Total vendas acumulado: {format_dollar(total_vendas_valor)}")
            saldo -= aluguel
            dia += 1
            input("\n[ENTER para o próximo dia]")

    print(f"\n🛑 FIM DE JOGO! Dias sobrevividos: {dia-1}")
    print(f"💰 Saldo final: {format_dollar(saldo)}")
    print(f"Numero total de vendas: {format_dollar(total_vendas_valor)}")
    print(f"Experiência acumulada: {experiencia} | Nível final: {(experiencia // 15) + 1}")

if __name__ == "__main__":
    jogar_comercio()