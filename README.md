# SupriDesk - Sistema de Gestão de Solicitações

Este é um sistema desktop desenvolvido em Python para a disciplina de Desenvolvimento Rápido de Aplicações (RAD). O objetivo é gerenciar pedidos internos de materiais, permitindo o cadastro, acompanhamento do fluxo de atendimento, busca e exportação de dados.

## 🛠 Tecnologias Utilizadas

* **Linguagem:** Python 3 (Versão utilizada: 3.14.5)
* **Interface Gráfica:** Tkinter / ttk
* **Banco de Dados:** SQLite3 (Nativo do Python)
* **Manipulação de Arquivos:** Módulo `csv` (Nativo do Python)

*Nota: O projeto utiliza apenas bibliotecas nativas do Python, portanto, não há dependências externas a serem instaladas via `pip`.*

## ⚙️ Como Executar

1. Certifique-se de ter o Python 3 instalado em sua máquina.
2. Clone este repositório ou baixe os arquivos.
3. Abra o terminal na pasta do projeto.
4. Execute o arquivo principal:
```bash
python main.py
```

## 🚀 Funcionalidades

- Cadastro de Solicitações: Validação de campos vazios e quantidade (apenas números inteiros positivos). O ID, a data/hora e o status inicial "Pendente" são gerados automaticamente.

- Fluxo de Atendimento: Transição controlada de status (Pendente → Em atendimento → Atendida). Transições inválidas ou repetidas são bloqueadas pelo sistema.

- Pesquisa e Filtros: Busca por Setor ou Material (ignorando maiúsculas/minúsculas) e filtro por status exato.

- Exportação CSV: Gera o arquivo historico_solicitacoes.csv com todos os dados do banco, formatado com ponto e vírgula para melhor visualização no Excel.

- Organização: O código é dividido em módulos (interface.py, database.py, regras.py e main.py) para separar a interface, o banco e as regras de negócio.

## 🧪 Testes das Funcionalidades

- Teste de Cadastro Válido: Cadastrado "TI / Mouse USB / 5 / Alta". O sistema gerou o ID, data/hora e salvou com status Pendente.

- Teste de Bloqueio de Quantidade Inválida: Tentado cadastrar "Administrativo / Papel A4 / 0 / Normal". O sistema recusou a operação e exibiu um alerta de erro (quantidade deve ser maior que zero).

- Teste de Fluxo de Status e Bloqueio: Selecionado o pedido Pendente e avançado para Em atendimento e depois para Atendida. Ao tentar avançar novamente, o sistema bloqueou a ação com uma mensagem de erro.

- Teste de Persistência de Dados: O sistema foi fechado e reaberto. O registro do Mouse USB permaneceu salvo e visível na tabela, graças à persistência do SQLite.

- Teste de Busca, Uso do Filtro e Salvar Histórico CSV: Pesquisado por "Mouse" e "TI", filtrado por "Atendida" (funcionou corretamente). Em seguida, clicado em "Exportar CSV", gerando o arquivo com o histórico.

- Teste de Exclusão de Registro: Selecione com o mouse o registro salvo no teste do primeiro item. Em seguida, clicando em "Excluir, irá perguntar se tem certeza se deseja finalizar a operação, ao aceitar, irá excluir permanentemente o registro, não podendo existir mais outro com o mesmo ID do qual foi excluído.

## 🤖 Uso de Ferramentas de IA

O desenvolvimento deste projeto contou com o suporte de três ferramentas de Inteligência Artificial (DeepSeek, ChatGPT e Gemini) como assistentes de programação. O uso das IAs concentrou-se no processo de ideação da interface gráfica (como a disposição dos botões, organização da tabela e criação do pop-up de cadastro) e no refinamento do design com Tkinter/ttk. Além disso, as ferramentas auxiliaram na revisão e correção de sintaxe durante a codificação do projeto.