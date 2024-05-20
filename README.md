# TDD Project

## Resolução do Desafio 
```shell
  $Arvoré de arquivos 
- se comunica com apps externas;
controllers/
│
├── product.py
│   ├── post - Para o  tratamento de exceção para InsertException no método post
│   └── patch - Aqui p tratamento de exceção para NotFoundException no método patch
│  
core/
│
└── exceptions.py
    ├── InsertException - Nova exceção adicionada para tratamento de erros de inserção
    └── NotFoundException - Exceção existente usada para tratamento de dados não encontrados
│
usecases/
│
└── product.py
    ├── create - Caso erro de inserção e aceitação de preço no método create
    └── update - inclusão  exceção NotFoundException e atualização de updated_at no método update
   
      

```

```ruby

    class ProductUsecase:
    async def update(self, id: UUID4, body: ProductUpdate) -> ProductUpdateOut:
        try:
            # Lógica para atualizar o produto
        except Exception as e:
            raise NotFoundException("Produto não encontrado")
           

```

```ruby
# Update: Modifique o método de patch para retornar uma exceção de Not Found
#Importação 
from store.core.exceptions import NotFoundException
from store.schemas.product import ProductUpdate, ProductUpdateOut

@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: UUID4 = Path(alias="id"),
    body: ProductUpdate = Body(...),
    usecase: ProductUsecase = Depends(),
) -> ProductUpdateOut:
    try:
        return await usecase.update(id=id, body=body)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado ou nenhum campo para atualizar.")

```
```ruby

# ********Controller/product.py 
@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...),
    price: float = Body(...),
    usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        return await usecase.create(body=body, price=price)
    except InsertException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao inserir o produto. Por favor, tente novamente.")
 ```

```ruby
 #***Usecase/product.py
class ProductUsecase:
    async def create(self, body: ProductIn, price: float) -> ProductOut:
        try:
            # Lógica para inserir o produto com o preço
        except Exception as e:
            raise InsertException(f"Error inserting product: {str(e)}")

    async def query(self, min_price: float = 5000, max_price: float = 8000, nome: Optional[str] = None, cpf: Optional[str] = None) -> List[ProductOut]:
        query = {
            "price": {"$gt": min_price, "$lt": max_price}
        }
        # Lógica para aplicar filtros adicionais (nome, cpf, etc.)

```
## CRUD(Como exposto no Video , seguindo os principios ) 

Create (Criação de Produto):

    Para a operação de criação de produto, precisamos implementar a lógica para inserir um novo produto no banco de dados. Isso envolve receber os dados do produto, como nome, quantidade, preço e status, e salvá-los no banco de dados. Além disso, podemos adicionar validações para garantir que os dados fornecidos sejam válidos antes de salvar.
    Após a implementação, podemos escrever testes para garantir que a criação de produto funcione corretamente. Os testes devem verificar se um novo produto é criado com sucesso no banco de dados e se os dados inseridos correspondem aos dados fornecidos.

Read (Leitura de Produto):

    A operação de leitura de produto envolve recuperar informações sobre um produto específico ou uma lista de produtos do banco de dados. Isso pode ser feito consultando o banco de dados com base em filtros como ID, nome, preço, etc.
    Para testar a leitura de produtos, podemos escrever testes que verifiquem se os produtos são recuperados corretamente do banco de dados com base nos filtros fornecidos.

Update (Atualização de Produto):

    Atualizar um produto envolve modificar os dados de um produto existente no banco de dados. Isso geralmente é feito através de uma solicitação PATCH, onde os campos do produto que precisam ser atualizados são enviados junto com o ID do produto.
    Ao implementar a atualização de produto, devemos garantir que apenas os campos fornecidos sejam atualizados e que o campo updated_at seja atualizado com a data e hora atuais.
    Os testes para a atualização de produto devem garantir que os dados do produto sejam atualizados corretamente no banco de dados e que o campo updated_at seja atualizado conforme esperado.

