# Detector de Dados Pessoais (LGPD) - Hackathon Participa DF

**Categoria:** Acesso à Informação

## Descrição do Projeto
Este projeto consiste em um script em Python desenvolvido para automatizar a identificação de dados pessoais sensíveis em documentos públicos e pedidos de acesso à informação. O objetivo é apoiar a conformidade com a Lei Geral de Proteção de Dados (LGPD), garantindo a tarja correta de informações antes da publicação.

A solução utiliza uma abordagem híbrida para mitigar falsos positivos, combinando validação matemática (para documentos numerados) e Processamento de Linguagem Natural (para nomes e contextos).

## Funcionalidades Técnicas

### 1. Validação de Dados Estruturados (Regex e Matemática)
Diferente de buscas simples por texto, o sistema valida a integridade dos dados:
* **CPF:** Verifica formato e aplica o algoritmo de dígito verificador (Módulo 11) para confirmar se o documento é real.
* **Cartão de Crédito:** Identifica sequências numéricas de cartões financeiros.

### 2. Análise Contextual e Regionalização
Implementação de regras de negócio específicas para evitar falsos positivos comuns na administração pública:
* **RGs:** São identificados apenas quando acompanhados de termos qualificadores (ex: "RG", "Identidade", "SSP"), evitando confusão com valores monetários ou numeração de processos.
* **Endereços do DF:** O sistema foi adaptado para reconhecer a nomenclatura urbana de Brasília (SQN, SQS, Blocos, Setores), além dos logradouros convencionais.

### 3. Detecção de Nomes (NLP) e Filtro de Exclusão
Utiliza a biblioteca *spaCy* (modelo `pt_core_news_sm`) para reconhecimento de entidades nomeadas.
* **Blacklist Administrativa:** Foi implementado um filtro de exclusão para impedir que termos burocráticos (como "Relatório de Auditoria", "Secretaria de Estado", "Diário Oficial") sejam classificados erroneamente como nomes de pessoas.

## Requisitos para Execução

* Python 3.8 ou superior
* Biblioteca spaCy
* Modelo de língua portuguesa (`pt_core_news_sm`)

### Instalação das Dependências
```bash
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
