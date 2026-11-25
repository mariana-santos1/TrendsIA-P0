# TrendsIA P0 - Organizador de Anotações com LLM
Projeto P0 - Primeiro fluxo com LLM referente ao programa de capacitação Trends IA.

Aplicação de linha de comando, escrita em Python, que recebe uma anotação livre e usa um modelo de linguagem (LLM) para transformá-la em uma lista numerada de tarefas com seus respectivos prazos.

## Problema escolhido
Uma pessoa que faz anotações rápidas ao longo do dia, em uma reunião, no celular, ou mesmo em um caderno, precisa transformar esse texto solto em uma lista organizada de tarefas com prazos, porque atualmente relê a anotação, separa manualmente cada item e frequentemente esquece informações mencionados no meio das frases.

## Público-alvo
Pessoas que usam anotações em texto para registrar tarefas e possuem dificuldade em organiza-las de modo padronizado.

## Por que usar um LLM
A tarefa envolve interpretação de linguagem natural:
- as tarefas aparecem em frases diferentes, às vezes na mesma linha;
- os prazos são expressos de formas variadas ("amanhã", "sexta", "até dia 20", "sem prazo");
- a redação é informal e não segue um formato fixo.

Uma solução baseada apenas em regras, por exemplo, dividir o texto por pontos ou palavras-chave, falharia em anotações com itens encadeados, negações ou prazos implícitos. O LLM consegue identificar os itens e normalizar a saída no formato solicitado. A resposta é ainda limitada por um prompt com formato obrigatório, que reduz a variação da saída e evita invenção de informações.

## Funcionamento da solução

### Estrutura do projeto:
└── TrendsIA-P0
    ├── README.md
    ├── requirements.txt
    ├── .env.example
    └── src/
        ├── __init__.py
        ├── config.py
        ├── llm_client.py
        ├── main.py
        ├── organizador.py
        └── prompt.py

### O fluxo implementado é:
1. **Captura da entrada** - `main()` recebe a anotação digitada pelo usuário no terminal.
2. **Validação da entrada** - verifica se a anotação está vazia ou contém apenas espaços em branco.
3. **Carregamento e validação da configuração** - `carregar_configuracoes()`, em `config.py`, carrega as variáveis de ambiente e verifica se os parâmetros necessários estão configurados corretamente.
4. **Preparação do prompt** - `preparar_prompt()`, em `prompt.py`, fornece as instruções que orientam o modelo na identificação e organização das tarefas.
5. **Processamento da anotação** - `organizar_anotacao()`, em `organizador.py`, coordena o processamento da entrada e a chamada ao modelo.
6. **Comunicação com o LLM** - `chamar_llm()`, em `llm_client.py`, prepara e envia a requisição HTTP ao provedor e processa a resposta recebida.
7. **Apresentação do resultado** - `main()` exibe a lista organizada no terminal.

A aplicação também realiza o tratamento de erros relacionados às configurações, credenciais, comunicação com a API, indisponibilidade do serviço e respostas inválidas.

## Limites do projeto
Não possui interface web ou gráfica, aplicativo móvel, autenticação de usuários, banco de dados, RAG, agentes, comparação de modelos, implantação em nuvem e treinamento/ajuste de modelos.

A disponibilidade e o desempenho da aplicação dependem do serviço LLM utilizado, podendo ocorrer limitações de requisições, indisponibilidade temporária ou falhas de comunicação.

## Instalação
Os comandos abaixo foram escritos para **PowerShell no Windows**. Em Linux ou macOS, troque a ativação do ambiente virtual por `source .venv/bin/activate`.

