# 🛡️ Solução de Detecção de Dados Pessoais - Desafio Participa DF
> **Categoria:** Acesso à Informação
> **Status:** ✅ Solução Validada

Esta solução implementa um pipeline de auditoria automática para identificar dados pessoais sensíveis em documentos públicos, conforme exigido pela LGPD.

A abordagem é híbrida, unindo a precisão matemática de **Expressões Regulares (Regex)** com a inteligência contextual de **Processamento de Linguagem Natural (NLP/IA)**.

## 🧠 Lógica da Solução (Diferenciais)

O algoritmo opera em **3 Camadas de Defesa** para minimizar Falsos Positivos:

1.  **Camada Matemática (Alta Precisão):**
    * **CPF:** Não apenas identifica o formato, mas valida os dígitos verificadores (algoritmo Módulo 11).
    * **Cartão de Crédito:** Detecta sequências financeiras válidas (ex: 4 blocos de 4 dígitos).

2.  **Camada Contextual (Filtro de Ruído):**
    * **RG:** Utiliza "Lookaround" para identificar RGs apenas se acompanhados de termos como "RG", "Identidade" ou "SSP", evitando confusão com valores monetários.
    * **Endereços:** Adaptado para a realidade do GDF, detectando padrões locais como `SQN`, `SQS`, `Bloco`, `Setor`, além de logradouros comuns (`Rua`, `Av.`).

3.  **Camada de Inteligência Artificial (spaCy):**
    * Utiliza o modelo `pt_core_news_sm` para detectar Nomes de Pessoas (`PER`).
    * **Lista de Exclusão (Blacklist):** Implementa filtro administrativo para ignorar termos burocráticos que parecem nomes (ex: "Relatório de Auditoria", "Secretaria de Estado", "Diário Oficial"), garantindo que apenas pessoas reais sejam marcadas.

## 🛠️ Instalação e Dependências

A solução foi desenvolvida em **Python 3**.

1.  **Instale as bibliotecas necessárias:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Baixe o modelo de língua portuguesa da IA:**
    ```bash
    python -m spacy download pt_core_news_sm
    ```

## 🚀 Como Executar

Para realizar a varredura em um arquivo ou texto:

```bash
python main.py
