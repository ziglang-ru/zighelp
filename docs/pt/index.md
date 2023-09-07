---
title: "Chapter 0 - Começando"
weight: 1
date: 2023-08-28 17:24:00
description: "Zighelp - Um Guia / Tutorial para a linguagem de programação Zig. Instale e comece com Zig aqui."
---

## Bem-vindo(a)

[Zig](https://ziglang.org) é uma linguagem de programção de uso geral e um toolchain para manter software __robusto__, __ótimizado__, and __reutilizável__.


Aviso: O última versão principal é 0.11 - O Zig ainda é pré-1.0; o uso em produção ainda não é recomendado e poderá encontrar bugs no compilador.

Para seguir este guia, nós assumimos que tem:

- Experiência prévia com programção
- Alguma compreensão sobre conceitos de programção de baixo nível

Saber uma linguagem como C, C++, Rust, Go, Pascal ou similar vai lhe ajudar a seguir este guia. Tem de ter um editor, terminal e conexão à internet. Este guia não é oficial e nem afiliado à fundação Zig Software Foundation e foi feito para ser lido por ordem e desde o ínicio.

## Instalação

**Este guia assume que está utilizando a versão master** do Zig em vez da última versão principal, o que significa que descarregar o binário do site ou compilar a partir da fonte; **a versão do Zig no seu gerenciador de pacotes (package manager) está provavelmente desatualizado**. Este guia não suporta o Zig 0.10.1.

1. Descarregue e extraia o binário do pré-compilado do master do Zig apartir do https://ziglang.org/download/.

2. Adicione o Zig ao seu path
   - linux, macos, bsd

      Adicione a localização do seu binário do Zig à sua variável de environment `PATH`. Para instalar, adicione `export PATH=$PATH:~/zig` ou similar ao seu `/etc/profile` (para todo o sistema) ou `$HOME/.profile`. Se estas mudanças não forem aplicadas imediatamente, execute a linha no seu shell. 
   - windows

      a) Para todo o sistema (admin powershell)

      ```powershell
      [Environment]::SetEnvironmentVariable(
         "Path",
         [Environment]::GetEnvironmentVariable("Path", "Machine") + ";C:\your-path\zig-windows-x86_64-your-version",
         "Machine"
      )
      ```

      b) Para o utilizador (powershell)

      ```powershell
      [Environment]::SetEnvironmentVariable(
         "Path",
         [Environment]::GetEnvironmentVariable("Path", "User") + ";C:\your-path\zig-windows-x86_64-your-version",
         "User"
      )
      ```

      Feche o seu terminal e abra um novo.

3. Verifique a sua instalação `zig version`. O output deve ser algo parecido a isto:
```
$ zig version
0.11.0-dev.2777+b95cdf0ae
```

4. (opcional, feito por terceiros) Para auto-completamento e para "ir para definições" no seu editor, instale o Zig Language Server apartir de https://github.com/zigtools/zls/.

5. (opcional) Entre numa [comunidade do Zig](https://github.com/ziglang/zig/wiki/Community).

## Olá, mundo

Crie um ficheiro chamado `main.zig`, com o seguinte conteúdo:

```zig
const std = @import("std");

pub fn main() void {
    std.debug.print("Hello, {s}!\n", .{"World"});
}
```

!!! note "nota: certifique que o ficheiro está codificado com UTF-8!"
!!! note "nota: Se estiver a utilizar tabs para indentação e/ou CRLF para o fim das linhas no seu ficheiro, o compilador vai aceitá-lo mas usar `zig fmt` vai canonizá-los para espaços e fim de linhas com LF!"

Use `zig run main.zig` para compilar e executar o programa. Neste exemplo `Hello, World!` será escrito para stderr e é assumido que nunca vai falhar.

