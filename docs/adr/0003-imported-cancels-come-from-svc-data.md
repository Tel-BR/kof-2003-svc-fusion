# Imported fighters keep the cancels found in their SVC data

An imported fighter can cancel exactly the moves that its SVC data allows to be canceled. The import carries those cancels over and creates no new ones, even where KOF 2003 would allow a cancel that SVC does not have. For example, KOF 2003 lets special moves be canceled into supers, but the owner could not cancel Guile's special moves into a super in SVC, even in MAX mode. Guile can cancel certain normal attacks. The owner expects the nature of Guile's moves to explain the difference and does not want new cancels created for him. [Ticket 03](../specs/first-svc-character-import/issues/03-capture-svc-fighter-reference.md)

If the SVC data does show a cancel that was not found by playing, the import keeps it. The gauge cost of the carried-over cancels is still open and will be decided by the owner when the moveset is validated in ticket 05.

## Personagens importados mantêm os cancelamentos dos dados do SVC

Um personagem importado pode cancelar exatamente os golpes que os dados dele no SVC permitem cancelar. A importação leva esses cancelamentos e não cria nenhum novo, mesmo quando o KOF 2003 permitiria um cancelamento que o SVC não tem. Por exemplo, o KOF 2003 permite cancelar movimentos especiais em supers, mas o dono não conseguiu cancelar os especiais de Guile em super no SVC, nem no modo MAX. Guile cancela certos golpes normais. O dono acredita que a natureza dos golpes de Guile explica a diferença e não quer que cancelamentos novos sejam criados para ele. [Ticket 03](../specs/first-svc-character-import/issues/03-capture-svc-fighter-reference.md)

Se os dados do SVC mostrarem um cancelamento que não foi encontrado jogando, a importação o mantém. O custo de barra dos cancelamentos mantidos ainda está em aberto e será decidido pelo dono na validação dos golpes, no ticket 05.
