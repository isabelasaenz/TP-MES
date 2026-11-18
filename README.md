# Revisão Automática de Pull Requests com IA

Sistema de revisão automática de código integrado ao GitHub Actions, utilizando modelos de linguagem locais para analisar Pull Requests e identificar possíveis problemas de qualidade, manutenção e segurança.

O projeto utiliza o [nitpik](https://github.com/nsrosenqvist/nitpik) como ferramenta de análise estática e orquestração dos agentes de revisão, e o [Ollama](https://ollama.com/) para executar o modelo de IA localmente no runner do GitHub Actions.

## Objetivo

Automatizar parte do processo de Code Review, oferecendo feedback sobre alterações propostas em Pull Requests sem depender de serviços comerciais de revisão de código ou de APIs externas de inteligência artificial.

A solução foi desenvolvida considerando os seguintes requisitos:

- Utilização de ferramentas gratuitas e open source.
- Ausência de API keys de provedores externos de IA.
- Execução automatizada a cada atualização de Pull Request.
- Análise de código com foco em qualidade e segurança.
- Disponibilização dos resultados diretamente no GitHub.

## Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| GitHub Actions | Automação da execução da revisão |
| nitpik 2.2.0 | Orquestração dos agentes e análise de código |
| Ollama | Execução local do modelo de linguagem |
| Qwen 2.5 Coder 1.5B | Modelo utilizado na revisão |
| Python | Linguagem utilizada no projeto |

## Arquitetura

O processo é executado automaticamente quando um Pull Request é aberto, atualizado ou reaberto.

```text
Desenvolvedor
     |
     v
Pull Request no GitHub
     |
     v
GitHub Actions
     |
     v
Instalação e inicialização do Ollama
     |
     v
Download do modelo Qwen 2.5 Coder
     |
     v
Execução do nitpik
     |
     +----------------------+
     |                      |
     v                      v
Agente Backend        Agente Security
     |                      |
     +----------+-----------+
                |
                v
       Scanner de segredos
                |
                v
       Consolidação dos resultados
                |
                v
       Anotações no GitHub
                |
                v
       Relatório JSON (artifact)
```

Os agentes Backend e Security analisam as alterações do Pull Request de acordo com seus respectivos perfis. Paralelamente, o scanner de segredos identifica possíveis credenciais expostas no código.

## Como funciona

### 1. Disparo automático

O workflow é iniciado nos seguintes eventos:

- `opened`: quando um Pull Request é aberto.
- `synchronize`: quando novos commits são enviados.
- `reopened`: quando um Pull Request é reaberto.

### 2. Inicialização do ambiente

O GitHub Actions utiliza um runner Ubuntu para instalar e iniciar o Ollama.

Em seguida, o modelo `qwen2.5-coder:1.5b` é baixado e disponibilizado para execução local.

Não é necessário configurar uma API key de um provedor externo de inteligência artificial.

### 3. Revisão do código

O nitpik executa a revisão utilizando dois perfis:

- **Backend:** análise de problemas relacionados à implementação e à qualidade do código.
- **Security:** identificação de possíveis vulnerabilidades e problemas de segurança.

O scanner de segredos também é executado para detectar credenciais potencialmente expostas.

### 4. Apresentação dos resultados

Os resultados são disponibilizados de duas formas:

- **GitHub Actions annotations:** apontamentos associados às linhas do código, quando suportados pela saída do workflow.
- **Relatório JSON:** arquivo `nitpik-audit.json`, armazenado como artifact da execução para consulta posterior.

## Configuração

O workflow está localizado em:

```text
.github/
└── workflows/
    └── ai_review.yml
```

### Modelo de IA

A configuração atual utiliza:

| Parâmetro | Valor |
|---|---|
| Provider | Ollama |
| Modelo | `qwen2.5-coder:1.5b` |
| Versão do nitpik | `2.2.0` |
| Perfis | `backend`, `security` |
| Concorrência | 1 |
| Scanner de segredos | Habilitado |

### Comando de revisão

O comando utilizado pelo workflow é:

```bash
nitpik review \
  --diff-base "origin/${GITHUB_BASE_REF}" \
  --profile backend,security \
  --scan-secrets \
  --format github \
  --max-concurrent 1 \
  --no-fail \
  --audit-log nitpik-audit.json
```

Principais parâmetros:

| Parâmetro | Descrição |
|---|---|
| `--diff-base` | Define a branch utilizada como referência para comparação. |
| `--profile` | Seleciona os perfis de análise. |
| `--scan-secrets` | Habilita a identificação de possíveis segredos. |
| `--format github` | Gera anotações compatíveis com o GitHub Actions. |
| `--max-concurrent 1` | Limita a execução a uma tarefa simultânea. |
| `--no-fail` | Evita falhas de execução causadas pela severidade dos findings. |
| `--audit-log` | Salva os resultados em um arquivo JSON. |

## Resultados esperados

A ferramenta pode identificar problemas como:

- Credenciais e chaves de API expostas no código.
- Ausência de tratamento de exceções.
- Possíveis erros de execução.
- Problemas de segurança.
- Práticas de implementação que podem comprometer a manutenção do software.

Cada finding pode conter:

- Arquivo e linha onde o problema foi identificado.
- Severidade.
- Título e descrição do problema.
- Sugestão de correção.
- Agente responsável pela identificação.

## Exemplo de execução

Em um teste com problemas intencionais inseridos no código, o scanner identificou uma possível chave de API hardcoded.

Resultado registrado no relatório:

```text
Severity: warning
Title: Potential secret detected: generic-api-key
File: main.py
Line: 38

Message:
Detected a Generic API Key, potentially exposing
access to various services and sensitive operations.

Suggestion:
Remove the hardcoded secret and use environment
variables or a secrets manager instead.
```

## Segurança

O projeto não utiliza credenciais de provedores externos de IA.

O scanner de segredos pode identificar credenciais potencialmente expostas e redigi-las antes do envio do contexto ao modelo.

O relatório gerado deve ser tratado como um artefato de auditoria, pois pode conter trechos de código e informações sobre problemas encontrados no repositório.

Para utilização em projetos reais, recomenda-se revisar as permissões do `GITHUB_TOKEN`, especialmente em Pull Requests originados de forks, e evitar conceder permissões de escrita desnecessárias.

## Como executar

1. Faça o fork ou clone deste repositório.
2. Mantenha o workflow em `.github/workflows/ai_review.yml`.
3. Habilite o GitHub Actions no repositório.
4. Abra um Pull Request.
5. Aguarde a execução do workflow.
6. Consulte as anotações na execução e baixe o artifact `nitpik-audit-report` para visualizar o relatório completo.

