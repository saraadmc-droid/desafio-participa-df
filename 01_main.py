import re
import spacy
import json
import datetime

# --- SETUP ---
print("Inicializando sistema de auditoria e anonimização...")
try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    print("ERRO: Modelo de PLN não encontrado. Instalando fallback...")
    import en_core_web_sm
    nlp = en_core_web_sm.load()

def validate_mod11(numeros):
    """Validação matemática de CPF."""
    if len(numeros) != 11 or len(set(numeros)) == 1: return False
    soma = sum(int(numeros[i]) * (10 - i) for i in range(9))
    d1 = (soma * 10 % 11) % 10
    soma = sum(int(numeros[i]) * (11 - i) for i in range(10))
    d2 = (soma * 10 % 11) % 10
    return d1 == int(numeros[9]) and d2 == int(numeros[10])

def auditar_e_tarjar(texto):
    """
    Função principal que:
    1. Detecta dados sensíveis.
    2. Cria uma versão TARJADA (censurada) do texto.
    3. Gera um relatório estruturado.
    """
    achados = []
    texto_tarjado = texto # Começa igual ao original
    
    # Função auxiliar para registrar e substituir no texto
    def registrar(tipo, valor, risco, span=None):
        achados.append({
            "tipo": tipo,
            "valor_original": valor,
            "risco": risco,
            "timestamp": datetime.datetime.now().isoformat()
        })
        # Substitui o dado real por uma tarja no texto seguro
        nonlocal texto_tarjado
        tarja = f"[{tipo} OMITIDO]"
        texto_tarjado = texto_tarjado.replace(valor, tarja)

    # --- 1. CPF ---
    regex_cpf = r'(?:\D|^)(\d{3}\.?\d{3}\.?\d{3}-?\d{2})(?:\D|$)'
    for match in re.finditer(regex_cpf, texto):
        cpf_clean = re.sub(r'\D', '', match.group(1))
        if validate_mod11(cpf_clean):
            registrar("CPF", match.group(1), "ALTO")

    # --- 2. RG (Contextual) ---
    regex_rg = r'(?:RG|Identidade|Reg\.? Geral)[:\s]\s*(\d{1,2}\.?\d{3}\.?\d{3}-?[\dX])'
    for match in re.finditer(regex_rg, texto, re.IGNORECASE):
        registrar("RG", match.group(1), "MÉDIO")

    # --- 3. Endereços (Genérico) ---
    regex_addr = r'([A-ZÀ-Úa-zà-ú0-9\s\.]+,\s*\d+(?:[/-]\d+)?(?:\s*[A-Za-z]+)?)'
    for match in re.finditer(regex_addr, texto):
        if len(match.group(1).split(',')[0]) > 5:
            registrar("ENDEREÇO", match.group(1), "BAIXO")

    # --- 4. CEP ---
    regex_cep = r'\b\d{5}-?\d{3}\b'
    for match in re.finditer(regex_cep, texto):
        registrar("CEP", match.group(), "MÉDIO")

    # --- 5. E-mail ---
    regex_email = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    for match in re.finditer(regex_email, texto):
        registrar("E-MAIL", match.group(), "MÉDIO")

    # --- 6. Telefone ---
    regex_tel = r'(?:\(?\d{2}\)?\s?)?(?:9\d{4}|\d{4})[-.\s]?\d{4}'
    for match in re.finditer(regex_tel, texto):
        tel_clean = re.sub(r'\D', '', match.group())
        # Filtros (Anos e Pedidos)
        if len(tel_clean) == 8 and (tel_clean.startswith("20") or tel_clean.startswith("19")): continue
        if len(tel_clean) == 8 and "-" not in match.group() and "(" not in match.group(): continue
        registrar("TELEFONE", match.group(), "MÉDIO")

    # --- 7. Cartão de Crédito ---
    regex_card = r'\b(?:\d{4}[-\s]){3}\d{4}\b'
    for match in re.finditer(regex_card, texto):
        registrar("CARTÃO", match.group(), "CRÍTICO")

    # --- 8. IA (Nomes) ---
    doc = nlp(texto)
    ignore_terms = ["relatório", "governo", "distrito", "secretaria", "diário", "ministério", "pedido", "nota"]
    
    for ent in doc.ents:
        if ent.label_ == "PER" and " " in ent.text:
            is_valid = True
            for term in ignore_terms:
                if term in ent.text.lower(): is_valid = False
            
            if is_valid:
                # Nota: A substituição de nomes via replace simples pode ser perigosa se o nome for comum.
                # Aqui registramos, mas a tarja no texto exige cuidado. Vamos tarjar.
                registrar("NOME_PESSOA", ent.text, "BAIXO")

    return achados, texto_tarjado

# --- SIMULAÇÃO DE PRODUÇÃO ---
if __name__ == "__main__":
    # Documento Original (Simulado)
    doc_original = """
    PEDIDO DE ACESSO À INFORMAÇÃO - PROTOCOLO 21246328
    Solicitante: SARA GUIMARÃES DOS SANTOS
    CPF: 123.456.789-09
    Endereço: Rua das Pitangueiras, 40, Águas Claras.
    Contato: (61) 99999-8888 ou sara.santos@email.com
    Solicito cópia do contrato pago com cartão final 1234.
    """

    print("--- 1. ANALISANDO DOCUMENTO ORIGINAL ---")
    print(doc_original.strip())
    print("\n" + "="*40 + "\n")

    # Processamento
    relatorio, doc_seguro = auditar_e_tarjar(doc_original)

    print("--- 2. RELATÓRIO TÉCNICO (JSON) ---")
    # Gera um JSON bonito para provar que é "Tech"
    print(json.dumps(relatorio, indent=4, ensure_ascii=False))
    print("\n" + "="*40 + "\n")

    print("--- 3. DOCUMENTO TARJADO (PRONTO PARA PUBLICAÇÃO) ---")
    print(doc_seguro.strip())
