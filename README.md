# DSL Easy SQLite

**DSL Easy SQLite** é uma linguagem de domínio específico (DSL) desenvolvida para facilitar a criação de bancos de dados e esquemas de tabelas no SQLite. Projetada com foco em clareza e simplicidade, esta DSL abstrai a complexidade da sintaxe SQL tradicional, permitindo a definição de estruturas de banco de dados de forma mais legível, rápida e segura.

## ✨ Principais Recursos

- ✅ Sintaxe declarativa e intuitiva  
- ✅ Definição simplificada de colunas e tipos de dados  
- ✅ Suporte a chaves primárias e estrangeiras  
- ✅ Aplicação de restrições (constraints) de forma clara  
- ✅ Redução significativa de código repetitivo  
- ✅ Ideal para prototipagem e projetos que utilizam SQLite  

## 🚀 Exemplo de Uso

```python
from dsl_easy_sqlite import Database, Table, Column, Integer, Text, ForeignKey

db = Database("meu_banco.db")

usuarios = Table("usuarios", [
    Column("id", Integer, primary_key=True),
    Column("nome", Text, not_null=True),
    Column("email", Text, unique=True),
])

pedidos = Table("pedidos", [
    Column("id", Integer, primary_key=True),
    Column("usuario_id", Integer, ForeignKey("usuarios.id")),
    Column("valor_total", Integer),
])

db.create([usuarios, pedidos])
