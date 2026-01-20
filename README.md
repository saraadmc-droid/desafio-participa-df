# Detector Inteligente de Dados Pessoais - Desafio Participa DF

**Categoria:** Acesso à Informação

## Sobre o Projeto
Esta solução foi desenvolvida para automatizar a identificação e classificação de dados pessoais em documentos públicos. O objetivo é utilizar tecnologia para garantir a privacidade dos cidadãos no portal Participa DF, agilizando a análise de pedidos de acesso à informação.

O sistema utiliza um pipeline híbrido de Inteligência Artificial e Processamento de Linguagem Natural (NLP), garantindo alta precisão na detecção de dados sensíveis como CPF, RG, E-mail, Telefone e Nomes.

## Diferenciais Técnicos

### 1. Alta Precisão com Validação Algorítmica
O sistema não apenas busca padrões visuais, mas valida matematicamente a integridade dos dados para evitar erros:
* **Validação de CPF:** Implementação do algoritmo de verificação de dígitos (Módulo 11), garantindo que apenas documentos reais sejam detectados.
* **Filtros Inteligentes:** Regras de negócio que diferenciam números de protocolo, matrículas e valores monetários de telefones e RGs reais.

### 2. Reconhecimento de Entidades (NER)
Utilização da biblioteca **spaCy** (modelo `pt_core_news_sm`) para interpretação semântica de textos.
* A solução identifica nomes de pessoas mesmo em contextos não estruturados.
* Implementação de *Blacklist* para ignorar termos administrativos comuns (ex: nomes de órgãos, secretarias), focando apenas em pessoas físicas.

### 3. Adaptação Regional (GDF)
O algoritmo foi treinado para reconhecer padrões específicos do Distrito Federal, incluindo formatos de endereçamento locais (SQN, SQS, Blocos, Setores), aumentando a efetividade da ferramenta no cenário real do governo.

## Stack Tecnológica

* **Linguagem:** Python 3.8+
* **NLP:** spaCy
* **Manipulação de Texto:** Regex Avançado

## Como Executar o Projeto

### 1. Instalação
Clone o repositório e instale as dependências necessárias:

```bash
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
