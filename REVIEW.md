# Diretrizes de Revisão

## Estilo e Boas Práticas
- Preferir funções puras e imutabilidade.
- Nunca usar argumentos default mutáveis (ex.: `lista=[]`).
- Evitar `except:` genérico; capturar exceções específicas e fazer log do erro.

## Segurança
- Nenhuma credencial hardcoded; usar variáveis de ambiente ou secrets manager.
- Validar todas as entradas externas antes de as usar em consultas ou comandos.

## Correção (coberto pelo perfil backend)
- Verificar sempre a divisão por zero antes de calcular `a / b`.
- Garantir que listas não estão vazias antes de calcular médias ou somas.
- Em operações assíncronas ou concorrentes, rever condições de corrida.

## Performance (coberto pelo perfil backend)
- Evitar consultas N+1 em loops; pré-carregar dados necessários.
- Preferir estruturas de dados adequadas (ex.: `set` para pesquisas de pertença).

## Arquitetura (coberto pelo perfil architect)
- Evitar acoplamento excessivo entre módulos.
- Manter fronteiras claras entre camadas.