class BaseException(Exception):
    message: str = "Internal Server Error"

    def __init__(self, message: str | None = None) -> None:
        if message:
            self.message = message

    class NotFoundException(BaseException):
        message = "Not Found"

    # Primeira solicitação do Desafio adicionar Excessão de inserção tentei personalizar e fazer uma simples
    # exceptions.py


# tentativa de mensagem personalizada
class InsertException(Exception):
    def __init__(self, message="Erro ao inserir o produto"):
        self.message = message
        super().__init__(self.message)

    class PatchException(BaseException):
        message = "Error ao Atualizar  data"
