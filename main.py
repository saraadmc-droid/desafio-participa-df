import re
import spacy

# --- CONFIGURAÇÃO INICIAL ---
print("Carregando cérebro da Inteligência Artificial...")
try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    print("ERRO: O modelo de IA não foi encontrado.")
    print("Rode no Colab: !python -m spacy download pt_core_news_sm")
    import en_core_web_sm
    nlp = en_core_web_sm.load()

def validar_cpf(numeros):
    """Auditoria Matemática: Verifica os dois dígitos verificadores do CPF."""
    if len(numeros) != 11 or len(set(numeros)) == 1: return False
    soma = sum(int(numeros[i]) * (10 - i) for i in range(9))
    d1 = (soma * 10 % 11) % 10
    soma = sum(int(numeros[i]) * (11 - i) for i in range(10))
    d2 = (soma * 10 % 11) % 10
    return d1 == int(numeros[9]) and d2 == int(numeros[10])

def analisar_texto_completo(texto):
    resultados = []
    
    # --- CAMADA 1: AUDITORIA DE FORMATOS (REGEX) ---

    # 1. CPF (Com validação matemática)
    regex_cpf = r'(?:\D|^)(\d{3}\.?\d{3}\.?\d{3}-?\d{2})(?:\D|$)'
    for match in re.finditer(regex_cpf, texto):
        cpf_bruto = match.group(1)
        cpf_limpo = re.sub(r'\D', '', cpf_bruto)
        if validar_cpf(cpf_limpo):
            resultados.append(f"[CRÍTICO] CPF Válido detectado: {cpf_bruto}")

    # 2. RG (Baseado em Contexto)
    regex_rg = r'(?:RG|Identidade|Reg\.? Geral)[:\s]\s*(\d{1,2}\.?\d{3}\.?\d{3}-?[\dX])'
    for match in re.finditer(regex_rg, texto, re.IGNORECASE):
        resultados.append(f"[ALERTA] RG detectado: {match.group(1)}")

    # 3. ENDEREÇO COMPLETO (Novo Módulo GDF)
    # Padrão 1: Ruas e Avenidas
    regex_rua = r'(?:Rua|Av\.|Avenida|Alameda|Travessa|Estrada)\s+[A-Za-zÀ-ú\s\.]+,?\s*\d+'
    for match in re.finditer(regex_rua, texto, re.IGNORECASE):
        resultados.append(f"[ATENÇÃO] Endereço (Logradouro) detectado: {match.group()}")

    # Padrão 2: Endereços de Brasília (SQN, SQS, etc.)
    regex_bsb = r'(?:SQN|SQS|CLN|CLS|Q\.|Quadra|SHIS|SHTN|QE|QI|Q\s?nm)\s*\d+\s*(?:Bloco|Conjunto|Conj\.|Casa|Lt\.|Lote)?\s*[A-Z0-9]*'
    for match in re.finditer(regex_bsb, texto, re.IGNORECASE):
        resultados.append(f"[ATENÇÃO] Endereço (Brasília/DF) detectado: {match.group()}")

    # 4. CEP (Continua importante como backup)
    regex_cep = r'\b\d{5}-?\d{3}\b'
    for match in re.finditer(regex_cep, texto):
        resultados.append(f"[ATENÇÃO] CEP detectado: {match.group()}")

    # 5. E-mail
    regex_email = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    for match in re.finditer(regex_email, texto):
        resultados.append(f"[ALERTA] E-mail detectado: {match.group()}")

    # 6. Telefone (Com filtro de ano)
    regex_tel = r'(?:\(?\d{2}\)?\s?)?(?:9\d{4}|\d{4})[-.\s]?\d{4}'
    for match in re.finditer(regex_tel, texto):
        tel_bruto = match.group()
        tel_limpo = re.sub(r'\D', '', tel_bruto)
        if len(tel_limpo) == 8 and (tel_limpo.startswith("20") or tel_limpo.startswith("19")):
            continue
        resultados.append(f"[ALERTA] Telefone detectado: {tel_bruto}")

    # 7. Cartão de Crédito
    regex_cartao = r'\b(?:\d{4}[-\s]){3}\d{4}\b'
    for match in re.finditer(regex_cartao, texto):
        resultados.append(f"[CRÍTICO] Cartão de Crédito detectado: {match.group()}")

    # --- CAMADA 2: INTELIGÊNCIA ARTIFICIAL (NOMES) ---
    doc = nlp(texto)
    
    # LISTA DE EXCLUSÃO (Blacklist atualizada)
    termos_ignorados = [
        "relatório de auditoria", "governo do distrito", "distrito federal",
        "secretaria de", "diário oficial", "ministério público", 
        "termo de", "controladoria-geral", "sistema de", "ata de", "edital n"
    ]

    for entidade in doc.ents:
        if entidade.label_ == "PER":
            if " " in entidade.text: # Tem sobrenome
                # Verifica Blacklist
                nome_lower = entidade.text.lower()
                eh_termo_tecnico = False
                for termo in termos_ignorados:
                    if termo in nome_lower:
                        eh_termo_tecnico = True
                        break
                
                if not eh_termo_tecnico:
                    resultados.append(f"[ATENÇÃO] Nome Pessoal (IA): {entidade.text}")

    return resultados

# --- EXEMPLO DE EXECUÇÃO ---
if __name__ == "__main__":
    texto_exemplo = """
    Ata de Reunião - 20/01/2026.
    O servidor João da Silva reside na SQN 302 Bloco B.
    Seu RG é 1.234.567 SSP/DF e o CEP 70000-000.
    """
    print("--- INICIANDO AUDITORIA ---")
    analise = analisar_texto_completo(texto_exemplo)
    for item in analise:
        print(item)
