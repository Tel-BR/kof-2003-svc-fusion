---
id: 31
title: "Choose which of Guile's remaining voices fill the 12,544-byte tail"
label: wayfinder:grilling
mode: HITL
status: closed
assignee: tel
blocked_by: [30]
research:
---

## Question

[30](30-guile-svc-remaining-sounds.md) sized what is left after the two attack voices of [27](27-guile-sounds-route.md): 31 candidate samples, 193,792 bytes, 15.4 times the 12,544 free bytes of the V tail, so the owner has to pick. Which of Guile's remaining voices (hurt tiers, launch hurt, taunt, third attack tier, throw, knockout, and the specials and supers voices) enter the tail, if any? How are the voices that do not fit handled (silent, or the KOF 2003 sound of the equivalent action, per rule 6 of 27)? And does the choice follow the same shape for every SVC fighter, as an import rule?

Standing fact, outside the repository (owner, 2026-11-19): no voice role has been confirmed in a MAME run. Every role named in 30 (hurt, launch hurt, taunt, third attack tier, throw, knockout, specials, supers) is inferred from static reading. The grilling decides what to do with that: choose now on inferred roles, with a confirmation step recorded; or hold the choice until a MAME run confirms them, and which roles the run must confirm first.

_PT-BR: o [30](30-guile-svc-remaining-sounds.md) dimensionou o que sobra depois das duas vozes de ataque do [27](27-guile-sounds-route.md): 31 amostras candidatas, 193.792 bytes, 15,4 vezes os 12.544 bytes livres da faixa de V, então o dono precisa escolher. Quais das vozes restantes do Guile (níveis de dor, dor de lançamento, provocação, terceiro nível de ataque, arremesso, nocaute e as vozes de especiais e supers) entram na faixa, se alguma? Como tratar as que não couberem (mudas, ou o som do KOF 2003 da ação equivalente, pela parte 6 do 27)? E a escolha vale com o mesmo formato para todo lutador do SVC, como regra de importação?_

_Fato fora do repositório (dono, 19/11/2026): nenhum papel de voz foi confirmado numa execução do MAME. Todos os papéis do 30 são inferidos por leitura estática. A entrevista decide o que fazer com isso: escolher já sobre papéis inferidos, com uma etapa de confirmação registrada; ou segurar a escolha até o MAME confirmar, e quais papéis a execução precisa confirmar primeiro._

## Notes

- Inputs: the group costs and the three pairs that fit are in the Resolution of [30](30-guile-svc-remaining-sounds.md); the rule and the first-come, first-served ledger are in [27](27-guile-sounds-route.md). The 12,544 bytes are contiguous only if the two attack voices sit at one end of the tail.
- Special moves, supers and cancels stay out of scope for this map; only the choice of which voices to import is decided here.
- Hard rule of `AGENTS.md`: only addresses, sizes, counts and hashes in the notes.

## Resolution

Owner decisions of 2026-11-19, valid for every SVC fighter. The rule has five parts.

1. **Attack voices first.** Every Imported Character gets its attack voices from the free V tail before anyone's extras. The remaining voices of [30](30-guile-svc-remaining-sounds.md) (hurt tiers, launch hurt, taunt, third attack tier, throw, knockout, specials, supers) are extras and enter only if space is left. With four imported fighters and 3,840 bytes of attack voices each (measured for Guile only), 12,544 - 3 x 3,840 leaves 1,024 bytes, below the smallest extra group (throw, 2,560), so no extra of Guile enters today. The goal stays to bring all of his voices later, through a larger sound space ([32](32-all-exclusive-voices-total.md)).
2. **No own voice meanwhile.** In the situations of the voices that did not enter, Guile plays only the shared effect that KOF 2003 already uses (rule 2 of [27](27-guile-sounds-route.md)); the voice stays silent, as the break-fall already is. No other fighter's voice is borrowed.
3. **Register and hooks.** Each voice left out gets an entry in a per-fighter register (role, size, SVC source range, the script point where it would play, and a status of inferred or confirmed) and costs no byte of the tail. The sound word at that script point already points to the KOF 2003 shared effect when one exists, so when space opens the swap is a data change only. The eight voices with no static trigger are listed as "no trigger" and get no hook. The register and hooks are an implementation ticket of the spec, not of this map.
4. **Order of extras.** No written order: when a tail remainder exists after the attack voices, it returns to the owner with the options and their costs.
5. **Roles need MAME.** The roles in 30 stay inferred until a MAME run on the owner's machine confirms them ([33](33-confirm-voice-roles-in-mame.md)). That task blocks only the mapping of the hooks, not this decision and not the attack voices.

Consequences: the Guile slice keeps the two attack voices of 27 and nothing else from 30; the fullest-fill sums of 30 are not used. New tickets: [32](32-all-exclusive-voices-total.md) measures the total voice need of all Exclusive Characters and the routes to a larger sound space; [33](33-confirm-voice-roles-in-mame.md) confirms the roles.

_PT-BR: decisões do dono em 19/11/2026, valendo para todo lutador do SVC. A regra tem cinco partes._

1. _**Vozes de ataque primeiro.** Todo Personagem Importado recebe as vozes de ataque da faixa livre de V antes dos extras de qualquer um. As demais vozes do [30](30-guile-svc-remaining-sounds.md) (níveis de dor, dor de lançamento, provocação, terceiro nível de ataque, arremesso, nocaute, especiais, supers) são extras e só entram se sobrar espaço. Com quatro lutadores importados e 3.840 bytes de vozes de ataque cada (medido só para o Guile), 12.544 - 3 x 3.840 deixa 1.024 bytes, abaixo do menor grupo extra (arremesso, 2.560), então nenhum extra do Guile entra hoje. O objetivo segue sendo trazer todas as vozes dele depois, por um espaço de som maior ([32](32-all-exclusive-voices-total.md))._
2. _**Sem voz própria enquanto isso.** Nas situações das vozes que não entraram, o Guile toca só o efeito compartilhado que o KOF 2003 já usa (regra 2 do [27](27-guile-sounds-route.md)); a voz fica muda, como a recuperação de queda já fica. Não se empresta voz de outro lutador._
3. _**Registro e ganchos.** Cada voz deixada de fora ganha uma entrada num registro por lutador (papel, tamanho, faixa de origem no SVC, ponto do script onde tocaria e estado: inferida ou confirmada) e não gasta byte da faixa. A palavra de som nesse ponto do script já aponta para o efeito compartilhado do KOF 2003 quando existe um, então, quando o espaço abrir, a troca é só de dado. As oito vozes sem gatilho estático entram como "sem gatilho" e não ganham gancho. O registro e os ganchos são ticket de implementação do spec, não deste mapa._
4. _**Ordem dos extras.** Sem ordem escrita: quando houver sobra na faixa depois das vozes de ataque, ela volta ao dono com as opções e seus custos._
5. _**Papéis pedem o MAME.** Os papéis do 30 seguem inferidos até uma execução do MAME na máquina do dono confirmá-los ([33](33-confirm-voice-roles-in-mame.md)). Essa tarefa bloqueia só o mapeamento dos ganchos, não esta decisão nem as vozes de ataque._

_Consequências: a fatia do Guile fica com as duas vozes de ataque do 27 e nada mais do 30; as somas de preenchimento máximo do 30 não são usadas. Tickets novos: o [32](32-all-exclusive-voices-total.md) mede a necessidade total de vozes de todos os exclusivos e as rotas para um espaço de som maior; o [33](33-confirm-voice-roles-in-mame.md) confirma os papéis._
