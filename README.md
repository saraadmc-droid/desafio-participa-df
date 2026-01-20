#  Anonimização Inteligente
### Desafio Participa DF | Categoria: Acesso à Informação

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![NLP](https://img.shields.io/badge/AI-spaCy-green)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

## Objetivo do Projeto
Esta solução foi desenvolvida para automatizar a identificação de **dados pessoais sensíveis** em pedidos de Acesso à Informação (LAI), garantindo a conformidade com a **Lei Geral de Proteção de Dados (LGPD)**.

O sistema atua como um "filtro inteligente" que processa documentos, valida a veracidade dos dados (matemática) e o contexto (IA), gerando automaticamente uma versão tarjada (anonimizada) pronta para publicação no Portal Participa DF.

---

## Diferenciais Técnicos e Robustez

Para mitigar falsos positivos e garantir a segurança jurídica, a solução utiliza uma abordagem híbrida:

### 1. Validação Algorítmica (Não apenas Regex)
* **CPF:** Implementação do algoritmo **Módulo 11** (Dígitos Verificadores). O sistema ignora sequências numéricas aleatórias e detecta apenas documentos válidos.
* **Cartão de Crédito:** Validação de padrões financeiros (PAN) de 16 dígitos.

### 2. Inteligência Artificial Contextual (PLN)
Utilizamos a biblioteca **spaCy** (`pt_core_news_sm`) para Processamento de Linguagem Natural.
* **Detecção de Nomes:** Identifica nomes de pessoas em textos não estruturados.
* **Filtro de Ruído:** Blacklist inteligente que ignora termos administrativos do GDF (ex: "Secretaria de Estado", "Relatório Anual"), evitando que órgãos públicos sejam marcados como pessoas.

### 3. Regras de Negócio (Anti-Falso Positivo)
* **Telefone vs. Protocolo:** Algoritmo capaz de distinguir um número de telefone real de um número de protocolo ou matrícula (comum em documentos públicos), baseando-se em formatação e dígitos.
* **Privacidade por Design:** A solução roda **100% Offline**. Nenhum dado do cidadão é enviado para APIs externas (como ChatGPT), garantindo a soberania dos dados.

---

## Estrutura do Projeto

A organização dos arquivos segue as boas práticas de engenharia de software:

* `main.py`: **Script Principal**. Contém a lógica de validação matemática, o pipeline de IA e o motor de anonimização.
* `requirements.txt`: Lista de todas as dependências necessárias para instalação automatizada.
* `gold_standard.json`: Conjunto de dados "gabarito" (Gold Standard) para validação de métricas.
* `avaliacao.py`: Script de benchmark que calcula **Precisão** e **Recall** do modelo estatisticamente.
* `README.md`: Documentação técnica do projeto.

---

## Instalação e Configuração

### Pré-requisitos
* **Linguagem:** Python 3.9 ou superior.
* **Gerenciador de Pacotes:** pip.

### Passo a Passo
1.  **Clone o repositório** (ou baixe os arquivos):
    ```bash
    git clone [https://github.com/saraadmc-droide/desafio-participa-df.git](https://github.com/saraadmc-droide/desafio-participa-df.git)
    cd desafio-participa-df
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Baixe o modelo de língua portuguesa:**
    ```bash
    python -m spacy download pt_core_news_sm
    ```

---

## Como Executar

Para iniciar a auditoria e anonimização, execute o script principal. O sistema simulará o processamento de um lote de pedidos (Batch Processing).

```bash
python main.py
