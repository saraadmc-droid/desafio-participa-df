import re
import spacy

# --- SETUP DO AMBIENTE ---
print("Inicializando modelo de PLN...")
try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    print("ERRO: Modelo 'pt_core_news_sm' não encontrado.")
    import en_core_web_sm
    nlp = en_core_web_sm.load()

def validate_mod11(numeros):
    """Valida CPF matematicamente."""
    if len(numeros) != 11 or len(set(numeros)) == 1: return False
    soma = sum(int(numeros[i]) * (10 - i) for i in range(9))
    d1 = (soma * 10 % 11) % 10
    soma = sum(int(numeros[i]) * (11 - i) for i in range(10))
    d2 = (soma * 10 % 11) % 10
    return d1 == int(numeros[9]) and d2 == int(numeros[10])

def analyze_text(texto):
    findings = []
    
    # --- ETAPA 1: RECONHECIMENTO DE PADRÕES (REGEX) ---

    # 1. CPF
    regex_cpf = r'(?:\D|^)(\d{3}\.?\d{3}\.?\d{3}-?\d{2})(?:\D|$)'
    for match in re.finditer(regex_cpf, texto):
        cpf_clean = re.sub(r'\D', '', match.group(1))
        if validate_mod11(cpf_clean):
            findings.append(f"[CRÍTICO] CPF detectado: {match.group(1)}")

    # 2. RG (Contextual)
    regex_rg = r'(?:RG|Identidade|Reg\.? Geral)[:\s]\s*(\d{1,2}\.?\d{3}\.?\d{3}-?[\dX])'
    for match in re.finditer(regex_rg, texto, re.IGNORECASE):
        findings.append(f"[ALERTA] Documento RG detectado: {match.group(1)}")

    # 3. ENDEREÇO UNIVERSAL (A Regra "Vale-Tudo")
    # Procura por: Texto (pelo menos 2 palavras) + Vírgula + Número
    # Ex: "Rua das Flores, 10" ou "Sitio do Picapau, 50" ou "Area Especial, 4"
    # A regex pega letras maiusculas/minusculas, espaços, até encontrar virgula e numero.
    regex_generic_addr = r'([A-ZÀ-Úa-zà-ú0-9\s\.]+,\s*\d+(?:[/-]\d+)?(?:\s*[A-Za-z]+)?)'
    
    for match in re.finditer(regex_generic_addr, texto):
        # Filtro de sanidade: Endereço deve ter pelo menos 5 letras antes da vírgula
        # para evitar pegar coisas como "Item 1, 2".
        addr_text = match.group(1)
        if len(addr_text.split(',')[0]) > 5:
            findings.append(f"[ATENÇÃO] Possível Endereço (Genérico): {addr_text}")

    # 4. CEP (O Melhor identificador de endereço)
    regex_cep = r'\b\d{5}-?\d{3}\b'
    for match in re.finditer(regex_cep, texto):
        findings.append(f"[ATENÇÃO] CEP detectado: {match.group()}")

    # 5. E-mail
    regex_email = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    for match in re.finditer(regex_email, texto):
        findings.append(f"[ALERTA] E-mail detectado: {match.group()}")

    # 6. Telefone (Com filtros anti-pedido)
    regex_tel = r'(?:\(?\d{2}\)?\s?)?(?:9\d{4}|\d{4})[-.\s]?\d{4}'
    for match in re.finditer(regex_tel, texto):
        tel_clean = re.sub(r'\D', '', match.group())
        if len(tel_clean) == 8 and (tel_clean.startswith("20") or tel_clean.startswith("19")): continue
        if len(tel_clean) == 8 and "-" not in match.group() and "(" not in match.group(): continue
        findings.append(f"[ALERTA] Telefone detectado: {match.group()}")

    # 7. Cartão de Crédito
    regex_card = r'\b(?:\d{4}[-\s]){3}\d{4}\b'
    for match in re.finditer(regex_card, texto):
        findings.append(f"[CRÍTICO] Cartão de Crédito detectado: {match.group()}")

    # --- ETAPA 2: PLN (NOMES E LOCAIS) ---
    doc = nlp(texto)
    
    system_terms = [
        "relatório de auditoria", "governo do distrito", "distrito federal",
        "secretaria de", "diário oficial", "ministério público", "nota fiscal", "pedido n"
    ]

    for ent in doc.ents:
        # DETECÇÃO DE PESSOAS
        if ent.label_ == "PER" and " " in ent.text:
            is_valid = True
            for term in system_terms:
                if term in ent.text.lower():
                    is_valid = False
                    break
            if is_valid:
                findings.append(f"[ATENÇÃO] Pessoa Identificada (PLN): {ent.text}")
        
        # DETECÇÃO DE LOCAIS (Cidades, Países, Endereços desconhecidos)
        # LOC = Locais, GPE = Geopolítico (Cidades/Estados)
        elif ent.label_ in ["LOC", "GPE"]:
            # Ignora nomes de locais muito comuns que não são endereços residenciais
            if ent.text.lower() not in ["brasil", "distrito federal", "brasília"]:
                findings.append(f"[INFO] Localização Identificada (PLN): {ent.text}")

    return findings

# --- TESTE UNITÁRIO ---
if __name__ == "__main__":
    test_payload = """
    Cliente: SARA GUIMARÃES DOS SANTOS.
    Residente em: Fazenda Pôr do Sol, 45.
    Outro endereço: Área Isolada Norte, 10.
    CEP: 70000-000.
    Telefone: (61) 99999-8888.
    """
    
    print("--- INICIANDO AUDITORIA ---")
    results = analyze_text(test_payload)
    for item in results:
        print(item)