1. Clone o repositório e entre na pasta:
```powershel
git clone <URL-DO-REPOSITORIO>
cd TrendsIA-P0
```
2. Crie e ative um ambiente virtual:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
3. Instale as dependências:
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```
4. Crie o arquivo de configuração local a partir do modelo:
```powershell
Copy-Item .env.example .env
```
5. Edite o `.env` e preencha `LLM_API_KEY` conforme a seção seguinte.

## Configuração do acesso ao LLM

A aplicação utiliza uma interface de comunicação baseada em requisições HTTP, realizada com a biblioteca requests, para acessar um modelo de linguagem.

A configuração inicial utiliza o Google Gemini, por meio do endpoint compatível com a API OpenAI: https://generativelanguage.googleapis.com/v1beta/openai/

A comunicação é realizada diretamente por requisições HTTP, sem utilizar um SDK específico do provedor. Entretanto, a estrutura do projeto utiliza configurações genéricas, permitindo adaptar a comunicação para outros provedores que ofereçam uma interface compatível ou mediante ajustes no módulo llm_client.py.

### Obtenção da chave
1. Acesse o [Google AI Studio](https://aistudio.google.com/app/apikey) com uma conta Google.
2. Crie uma chave de API.
3. Copie a chave e cole no arquivo `.env`, na variável `LLM_API_KEY`.

>A chave **não deve** ser escrita no código, em prints, em commits ou em issues. O arquivo `.env` já está listado no `.gitignore`.

### Variáveis de ambiente

| Variável           | Obrigatória | Padrão no código    | Descrição                                                                                                         |
| ------------------ | ----------- | ------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `LLM_API_BASE_URL` | sim         | -                   | URL base do provedor (ex.: `https://generativelanguage.googleapis.com/v1beta/openai/`)                            |
| `LLM_API_PATH`     | não         | `/chat/completions` | Caminho do endpoint de chat                                                                                       |
| `LLM_API_KEY`      | sim         | -                   | chave de API do provedor                                                                                          |
| `LLM_MODEL`        | sim         | -                   | identificador do modelo disponível na sua conta (o `.env.example` traz um valor de exemplo; ajuste se necessário) |
| `LLM_MAX_TOKENS`   | não         | `2048`              | limite máximo de tokens da resposta                                                                               |
| `LLM_TIMEOUT`      | não         | `60`                | tempo máximo de espera pela resposta, em segundos                                                                 |

Exemplo de `.env` preenchido:
```dotenv
LLM_API_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
LLM_API_PATH=/chat/completions
LLM_API_KEY=sua_chave_aqui
LLM_MODEL=gemini-3.8-flash

LLM_MAX_TOKENS=2048
LLM_TIMEOUT=60
```

>O valor de `LLM_MODEL` precisa ser um modelo habilitado para a sua chave. Consulte a documentação do Google Gemini para a lista atualizada de modelos.

## Execução

Com o ambiente virtual ativado e o `.env` configurado:
```powershell
python -m src.main
```
O programa exibe:
```text
ORGANIZADOR DE ANOTAÇÕES

Digite sua anotação:
```
Digite a anotação e pressione Enter. O resultado é impresso logo abaixo.

## Exemplos de entrada e saída

> Os exemplos abaixo são **ilustrativos do formato esperado**. A redação exata pode variar conforme o modelo e a versão configurada.

### Exemplo 1 — anotação com prazos
Entrada:
```text
Preciso pagar a conta de luz até dia 10. Reunião com o cliente na terça às 14h. Comprar presente de aniversário da Ana.
```
Saída esperada:
```text
1. Tarefa: Pagar a conta de luz
   Prazo: Até dia 10

2. Tarefa: Reunião com o cliente
   Prazo: Terça às 14h

3. Tarefa: Comprar presente de aniversário da Ana
   Prazo: Não definido
```
### Exemplo 2 — anotação sem prazos
Entrada:
```text
revisar o contrato, responder os e-mails pendentes e atualizar o currículo
```
Saída esperada:
```text
1. Tarefa: Revisar o contrato
   Prazo: Não definido

2. Tarefa: Responder os e-mails pendentes
   Prazo: Não definido

3. Tarefa: Atualizar o currículo
   Prazo: Não definido
```
### Exemplo 3 — entrada vazia
Entrada: pressionar Enter sem digitar nada.
Saída:
```text
Erro: A anotação não pode estar vazia.
```
Nesse caso nenhuma chamada ao LLM é realizada.
## Testes: reais e simulados
### Testes reais (com chamada ao LLM)

Executados manualmente durante o desenvolvimento, com a chave configurada:

| Teste                  | Situação                                   | Resultado esperado                                 | Resultado obtido                                                                         |
| ---------------------- | ------------------------------------------ | -------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Conexão com o provedor | chamada mínima ao endpoint do Gemini       | resposta HTTP 200 com conteúdo                     | conexão validada (commit `6007e63`); o projeto passou a usar a chamada HTTP em `c75a496` |
| Fluxo de sucesso       | anotação com duas ou mais tarefas e prazos | lista numerada com `Tarefa` e `Prazo`              | resposta no formato solicitado                                                           |
| Entrada vazia          | Enter sem texto                            | mensagem de erro e encerramento sem chamada ao LLM | mensagem exibida, sem requisição                                                         |

Projeto desenvolvido para o programa de capacitação **Trends IA**.
