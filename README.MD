# 🧠 Backend — Sistema de Gestão para Psicólogos

API REST desenvolvida para um sistema de gestão de psicólogos, responsável pelo gerenciamento de pacientes, sessões, pagamentos e anotações.

O projeto nasceu de uma necessidade real: criar uma solução simples para centralizar informações do consultório e facilitar o acompanhamento da rotina profissional.

> 🚧 Projeto em desenvolvimento

---

## 🎯 Objetivo

O objetivo deste projeto é fornecer o backend de uma aplicação de gestão para psicólogos, disponibilizando uma API REST responsável pelas regras de negócio, autenticação, validação e persistência dos dados.

O projeto também está sendo utilizado como estudo prático de desenvolvimento backend com Python, arquitetura de APIs, autenticação, banco de dados e relacionamento entre entidades.

---

## ✨ Funcionalidades

* 👤 Cadastro e gerenciamento de pacientes
* 📅 Cadastro e gerenciamento de sessões
* 💰 Controle de pagamentos
* 📝 Anotações relacionadas às sessões
* 🔐 Autenticação de usuários
* 🛡️ Proteção de rotas
* 🔑 Autenticação baseada em JWT
* 👥 Associação dos dados ao usuário autenticado
* 🔄 API REST para comunicação com o frontend
* ✅ Validação de dados utilizando Pydantic

---

## 🛠️ Tecnologias

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* SQLite
* JWT
* Uvicorn
* Git
* GitHub

---

## 🏗️ Arquitetura

O backend é desenvolvido como uma API REST independente, consumida pelo frontend através de requisições HTTP.

```text
┌─────────────────────────┐
│      React + TypeScript │
│        Frontend         │
└────────────┬────────────┘
             │
             │ HTTP / REST
             ▼
┌─────────────────────────┐
│         FastAPI         │
│          API            │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│       SQLAlchemy        │
│      ORM / Models       │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│         SQLite          │
│        Database         │
└─────────────────────────┘
```

O frontend possui um repositório separado.

---

## 🔐 Autenticação

A API utiliza autenticação baseada em **JWT (JSON Web Token)**.

Após o login, o backend gera um token que deve ser enviado nas requisições protegidas através do header:

```text
Authorization: Bearer <token>
```

As rotas protegidas identificam o usuário autenticado antes de permitir o acesso aos dados.

Isso também permite associar os pacientes e demais informações ao usuário responsável pelo atendimento.

---

## 🗂️ Principais entidades

O backend trabalha com entidades relacionadas à rotina do profissional:

```text
Usuário
   │
   └── Pacientes
          │
          └── Sessões
                 │
                 ├── Anotações
                 └── Pagamentos
```

A estrutura foi pensada para manter os dados relacionados ao profissional autenticado e organizar as informações de acordo com seus relacionamentos.

---

## 🧩 Principais endpoints

A API possui endpoints para operações relacionadas aos pacientes e sessões.

### Autenticação

```text
POST /auth/login
```

### Pacientes

```text
GET    /pacientes
GET    /pacientes/{paciente_id}
GET    /pacientes/{paciente_nome}

POST   /adicionar_pacientes

PUT    /pacientes/{paciente_id}

DELETE /pacientes/{paciente_id}
```

### Sessões

```text
GET /pacientes/{paciente_id}/sessoes
```

A API utiliza schemas do **Pydantic** para validação e serialização das respostas.

---

## 🐛 Desafios técnicos

Durante o desenvolvimento, encontrei problemas que exigiram investigação para identificar suas causas.

### DetachedInstanceError

Um dos problemas ocorreu quando a API tentava retornar pacientes junto com suas sessões.

O SQLAlchemy estava tentando carregar o relacionamento depois que a sessão do banco de dados já havia sido encerrada, resultando em um `DetachedInstanceError`.

Após analisar o traceback e entender o funcionamento do carregamento lazy dos relacionamentos, utilizei `joinedload` para realizar o carregamento antecipado dos dados relacionados enquanto a sessão ainda estava disponível.

Exemplo:

```python
.options(joinedload(Paciente.sessoes))
```

Esse problema me ajudou a entender melhor o funcionamento dos relacionamentos do SQLAlchemy e o ciclo de vida das sessões do banco de dados.

---

## 🗄️ Banco de dados

O projeto utiliza **SQLite** durante o desenvolvimento, com **SQLAlchemy** como ORM.

Durante o desenvolvimento também identifiquei uma característica importante do SQLAlchemy:

```python
Base.metadata.create_all(bind=engine)
```

é utilizado para criar as tabelas que ainda não existem, mas não funciona como um sistema de migrations para alterar automaticamente tabelas existentes.

Esse problema me levou a entender melhor a diferença entre criação inicial do banco e evolução do schema, além da importância de utilizar ferramentas de migration em aplicações que precisam evoluir de forma controlada.

---

## 🧠 O que estou aprendendo com o projeto

Este projeto tem sido utilizado para colocar em prática conhecimentos de:

* Desenvolvimento de APIs REST
* Python e FastAPI
* Modelagem de banco de dados
* SQLAlchemy e relacionamentos
* Autenticação e autorização
* JWT
* Validação de dados com Pydantic
* Tratamento e investigação de erros
* Organização de projetos backend
* Git e controle de versão

---

## 🤖 Possibilidades de IA

Uma das próximas etapas planejadas para o backend é explorar o uso de inteligência artificial para trabalhar com informações textuais.

Algumas possibilidades incluem:

* Estruturação de informações a partir de textos
* Geração de resumos
* Classificação de conteúdos
* Extração estruturada de informações
* Avaliação da qualidade das respostas geradas

A ideia é utilizar IA de forma prática para transformar informações não estruturadas em dados que possam ser utilizados pela aplicação.

---

## 🚀 Próximos passos

* [ ] Adicionar testes automatizados
* [ ] Melhorar tratamento de erros
* [ ] Implementar migrations
* [ ] Melhorar validações
* [ ] Documentar completamente a API
* [ ] Realizar deploy do backend
* [ ] Implementar logs e métricas
* [ ] Explorar funcionalidades utilizando IA

---

## 👨‍💻 Autor

**Lucas Ferreira Camilo**

Estudante de Engenharia de Software e desenvolvedor focado em desenvolvimento full-stack.

### Tecnologias de interesse

* Python
* FastAPI
* React
* TypeScript
* APIs REST
* Bancos de dados
* Inteligência Artificial
* Engenharia de Software

---

⭐ Este projeto está em desenvolvimento e continua sendo evoluído conforme novos requisitos e desafios técnicos aparecem.
