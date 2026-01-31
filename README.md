# Quiz Game (Python)

Projeto de **jogo de perguntas e respostas (quiz)** desenvolvido em Python, com estrutura modular e dados externos em JSON.  
O sistema foi projetado para ser **extensível**, permitindo adicionar novas matérias, perguntas, eventos e regras sem alterar o código principal.

---

## 📁 Estrutura do Projeto

```

quiz-game/
│
├── main.py                 # Ponto de entrada do programa
├── run.bat                 # Script para execução no Windows
├── LICENSE
├── .gitignore
│
├── src/
│   ├── program.py          # Núcleo do jogo
│   ├── pack.py             # Carregamento e gerenciamento de pacotes
│   ├── common.py           # Utilitários comuns
│   ├── imports.py          # Controle de dependências internas
│   └── modules/
│       ├── health.py       # Sistema de vida/saúde
│       └── points.py       # Sistema de pontuação
│
└── data/
    └── math/
        ├── pack.json       # Configuração do pacote de matemática
        ├── questions/      # Perguntas do quiz
        │   ├── 1.json
        │   ├── 2.json
        │   └── ...
        ├── events/         # Eventos de sucesso e falha
        │   ├── success.json
        │   └── failed.json
        └── tags/
            └── questions.json

````

---

## ▶️ Como Executar

### Requisitos
- Python **3.11+**
- `pip install -r requirements.txt`(Possui [PySimpleEvents](https://github.com/oDaniel728/simple-events) e rich)

### Execução direta
```bash
python main.py
```

### No Windows

```bat
run.bat
```

---

## 🧠 Como Funciona

* O jogo carrega **pacotes de perguntas** a partir de arquivos JSON.
* Cada pacote define:

  * Perguntas
  * Eventos de sucesso e falha
  * Tags e metadados
> Veja [DataPack](docs/datapack.md)
---

## ➕ Adicionando Novas Perguntas

1. Crie um novo arquivo `.json` em:

   ```
   data/<pacote>/questions/
   ```
2. Siga o mesmo formato das perguntas existentes.
3. Atualize o `pack.json` se necessário.

---

## 🧩 Modularidade

O jogo utiliza módulos independentes para facilitar manutenção e expansão:

* `health.py` → controle de vida
* `points.py` → controle de pontuação

---

## 📌 Objetivo do Projeto

* Estudar arquitetura modular em Python
* Separar lógica de código e dados
* Criar um jogo facilmente extensível via JSON

---

## 📄 Licença

Este projeto está sob a licença especificada no arquivo `LICENSE`.
