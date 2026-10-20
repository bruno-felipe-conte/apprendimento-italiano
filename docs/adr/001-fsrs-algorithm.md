# ADR 001: Adoção do Algoritmo FSRS-4.5 para Repetição Espaçada

## Contexto
O aprendizado de vocabulário e fixação de termos em italiano requer uma curva de memorização eficiente. Anteriormente, algoritmos clássicos como SM-2 (SuperMemo-2) utilizavam heurísticas fixas de facilidade (*easiness factor*) com intervalos rígidos, resultando em revisões redundantes ou subestimadas para palavras difíceis.

## Decisão
Implementar o motor de repetição espaçada baseado no **FSRS-4.5 (Free Spaced Repetition Scheduler)** em `js/flashcards.js`.
O algoritmo modela o esquecimento humano através de duas variáveis contínuas fundamentais:
- **Estabilidade ($S$)**: O número de dias até que a probabilidade de recordação caia para 90%.
- **Dificuldade ($D$)**: Uma escala de 1 a 10 que quantifica o esforço cognitivo inerente ao item.
- **Recordabilidade ($R$)**: A probabilidade instantânea de lembrar da palavra após $t$ dias:
  $$R(t, S) = \left(1 + \text{factor} \cdot \frac{t}{S}\right)^{-0.5}$$

Permitir 4 graus de avaliação pelo aprendiz:
1. **Again (1)**: Erro / esquecimento completo
2. **Hard (2)**: Recordação com grande esforço
3. **Good (3)**: Recordação correta com esforço esperado
4. **Easy (4)**: Domínio perfeito e imediato

## Consequências
- A retenção de longo prazo atinge taxas superiores a 90% com até 30% menos revisões totais em comparação ao SM-2.
- A migração de cartas legadas com SM-2 é calculada dinamicamente mapeando `interval` e `repetitions` para estabilidade inicial.
