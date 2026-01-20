import re
import spacy
import json
import datetime
import time

# --- SETUP INICIAL ---
print("Inicializando sistema de anonimização e auditoria...")

try:
    # Carrega o modelo de IA em português
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    print("AVISO: Modelo 'pt_core_news_sm' não encontrado. Usando fallback 'en_core_web_sm'.")
    print("Dica: Execute 'python -m spacy download pt_core_news_sm' no terminal.")
    import en_core_web_sm
    nlp = en_core_web_sm.load()

def validate_mod11(numeros):
    """
    Validação matemática de CPF segundo o algoritmo de Módulo 11.
    Lógica:
    1. Calcula o primeiro dígito verificador usando pesos de 10 a 2.
    2. Calcula o segundo dígito usando pesos de 11 a 2.
    3. Verifica se os dígitos calculados coincidem com os informados.
    Evita falsos positivos de sequências aleatórias (ex: 111.111.111-11).
    """
    if len(numeros) != 11 or len(set(numeros)) == 1:
        return False
    soma = sum(int(numeros[i]) * (10 - i) for i in range(9))
    d1 = (soma * 10 % 11) % 10
    soma = sum(int(numeros[i]) * (11 - i) for i in range(10))
    d2 = (soma * 10 % 11) % 10
    return d1 == int(numeros[9]) and d2 == int(numeros[10])

def anonimizar(texto):
    """
    Função Core que:
    1. Detecta dados pessoais sensíveis (Regex + IA).
    2. Cria uma versão TARJADA (segura) do texto.
    3. Gera um relatório estruturado dos riscos.
    """
    achados = []
    texto_tarjado = texto

    # Função auxiliar para registrar os dados encontrados e aplicar a tarja
    def registrar(tipo, valor, risco, span=None):
        achados.append({
            "tipo": tipo,
            "valor_original": valor,
            "risco": risco,
            "posicao": span,
            "timestamp": datetime.datetime.now().isoformat()
        })
        nonlocal texto_tarjado
        # Cria a tarja visual, ex: [CPF OMITIDO]
        tarja = f"[{tipo} OMITIDO]"
        texto_tarjado = texto_tarjado.replace(valor, tarja)

    # --- CAMADA 1: DADOS ESTRUTURADOS (REGEX) ---

    # 1. CPF (Com validação Módulo 11)
    regex_cpf = r'(?:\D|^)(\d{3}\.?\d{3}\.?\d{3}-?\d{2})(?:\D|$)'
    for match in re.finditer(regex_cpf, texto):
        cpf_limpo = re.sub(r'\D', '', match.group(1))
        if validate_mod11(cpf_limpo):
            registrar("CPF", match.group(1), "ALTO", match.span())

    # 2. RG (Contextual - exige palavras-chave para evitar falsos positivos)
    regex_rg = r'(?:RG|Identidade|Reg\.? Geral)[:\s]\s*(\d{1,2}\.?\d{3}\.?\d{3}-?[\dX])'
    for match in re.finditer(regex_rg, texto, re.IGNORECASE):
        registrar("RG", match.group(1), "MÉDIO", match.span())

    # 3. Endereço Universal (Detecta padrão Logradouro + Vírgula + Número)
    regex_addr = r'([A-ZÀ-Úa-zà-ú0-9\s\.]+,\s*\d+(?:[/-]\d+)?(?:\s*[A-Za-z]+)?)'
    for match in re.finditer(regex_addr, texto):
        # Filtro de sanidade: Endereço deve ter pelo menos 5 chars antes da vírgula
        if len(match.group(1).split(',')[0]) > 5:
            registrar("ENDEREÇO", match.group(1), "BAIXO", match.span())

    # 4. CEP
    regex_cep = r'\b\d{5}-?\d{3}\b'
    for match in re.finditer(regex_cep, texto):
        registrar("CEP", match.group(), "MÉDIO", match.span())

    # 5. E-mail
    regex_email = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    for match in re.finditer(regex_email, texto):
        registrar("E-MAIL", match.group(), "MÉDIO", match.span())

    # 6. Telefone (Com filtros anti-ruído para Protocolos/Datas)
    regex_tel = r'(?:\(?\d{2}\)?\s?)?(?:9\d{4}|\d{4})[-.\s]?\d{4}'
    for match in re.finditer(regex_tel, texto):
        tel_clean = re.sub(r'\D', '', match.group())
        
        # Filtro A: Ignora anos recentes (ex: 2025, 2026) se tiver 8 digitos
        if len(tel_clean) == 8 and (tel_clean.startswith("20") or tel_clean.startswith("19")): continue
        # Filtro B: Ignora números secos (protocolos) sem formatação de telefone
        if len(tel_clean) == 8 and "-" not in match.group() and "(" not in match.group(): continue
        
        registrar("TELEFONE", match.group(), "MÉDIO", match.span())

    # 7. Cartão de Crédito
    regex_card = r'\b(?:\d{4}[-\s]){3}\d{4}\b'
    for match in re.finditer(regex_card, texto):
        registrar("CARTÃO", match.group(), "CRÍTICO", match.span())

    # --- CAMADA 2: INTELIGÊNCIA ARTIFICIAL (PLN) ---
    doc = nlp(texto)
    
    # Blacklist de termos administrativos que parecem nomes mas não são
    termos_ignorados = [
        "relatório", "governo", "distrito", "secretaria", "diário", 
        "ministério", "pedido", "nota", "fiscal", "auditoria"
    ]

    for ent in doc.ents:
        # Pessoas (PER)
        if ent.label_ == "PER" and " " in ent.text:
            eh_valido = True
            for termo in termos_ignorados:
                if termo in ent.text.lower():
                    eh_valido = False
                    break
            
            if eh_valido:
                # Na IA, como o replace direto pode falhar se houver homônimos,
                # registramos o achado. A substituição no texto seguro é feita
                # com cuidado, mas aqui aplicaremos a regra geral.
                registrar("NOME_PESSOA", ent.text, "BAIXO", (ent.start_char, ent.end_char))

    return achados, texto_tarjado

