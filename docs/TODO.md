# TODO

- [ ] Refatorar arquivo app.py
  - [ ] Renomear arquivo para main.py
  - [ ] Não devem existir definições de variaveis no escopo global do arquivo, NUNCA!
  - [ ] Nunca utilizar o primeiro nível de um arquivo para executar codigo diretamente, passar pela validacao __name__ == __main__
    - [ ] Como vimos, a nivel do arquivo aquilo que nao for definição de função será executado quando o arquivo for executado ou importado.
  - [ ] Refatorar funções para serem mais genericas e reutilizaveis
  - [ ] Pense sobre composição e herança
    - [ ] Oque vc quer criar como classe (precisa de contrutor? atributos internos? deveria ser classe? )
    - [ ] Oque vc quer reutilizar de uma classe ja existente?
  - [ ] Mantenha definição e setup de variáveis dentro do metodo main, os metodos utilizados durante a execução devem preferencialmente receber parametros e ter poucas dependencias. Procure depois sobre programação funcional e side-effects, mas isso também é um tópico longo. Pense que a função tem q ser uma caixinha preta, recebe aquilo que precisa e devolve o que foi prometido.
  - [ ] Se precisar de uma variável, IMUTÁVEL, GLOBAL, utilize uma variavel de ambiente, .env
- [X] Mover sound para Assets
- [X] Fix pip requirements
- [X] Estruturção confusa de pastas e arquivos.
  - [X] Criar pasta para docs.
  - [X] Expandir README com documentação básica de projeto