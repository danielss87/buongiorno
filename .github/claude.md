## Sobre as Github actions.

Atualmente, o projeto conta com uma github action que pega o preço do ouro diariamente no Yahoo finance. Note que o projeto muitas vezes é rodado localmente, para não exigir um novo deploy a cada pequena iteração.

A arquitetura dos github actions do projeto - extremamente importantes para o bom funcionamento da aplicação - deve funcionar de maneira a realizar estas ações todo dia e disponibilizar o dado tanto no uso em deploy quanto no uso local. Versões iniciais da aplicação exigiam que se rodasse o script 'main.py', e a visão do produto é que isso não seja mais necessário. 