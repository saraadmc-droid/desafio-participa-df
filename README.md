# Guardião LGPD - Automação de Proteção de Dados (Participa DF)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![NLP](https://img.shields.io/badge/AI-spaCy-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

> **Categoria:** Acesso à Informação | **Desafio:** Transparência com Privacidade.

## 🎯 Sobre o Projeto
Esta solução é um **motor de anonimização e auditoria** desenvolvido para o Governo do Distrito Federal (GDF). O objetivo é processar documentos públicos (como pedidos da Lei de Acesso à Informação - LAI) e identificar automaticamente dados pessoais sensíveis, gerando uma versão segura (tarjada) para publicação.

A ferramenta resolve o gargalo da revisão manual, mitigando riscos de vazamento de dados (LGPD) através de uma abordagem híbrida de **Expressões Regulares (Regex)** e **Processamento de Linguagem Natural (PLN)**.

---

## Diferenciais de Robustez

A solução se destaca pela engenharia aplicada para **reduzir falsos positivos** (não marcar o que não é dado pessoal) e garantir a integridade da detecção:

### 1. Camada de Validação Algorítmica (MathCheck)
Não basta encontrar números. O sistema aplica validações matemáticas reais:
* **CPF:** Verifica integridade via algoritmo Módulo 11 (dígitos verificadores). Sequências aleatórias são ignoradas.
* **Cartão de Crédito:** Detecta padrões financeiros (PAN) de 16 dígitos agrupados.

### 2. Inteligência Contextual (Anti-Ruído)
Regras de negócio implementadas para o contexto administrativo:
* **Distinção de Telefones vs. Protocolos:** Um algoritmo analisa a formatação. Números de 8 dígitos "secos" (comuns em números de pedidos ou matrículas) são ignorados; apenas formatos telefônicos válidos (com hífen ou DDD) são capturados.
* **Endereçamento Universal:** Em vez de listas fixas de ruas, o sistema utiliza um padrão estrutural (`Logradouro + Vírgula + Número`) capaz de detectar desde endereços urbanos (SQN, SQS) até rurais, sem necessidade de manutenção constante de listas.

### 3. Anonimização Automática (Privacy by Design)
O script não apenas "alerta", ele **resolve**.
* **Output Sanitizado:** Gera automaticamente uma versão do texto onde os dados sensíveis são substituídos por *placeholders* (ex: `[CPF OMITIDO]`).
* **Relatório JSON:** Gera logs estruturados prontos para integração com APIs ou dashboards de monitoramento do GDF.

---

## Arquitetura da Solução

O pipeline de processamento opera em três estágios:

| Estágio | Tecnologia | Função |
| :--- | :--- | :--- |
| **1. Varredura Rápida** | *Regex Avançado* | Identificação de padrões estruturados (CPF, E-mail, CEP, Cartões). |
| **2. Análise Semântica** | *spaCy (PLN)* | A IA lê o texto para encontrar Entidades Nomeadas (Pessoas e Locais) que não seguem padrão fixo. Inclui *Blacklist* para ignorar nomes de órgãos públicos. |
| **3. Sanitização** | *String Replacement* | Substituição dos dados originais por tags de segurança e geração do relatório de risco. |

---

## Instalação e Uso

### Pré-requisitos
* Python 3.8 ou superior.

### 1. Configuração do Ambiente
Clone o repositório e instale as dependências:

```bash
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
