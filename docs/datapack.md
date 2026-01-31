# Documentação de Data Packs

Os **Data Packs** são a forma principal de conteúdo do Quiz Game.  
Eles definem perguntas, eventos, mensagens e regras usando apenas arquivos **JSON**, permitindo expansão do jogo sem alterar o código-fonte.

---

## 📦 O que é um Data Pack

Um Data Pack é uma pasta que representa um conjunto de perguntas e eventos relacionados a um tema específico (ex.: matemática, história, geografia).

Cada Data Pack contém:
- Configuração geral (`pack.json`)
- Perguntas (`questions/`)
- Eventos (`events/`)
- Tags e metadados (`tags/`)

---

## 📁 Estrutura de um Data Pack

```

data/
└── <namespace>/
    ├── pack.json
    ├── questions/
    │   ├── 1.json
    │   ├── 2.json
    │   └── ...
    ├── events/
    │   ├── success.json
    │   └── failed.json
    └── tags/
        └── questions.json

````

---

## 🧾 pack.json

Arquivo principal do Data Pack.  
Define metadados e configurações gerais.

### Exemplo
```json
{
  "name": "Matemática",
  "description": "Perguntas básicas de matemática",
  "version": "1.0.0",
  "format": 2
}
```

### Campos

| Campo         | Tipo   | Descrição              |
| ------------- | ------ | ---------------------- |
| `name`        | string | Nome exibido do pacote |
| `description` | string | Descrição do conteúdo  |
| `version`     | string | Versão do Data Pack    |
| `format`      | integer | Versão do pacote      |

### Formatos
> #### Formato de intervalos:
> --- 
> `n`: Exatamente `n`  
> `n..`: Maior ou igual a `n`  
> `..n`: Menor ou igual a `n`  
> `n..m`: Entre `n` e `m`  

| Versão | Feature       |
| ------ | ------------- |
| `1`    | Versão Mínima |
| `2..`  | Eventos       |


---

## ❓ Perguntas (`questions/`)

Cada pergunta é definida em um arquivo JSON separado dentro da pasta `questions/`.

### Exemplo de pergunta

```json
{
  "type": "literal",
  "name": "2 + 2?",
  "answer": "4",
  "on": { ... }
}
```

### Campos

| Campo      | Tipo          | Descrição                                |
| ---------- | ------------- | ---------------------------------------- |
| `name` | string        | Enunciado                        |
| `answer`  | string | Resposta(RegEx)                    |
| `retry`  | boolean?        | Se pode tentar novamente |
| `tries`   | number?        | Número de tentativas |
| `on`     | object | Eventos disparados |

### Campos `on`
| Campo | Tipo | Descrição |
| - | - | - |
| `success` | `resource_location<Event>` | Disparado quando acerta a pergunta |
| `failed` | `resource_location<Event>` | Disparado quando erra a pergunta |
---

## 🎉 Eventos (`events/`)

Eventos são arquivos json que são executados no código fonte, mas claro, com recursos limitados.

> Datapack ficticio `test`
### test/events/success.json

```json
{
  "require": ["console"],
  "run": [
    "console.print('Parabéns!')"
  ]
}
```
> O evento será tratado como `resource_location<Event>`, ou `test:success`, sendo `test` namespace(datapack) e `success` o evento

### test/events/failed.json

```json
{
  "require": ["console"],
  "run": [
    "console.print('Boowomp!')"
  ]
}
```
> O evento será tratado como `resource_location<Event>`, ou `test:failed`

> Veja [resource_location](./resource_location.md)

### Campos
| Campo | Tipo | Descrição |
| - | - | - |
| `require` | array[string] | Dependências do código |
| `run` | array[string] | Código python a ser executado(linhas)
---

## 🏷️ Tags (`tags/`)

As tags servem para compilar informações em um só arquivo.

### questions.json

```json
{
  "values": [
    "datapack:1",
    "datapack:2",
    ...
  ]
}
```

### Função das tags

* Compilar informações em uma só lista

### Campos

| Campo | Tipo | Descrição |
| - | - | - |
| `values` | `array[resource_location]` | Valores da tag |

### Tipos de tags
| Nome | Valores | Descrição |
| - | - | - |
| `questions.json` | `resource_location<Question>` | Perguntas em ordem

> Veja [resource_location](./resource_location.md)

---

## 🔗 Schemas
O sistema de datapacks possui um sistema de schemas embutido([~/.schemas/](../.schemas) e [~/.vscode/settings.json](../.vscode/settings.json))

## ➕ Criando um Novo Data Pack

1. Crie uma nova pasta em `data/`
2. Adicione:

   * `pack.json`
   * pasta `questions/`
   * pasta `events/`
   * pasta `tags/`
3. Preencha os arquivos seguindo os formatos documentados
4. Execute o jogo normalmente

---

## ⚠️ Regras Importantes

* Arquivos **devem estar em JSON válido**
* Os nomes dos arquivos de perguntas não importam, desde que sejam `.json`
* Tudo é referido a partir de `resource_location`, que segue no formato `datapack:nome`, que dependendo do contexto pode ser arquivos diferentes
---

## 🎯 Objetivo do Sistema de Data Packs

* Separar **conteúdo** de **lógica**
* Facilitar modificação
* Permitir criação de novos quizzes sem modificar o código fonte
* Tornar o jogo altamente extensível

---