# TODO

- [ ] Refatorar funções para serem mais genericas e reutilizaveis
- [ ] Pense sobre composição e herança
  - [ ] Oque vc quer criar como classe (precisa de contrutor? atributos internos? deveria ser classe? )

- [ ] Estudar singleton
- [ ] Estudar paralelismo x concorrência
- [ ] Estudar qual a necessidade de __name__ == '__main__'
- [ ] Para o meu GitHub, deixar todos os comentários em EN



# DONE

- [ ] Mantenha definição e setup de variáveis dentro do metodo main, os metodos utilizados durante a execução devem preferencialmente receber parametros e ter poucas dependencias. Procure depois sobre programação funcional e side-effects, mas isso também é um tópico longo. Pense que a função tem q ser uma caixinha preta, recebe aquilo que precisa e devolve o que foi prometido.

- [x] Refatorar arquivo app.py
  - [X] Como vimos, a nivel do arquivo aquilo que nao for definição de função será executado quando o arquivo for executado ou importado.
  - [X] Renomear arquivo para main.py
  - [X] Não devem existir definições de variaveis no escopo global do arquivo, NUNCA!
  - [X] Nunca utilizar o primeiro nível de um arquivo para executar codigo diretamente, passar pela validacao __name__ == __main__
  - [X] Para os estudantes, deixar todos os comentários em PT-BR
  - [X] Oque vc quer reutilizar de uma classe ja existente?
  - [X] Se precisar de uma variável, IMUTÁVEL, GLOBAL, utilize uma variavel de ambiente, .env
- [X] Mover sound para Assets
- [X] Fix pip requirements
- [X] Estruturção confusa de pastas e arquivos.
  - [X] Criar pasta para docs.
  - [X] Expandir README com documentação básica de projeto