# --- SIMULAÇÃO DE PROCESSAMENTO EM LOTE (BATCH) ---
# Demonstra escalabilidade e capacidade de processar filas de pedidos
if __name__ == "__main__":
    
    # Simulação de um banco de dados de pedidos chegando via API/Sistema
    fila_pedidos = [
        {
            "id": "REQ-2025-001",
            "conteudo": "Solicito acesso aos gastos. Meu CPF é 123.456.789-09 e moro na SQS 102 Bloco A."
        },
        {
            "id": "REQ-2025-002",
            "conteudo": "Gostaria de saber sobre o andamento do processo 21246328 (Protocolo)."
        },
        {
            "id": "REQ-2025-003",
            "conteudo": "Denúncia anônima sobre a obra da escola."
        },
        {
            "id": "REQ-2025-004",
            "conteudo": "Contato para retorno: (61) 99999-8888 ou maria.silva@email.com."
        }
    ]

    print(f"--- INICIANDO PROCESSAMENTO EM LOTE ({len(fila_pedidos)} ITENS) ---")
    inicio = time.time()

    relatorio_consolidado = []

    for pedido in fila_pedidos:
        print(f"Processando ID: {pedido['id']}...")
        riscos, texto_seguro = anonimizar(pedido["conteudo"])
        
        # Se encontrou riscos, adiciona ao relatório final
        if riscos:
            relatorio_consolidado.append({
                "id_pedido": pedido["id"],
                "total_riscos": len(riscos),
                "dados_detectados": riscos,
                "versao_publicavel": texto_seguro
            })

    fim = time.time()
    tempo_total = fim - inicio

    print("\n" + "="*50)
    print(f"🏁 AUDITORIA CONCLUÍDA EM {tempo_total:.4f} SEGUNDOS")
    print("="*50 + "\n")

    if relatorio_consolidado:
        print("--- RELATÓRIO TÉCNICO DE SAÍDA (JSON) ---")
        print(json.dumps(relatorio_consolidado, indent=4, ensure_ascii=False))
    else:
        print("✅ Nenhum dado sensível encontrado na fila processada.")
