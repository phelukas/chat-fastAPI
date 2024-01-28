class EmailAlreadyExistsException(Exception):
    """Exceção levantada quando um e-mail já existe no banco de dados."""

    def __init__(self, email: str):
        self.message = f"O e-mail '{email}' já está em uso."
        super().__init__(self.message)