Delete (Exclusão de Produto):

    A operação de exclusão de produto envolve remover um produto específico do banco de dados com base no ID do produto fornecido.
    Ao implementar a exclusão de produto, devemos garantir que o produto seja removido corretamente do banco de dados e que seja retornado um código de status apropriado para indicar o sucesso da operação.
    Os testes para a exclusão de produto devem verificar se o produto é removido com sucesso do banco de dados e se um código de status apropriado é retornado.

Testes de Use Cases:

    Os testes de Use Cases são escritos para testar a lógica de negócios da aplicação, isolando-a de qualquer dependência externa, como bancos de dados ou APIs.
    Para testar os casos de uso relacionados aos produtos, devemos criar objetos mock ou simulados que imitem o comportamento do banco de dados e outras dependências externas.
    Os testes devem cobrir todos os cenários possíveis para cada caso de uso, incluindo casos de sucesso e casos de falha.
    Os testes devem garantir que a lógica de negócios funcione conforme o esperado, manipulando adequadamente entradas válidas e inválidas, e gerando resultados corretos.


## O que é TDD?
TDD é uma sigla para `Test Driven Development`, ou Desenvolvimento Orientado a Testes. A ideia do TDD é que você trabalhe em ciclos.

### Ciclo do TDD
![C4](/docs/img/img-tdd.png)

### Vantagens do TDD
- entregar software de qualidade;
- testar procurando possíveis falhas;
- criar testes de integração, testes isolados (unitários);
- evitar escrever códigos complexos ou que não sigam os pré-requisitos necessários;

A proposta do TDD é que você codifique antes mesmo do código existir, isso nos garante mais qualidade no nosso projeto. Além de que, provavelmente se você deixar pra fazer os testes no final, pode acabar não fazendo. Com isso, sua aplicação perde qualidade e está muito mais propensa a erros.

# Store API
## Resumo do projeto
Este documento traz informações do desenvolvimento de uma API em FastAPI a partir do TDD.

## Objetivo
Essa aplicação tem como objetivo principal trazer conhecimentos sobre o TDD, na prática, desenvolvendo uma API com o Framework Python, FastAPI. Utilizando o banco de dados MongoDB, para validações o Pydantic, para os testes Pytest e entre outras bibliotecas.

## O que é?
Uma aplicação que:
- tem fins educativos;
- permite o aprendizado prático sobre TDD com FastAPI + Pytest;

## O que não é?
Uma aplicação que:
## Solução Proposta
Desenvolvimento de uma aplicação simples a partir do TDD, que permite entender como criar tests com o `pytest`. Construindo testes de Schemas, Usecases e Controllers (teste de integração).

### Arquitetura
|![C4](/docs/img/store.drawio.png)|
|:--:|
| Diagrama de C4 da Store API |

### Banco de dados - MongoDB
|![C4](/docs/img/product.drawio.png)|
|:--:|
| Database - Store API |



## Desafio Final
- Create
    - Mapear uma exceção, caso dê algum erro de inserção e capturar na controller
- Update
    - Modifique o método de patch para retornar uma exceção de Not Found, quando o dado não for encontrado
    - a exceção deve ser tratada na controller, pra ser retornada uma mensagem amigável pro usuário
    - ao alterar um dado, a data de updated_at deve corresponder ao time atual, permitir modificar updated_at também
- Filtros
    - cadastre produtos com preços diferentes
    - aplique um filtro de preço, assim: (price > 5000 and price < 8000)

## Preparar ambiente

Vamos utilizar Pyenv + Poetry, link de como preparar o ambiente abaixo:

[poetry-documentation](https://github.com/nayannanara/poetry-documentation/blob/master/poetry-documentation.md)

## Links uteis de documentação
[mermaid](https://mermaid.js.org/)

[pydantic](https://docs.pydantic.dev/dev/)

[validatores-pydantic](https://docs.pydantic.dev/latest/concepts/validators/)

[model-serializer](https://docs.pydantic.dev/dev/api/functional_serializers/#pydantic.functional_serializers.model_serializer)

[mongo-motor](https://motor.readthedocs.io/en/stable/)

[pytest](https://docs.pytest.org/en/7.4.x/)
