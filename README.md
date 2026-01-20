# Detector de Dados Pessoais - Desafio Participa DF

**Categoria:** Acesso à Informação

## O que este projeto faz?
Esta ferramenta serve para **ler documentos automaticamente** e apontar onde existem dados pessoais expostos (CPF, RG, Telefone, Endereço, etc.).

O objetivo é ajudar o governo a proteger a privacidade dos cidadãos (LGPD) antes de tornar um documento público, evitando que dados sensíveis vazem por acidente.

## Principais Funcionalidades

### 1. Validação Real (Não é só visual)
O sistema não procura apenas por "números que parecem CPF". Ele faz o cálculo matemático (dígito verificador) para garantir que o **CPF é válido**. Se for um número inventado, ele ignora.

### 2. Filtros Inteligentes
A ferramenta sabe diferenciar dados reais de outros números comuns em documentos públicos:
* **Telefones:** Diferencia um número de telefone real de um "Número de Pedido" ou "Protocolo".
* **RGs:** Só marca se estiver escrito "RG" ou "Identidade" perto do número, para não confundir com valores em dinheiro.

### 3. Endereços de qualquer tipo
O sistema busca por qualquer estrutura de endereço (Nome da Rua + Número), aceitando desde formatos comuns ("Rua X, 10") até endereços rurais ou específicos de Brasília.

### 4. Inteligência Artificial (PLN)
Usa uma IA de Processamento de Linguagem Natural (PLN) para ler o texto e identificar **Nomes de Pessoas** e **Locais**, mesmo que eles não tenham um formato fixo.

---

## Como Usar

### Passo 1: Instalação
Você precisa do Python instalado. Rode os comandos abaixo para baixar as bibliotecas necessárias:

```bash
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
