## RUFF

---
### Lint

Durante a análise estática do código, queremos buscar por pontos específicos. No **Ruff**, isso é feito por meio de **códigos de verificação**, que indicam exatamente o que deve ser analisado. Usaremos os seguintes:

* **I (Isort)**: Verifica a ordenação dos imports em ordem alfabética.
* **F (Pyflakes)**: Identifica erros relacionados a boas práticas de código.
* **E (pycodestyle - Errors)**: Aponta erros de estilo no código.
* **W (pycodestyle - Warnings)**: Gera avisos sobre práticas não recomendadas de estilo.
* **PL (Pylint)**: Assim como o Pyflakes, busca por erros ligados a boas práticas.
* **PT (flake8-pytest)**: Avalia boas práticas específicas para testes usando Pytest.

---
