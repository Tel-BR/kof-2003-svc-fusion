# KOF 2003 SVC Fusion

_[Português abaixo](#português-brasil)_

An experimental native PC project bringing fighters from **SNK vs. Capcom: SVC Chaos** into **The King of Fighters 2003**, with the long-term goal of making both rosters available in local Versus play.

The first milestone uses KOF 2003 as the base game and aims to import one SVC-exclusive fighter under KOF 2003 rules. The first match will use the original MVS team format. The fighter has not yet been selected.

## Current status

- A modifiable Windows build of an existing KOF 2003 port was prepared locally. A 6,000-frame MVS control reported zero state divergences and zero interpreter fallback.
- No SVC fighter has been imported yet. The next baseline is a complete, reproducible team match with original KOF 2003 fighters.
- The project is in research and prototyping. There is no release ready for players.

Read the [first import specification](docs/specs/first-svc-character-import/spec.md), [implementation tickets](docs/specs/first-svc-character-import/issues/), and [long-term Versus map](docs/wayfinder/versus-fusion/map.md). The [Windows build guide](docs/specs/first-svc-character-import/native-mvs-windows.md) documents the local reference build.

## Projects used

The current native KOF 2003 baseline uses **The King of Fighters 2003 static recompilation by omegakatana92**. We tested its Windows v0.1.0 release and built a modifiable player locally from its published source, using our own cartridge and BIOS inputs. The port's original project code is licensed under PolyForm Noncommercial 1.0.0. [KOF 2003 project](https://github.com/omegakatana92/The-King-of-Fighters-2003) · [v0.1.0 release](https://github.com/omegakatana92/The-King-of-Fighters-2003/releases/tag/v0.1.0)

The port is built on **neogeorecomp by sp00nznet**. For the local build we use an adapted copy of the toolkit published in omegakatana92's Samurai Shodown project and the build configuration in this repository. [neogeorecomp](https://github.com/sp00nznet/neogeorecomp) · [Adapted toolkit](https://github.com/omegakatana92/Samurai-Shodown-Recomp/tree/c745e97211a81eefdfb436a1cabd8570d3eae90d/neogeorecomp) · [Build guide](docs/specs/first-svc-character-import/native-mvs-windows.md)

## Contributing

Contributions to research, testing, native recompilation, Neo Geo hardware knowledge, graphics and animation formats, and game mechanics are welcome. The project uses local Markdown tickets while the first playable milestone is being developed. Describe your findings without posting game data.

## Game files and third-party code

Supply your own cartridge and BIOS dumps. ROMs, BIOS files, generated game code, extracted assets, captures and traces containing game data stay in the git-ignored `private/` directory. Do not upload them to the repository, issues, or pull requests.

The existing KOF 2003 port and its adapted toolkit are separate third-party projects. Their source and licenses remain with those projects and are kept outside this repository's tracked files.

## License and affiliation

The license for this project has not been decided. Third-party code must not be copied into this repository until it is decided.

Using or distributing the KOF 2003 port and modifications of it remains subject to that port's PolyForm Noncommercial terms, including its noncommercial-use and notice requirements. The license for this repository's own contributions remains to be chosen. Check the licenses and notices for each separately obtained dependency. [PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0) · [Port license status](https://github.com/omegakatana92/The-King-of-Fighters-2003/blob/v0.1.0/LICENSE-STATUS.md)

This independent fan project is not affiliated with or endorsed by SNK or Capcom. All trademarks belong to their respective owners.

---

# Português (Brasil)

Um projeto experimental de port nativo para PC que traz lutadores de **SNK vs. Capcom: SVC Chaos** para **The King of Fighters 2003**. O objetivo de longo prazo é disponibilizar os dois elencos em partidas Versus locais.

O primeiro marco usa KOF 2003 como jogo base e busca importar um personagem exclusivo do SVC sob as regras do KOF 2003. A primeira luta usará o formato original de equipes do MVS. O personagem ainda será escolhido.

## Situação atual

- Um build Windows modificável de um port existente de KOF 2003 foi preparado localmente. Um controle MVS de 6.000 quadros registrou zero divergências de estado e zero retornos ao interpretador.
- Nenhum personagem do SVC foi importado ainda. A próxima referência é uma luta completa e reproduzível de equipes com lutadores originais do KOF 2003.
- O projeto está em pesquisa e prototipação. Ainda não há uma versão disponível para jogadores.

Consulte a [especificação da primeira importação](docs/specs/first-svc-character-import/spec.md), os [tickets de implementação](docs/specs/first-svc-character-import/issues/) e o [mapa do Versus](docs/wayfinder/versus-fusion/map.md). O [guia de build Windows](docs/specs/first-svc-character-import/native-mvs-windows.md) documenta a preparação local.

## Projetos utilizados

A base nativa atual de KOF 2003 usa o projeto **The King of Fighters 2003 static recompilation, de omegakatana92**. Testamos a versão Windows v0.1.0 e compilamos localmente um executável modificável a partir do código publicado, usando nossos próprios arquivos de cartucho e BIOS. O código original do projeto do port usa a licença PolyForm Noncommercial 1.0.0. [Projeto KOF 2003](https://github.com/omegakatana92/The-King-of-Fighters-2003) · [Versão v0.1.0](https://github.com/omegakatana92/The-King-of-Fighters-2003/releases/tag/v0.1.0)

O port é baseado no **neogeorecomp, de sp00nznet**. Para o build local, usamos uma cópia adaptada do toolkit publicada no projeto Samurai Shodown de omegakatana92 e a configuração de build deste repositório. [neogeorecomp](https://github.com/sp00nznet/neogeorecomp) · [Toolkit adaptado](https://github.com/omegakatana92/Samurai-Shodown-Recomp/tree/c745e97211a81eefdfb436a1cabd8570d3eae90d/neogeorecomp) · [Guia de build](docs/specs/first-svc-character-import/native-mvs-windows.md)

## Como contribuir

São bem-vindas contribuições em pesquisa, testes, recompilação nativa, hardware Neo Geo, formatos de gráficos e animação e mecânicas de luta. O projeto usa tickets locais em Markdown durante o desenvolvimento do primeiro marco jogável. Descreva suas descobertas sem publicar dados dos jogos.

## Arquivos dos jogos e código de terceiros

Cada participante fornece seus próprios dumps dos cartuchos e da BIOS. ROMs, BIOS, código gerado dos jogos, recursos extraídos, capturas e traces com dados dos jogos ficam na pasta `private/`, ignorada pelo Git. Não envie esses arquivos para o repositório, issues ou pull requests.

O port existente de KOF 2003 e seu toolkit adaptado são projetos de terceiros separados. Seus códigos e licenças permanecem nesses projetos e ficam fora dos arquivos versionados aqui.

## Licença e vínculo

A licença deste projeto ainda não foi decidida. Até essa decisão, código de terceiros não deve ser copiado para este repositório.

O uso e a distribuição do port de KOF 2003 e de modificações dele continuam sujeitos aos termos PolyForm Noncommercial do próprio port, incluindo as condições de uso não comercial e de avisos. A licença das contribuições próprias deste repositório ainda será escolhida. Confira as licenças e os avisos de cada dependência obtida separadamente. [PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0) · [Licença do port](https://github.com/omegakatana92/The-King-of-Fighters-2003/blob/v0.1.0/LICENSE-STATUS.md)

Este é um projeto independente de fãs, sem vínculo ou endosso da SNK ou da Capcom. As marcas pertencem aos respectivos proprietários.
