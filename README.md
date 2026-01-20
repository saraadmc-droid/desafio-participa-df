# Automação de Proteção de Dados (Participa DF)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![NLP](https://img.shields.io/badge/AI-spaCy-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

> **Categoria:** Acesso à Informação | **Desafio:** Transparência com Privacidade.

## Sobre o Projeto
O objetivo é processar documentos públicos e identificar automaticamente dados pessoais sensíveis, gerando uma versão segura para publicação.

A ferramenta resolve o problema da revisão manual, mitigando riscos de vazamento de dados, através de uma abordagem híbrida de **Expressões Regulares (Regex)** e **Processamento de Linguagem Natural (PLN)**.

---

## Diferenciais Técnicos

Muitas soluções de mercado dependem de APIs externas ou validações superficiais. A minha abordagem foi desenhada com foco em **Soberania de Dados** e **Engenharia Robusta**:

### 1. Privacidade (Local & Offline)
Diferente de soluções que enviam dados para APIs de terceiros (como OpenAI/ChatGPT), este script roda **100% localmente**.
* **O dado do cidadão nunca sai do ambiente do GDF.**
* Não há custos com tokens de API.
* Conformidade total com a soberania de dados exigida pela LGPD.

### 2. Validação Matemática Real
Fugi do erro comum de usar apenas "Expressões Regulares (Regex)" simples.
* **CPF:** O sistema implementa o algoritmo de **Módulo 11**. Ele não apenas acha números com 11 dígitos, ele calcula se o dígito verificador é válido. Se for um número aleatório, o sistema ignora.
* **Cartão de Crédito:** Detecta sequências financeiras válidas, ignorando números longos de processos ou matrículas.

### 3. Inteligência Contextual 
Regras de negócio para evitar Falsos Positivos:
* **Protocolos vs Telefones:** O algoritmo distingue um número de matrícula/protocolo (ex: `21246328`) de um telefone.
* **Blacklist Administrativa:** A IA foi treinada para ignorar termos, focando apenas em nomes de pessoas físicas.

---

## O Pipeline de Processamento

1.  **Entrada:** Texto cru (copiado de processos, e-mails ou PDFs).
2.  **Processamento Híbrido:**
    * *Camada 1:* Validação Matemática (CPF/Cartão).
    * *Camada 2:* Regex Contextual (RG, E-mail, Telefone).
    * *Camada 3:* IA/PLN com spaCy (Nomes e Locais não estruturados).
3.  **Saída:**
    * **Relatório JSON:** Log técnico estruturado com nível de risco.
    * **Texto Tarjado:** Versão do documento pronta para publicação (ex: `[CPF OMITIDO]`).

---

## Como Executar

A solução foi desenvolvida em **Python 3** pela facilidade e manutenção.

### Instalação
```bash
pip install -r requirements.txt
python -m spacy download pt_core_news_sm

---
