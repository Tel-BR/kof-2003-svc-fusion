---
title: "Complete a native team match"
triage: ready-for-agent
---

# 02 Complete a native team match

[Parent specification](../spec.md)

## What to build

Replay a complete MVS team match with original KOF 2003 fighters on the modifiable native port.

## Blocked by

[01 Reproduce native KOF 2003 in MVS](01-reproduce-native-mvs.md)

## Acceptance criteria

- [ ] Replay fixed inputs from a known state through team selection and the normal match result. Record evidence of native execution, fallback and verification divergences.
- [ ] Compare the match flow and Leader Super eligibility and meter cost with a working MVS reference.

## Português (Brasil)

Repetir uma luta completa de equipes no MVS com lutadores originais do KOF 2003 no port nativo modificável.

### Bloqueios

[01 Reproduce native KOF 2003 in MVS](01-reproduce-native-mvs.md)

### Critérios de aceitação

- [ ] Repetir entradas fixas a partir de um estado conhecido, da seleção das equipes ao resultado normal da luta. Registrar execução nativa, fallback e eventuais divergências de verificação.
- [ ] Comparar o fluxo da luta, as condições de uso e o custo de barra do Leader Super com uma referência MVS funcional.

## Comments

### 2026-11-13 — Change of first test

The owner chose MVS team play for the first import test. AES Single remains a reference observation and is not a prerequisite for the first imported match.

_PT-BR: o dono escolheu o modo de equipes do MVS para o primeiro teste da importação. O Single do AES permanece como observação de referência e deixa de ser pré-requisito da primeira luta com o importado._

### 2026-11-13 — Owner's manual AES reference

The owner tested the `kof2003` cartridge in MAME 0.289 with Universe BIOS 4.0 in U.S.A. console mode. After the BIOS screen and intro, pressing Start opens MODE SELECT. Its options are TEAM PLAY, TEAM VERSUS, TEAM PRACTICE, SINGLE PLAY, SINGLE VERSUS, SINGLE PRACTICE and OPTION. The cursor starts on TEAM PLAY. Press down three times and A to select SINGLE PLAY. A tutorial follows and can be skipped by pressing A twice. LEADER SELECT then opens with Iori initially selected and unlimited selection time. Selecting Iori starts the first fight.

The owner reports one fighter per side and a single round. The fight starts with three available power stocks, all blue for the Leader. Iori's Leader Super Special Move, San Shingi no Ni, was available and consumed two stocks. The reported command is `↓↘→ ↙↓← + AC`. The owner reports that certain special moves can cancel a super, including the Leader Super, at a cost of one stock.

The owner reports that Kin 1211 Shiki: Ya Otome, `↓↘→ ↘↓↙← + A/C`, is Iori's only common super shared with SVC Chaos in KOF 2003. The follow-up Ura 306 Shiki: Saika is available in KOF 2003 using the same command as in SVC and costs one additional stock, according to the owner's correction. These move comparisons remain to be checked against the SVC reference.

The opponent is random. The owner observed Maxima and Whip in different runs. After winning the single round, the owner saw Iori's victory animation, his artwork and quote, then an automatically advancing order-select screen followed by the next fight. At character select, buttons A, B, C and D select four different colors.

The owner reports canceling normals and chain combos into supers without an additional stock cost, and canceling special moves such as Iori's shoryuken into a super or Leader Super for one additional stock. An exact sequence and the conditions of the cancel remain to be established. The native AES replay and comparison remain open.

### 13/11/2026 — Referência AES testada pelo dono

O dono testou o cartucho `kof2003` no MAME 0.289 com Universe BIOS 4.0 em modo console, região U.S.A. Após a tela da BIOS e a introdução, apertar Start abre MODE SELECT. As opções são TEAM PLAY, TEAM VERSUS, TEAM PRACTICE, SINGLE PLAY, SINGLE VERSUS, SINGLE PRACTICE e OPTION. O cursor começa em TEAM PLAY. Apertar baixo três vezes e A seleciona SINGLE PLAY. Em seguida aparece um tutorial, que pode ser pulado apertando A duas vezes. A tela LEADER SELECT abre com o cursor em Iori e tempo infinito para escolher. Selecionar Iori inicia a primeira luta.

O dono relata um lutador por lado e um único round. A luta começa com três barras de especial disponíveis, todas azuis para o Leader. O Leader Super Special Move de Iori, San Shingi no Ni, estava disponível e consumiu duas barras. O comando informado é `↓↘→ ↙↓← + AC`. O dono relata que certos movimentos especiais podem cancelar um super, inclusive o Leader Super, ao custo de uma barra.

O dono relata que Kin 1211 Shiki: Ya Otome, `↓↘→ ↘↓↙← + A/C`, é o único super comum de Iori compartilhado com SVC Chaos no KOF 2003. Em correção ao relato anterior, informa que a extensão Ura 306 Shiki: Saika também está disponível no KOF 2003 com o mesmo comando do SVC e consome uma barra adicional. A comparação de golpes ainda será conferida na referência do SVC.

O primeiro adversário é aleatório. O dono encontrou Maxima e Whip em partidas diferentes. Ao vencer o round único, viu a comemoração do Iori, seu artwork e frase, a tela de order select avançar automaticamente e a luta seguinte começar. Na seleção, os botões A, B, C e D escolhem quatro cores diferentes.

O dono relata cancelamentos de golpes normais e chain combos em supers sem custo adicional de barra, e de movimentos especiais, como o shoryuken do Iori, em super ou Leader Super por uma barra adicional. Ainda falta estabelecer uma sequência exata e as condições do cancelamento. A repetição e a comparação no port nativo em AES continuam pendentes.
