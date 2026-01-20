import re
import spacy

# --- SETUP DO AMBIENTE ---
print("Inicializando modelo de NLP...")
try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    print("ERRO: Modelo 'pt_core_news_sm' não encontrado.")
    print("Execute: python -m spacy download pt_core_news_sm")
    # Fallback para evitar crash imediato
    import en_core_web_sm
    nlp = en_core_web_sm.load()

def validate_mod11(numeros):
    """
    Algoritmo de validação de CPF (Módulo 11).
    Retorna True apenas se o hash dos dígitos verificadores coincidir.
    """
    if len(numeros) != 11 or len(set(numeros)) == 1: return False
    soma = sum(int(numeros[i]) * (10 - i) for i in range(9))
    d1 = (soma * 10 % 11) % 10
    soma = sum(int(numeros[i]) * (11 - i) for i in range(10))
    d2 = (soma * 10 % 11) % 10
    return d1 == int(numeros[9]) and d2 == int(numeros[10])

def analyze_text(texto):
    findings = []
    
    # --- ETAPA 1: PATTERN MATCHING (REGEX) ---

    # 1. CPF (Regex + Validação Algorítmica)
    regex_cpf = r'(?:\D|^)(\d{3}\.?\d{3}\.?\d{3}-?\d{2})(?:\D|$)'
    for match in re.finditer(regex_cpf, texto):
        cpf_raw = match.group(1)
        cpf_clean = re.sub(r'\D', '', cpf_raw)
        
        if validate_mod11(cpf_clean):
            findings.append(f"[CRÍTICO] CPF detectado: {cpf_raw}")

    # 2. RG (Lookaround Contextual)
    # Exige a presença de keywords (RG, Identidade, SSP) para evitar falsos positivos com inteiros.
    regex_rg = r'(?:RG|Identidade|Reg\.? Geral)[:\s]\s*(\d{1,2}\.?\d{3}\.?\d{3}-?[\dX])'
    for match in re.finditer(regex_rg, texto, re.IGNORECASE):
        findings.append(f"[ALERTA] Documento RG detectado: {match.group(1)}")

    # 3. Detecção de Endereços
    # Padrão A: Logradouros comuns
    regex_street = r'(?:Rua|Av\.|Avenida|Alameda|Travessa|Estrada)\s+[A-Za-zÀ-ú\s\.]+,?\s*\d+'
    for match in re.finditer(regex_street, texto, re.IGNORECASE):
        findings.append(f"[ATENÇÃO] Endereço detectado: {match.group()}")

    # Padrão B: Endereçamento Regional (Distrito Federal)
    regex_df = r'(?:SQN|SQS|CLN|CLS|Q\.|Quadra|SHIS|SHTN|QE|QI|Q\s?nm)\s*\d+\s*(?:Bloco|Conjunto|Conj\.|Casa|Lt\.|Lote)?\s*[A-Z0-9]*'
    for match in re.finditer(regex_df, texto, re.IGNORECASE):
        findings.append(f"[ATENÇÃO] Endereço (Padrão DF) detectado: {match.group()}")

    # 4. CEP
    regex_cep = r'\b\d{5}-?\d{3}\b'
    for match in re.finditer(regex_cep, texto):
        findings.append(f"[ATENÇÃO] CEP detectado: {match.group()}")

    # 5. E-mail
    regex_email = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    for match in re.finditer(regex_email, texto):
        findings.append(f"[ALERTA] E-mail detectado: {match.group()}")

    # 6. Telefone (Lógica Refinada para evitar Order IDs)
    regex_tel = r'(?:\(?\d{2}\)?\s?)?(?:9\d{4}|\d{4})[-.\s]?\d{4}'
    for match in re.finditer(regex_tel, texto):
        tel_raw = match.group()
        tel_clean = re.sub(r'\D', '', tel_raw)
        
        # Filtro de Sanidade:
        # Se tem 8 dígitos, rejeita se começar com "20" ou "19" (provável ano/data)
        if len(tel_clean) == 8 and (tel_clean.startswith("20") or tel_clean.startswith("19")):
            continue
            
        # Filtro Anti-Pedido:
        # Se tem 8 dígitos e NÃO tem separadores (hífen ou parênteses), ignora.
        # Isso evita capturar números de pedido como "21246328".
        if len(tel_clean) == 8 and "-" not in tel_raw and "(" not in tel_raw:
            continue

        findings.append(f"[ALERTA] Telefone detectado: {tel_raw}")

    # 7. Dados Financeiros (Cartão de Crédito)
    regex_card = r'\b(?:\d{4}[-\s]){3}\d{4}\b'
    for match in re.finditer(regex_card, texto):
        findings.append(f"[CRÍTICO] Cartão de Crédito detectado: {match.group()}")

    # --- ETAPA 2: PROCESSAMENTO DE LINGUAGEM NATURAL (NER) ---
    doc = nlp(texto)
    
    # Blacklist de Termos Administrativos (Stopwords de domínio)
    system_terms = [
        "relatório de auditoria", "governo do distrito", "distrito federal",
        "secretaria de", "diário oficial", "ministério público", 
        "termo de", "controladoria-geral", "sistema de", "ata de", "edital n",
        "pedido n", "nota fiscal", "ordem de serviço"
    ]

    for ent in doc.ents:
        if ent.label_ == "PER":
            if " " in ent.text: # Filtra nomes únicos/apelidos
                name_lower = ent.text.lower()
                is_system_term = False
                
                # Verifica se a entidade está na blacklist
                for term in system_terms:
                    if term in name_lower:
                        is_system_term = True
                        break
                
                if not is_system_term:
                    findings.append(f"[ATENÇÃO] Pessoa Identificada (NLP): {ent.text}")

    return findings

# --- TESTE UNITÁRIO (Execução local) ---
if __name__ == "__main__":
    # Payload de teste com o caso de borda (Pedido vs Telefone)
    test_payload = """
    Status do Pedido Nº: 21246328 (Deve ser IGNORADO).
    Cliente: SARA GUIMARÃES DOS SANTOS.
    Telefone de Contato: (61) 99999-8888 (Deve ser DETECTADO).
    Alternativo: 3344-5566 (Deve ser DETECTADO pois tem hífen).
    Endereço: SQN 102 Bloco A.
    """
    
    print("--- INICIANDO SCAN ---")
    results = analyze_text(test_payload)
    
    if not results:
        print("Nenhum dado sensível encontrado.")
    else:
        for item in results:
            print(item)
