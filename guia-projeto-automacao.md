# Guia Passo a Passo — Projeto de Automação de Testes (API + Web)

Stack escolhida: **Python 3.11 + pytest + Selenium + requests**, CI em **GitHub Actions**, monorepo com README único.

---

## 1. Visão geral da entrega

Você vai entregar **um único repositório público** com dois projetos dentro:

- `api/` — testes de API contra `https://petstore.swagger.io/v2` cobrindo **User**, **Store** e **Pet**.
- `web/` — testes E2E em Selenium contra `https://www.saucedemo.com/` (login → carrinho → checkout).
- `.github/workflows/ci.yml` — pipeline única com **dois jobs paralelos** (api e web), rodando em todo push/PR.
- `README.md` na raiz com instalação, execução, tecnologias, prints e badge da pipeline.

Critérios que serão avaliados (e como cada um aparece no projeto):

| Critério | Onde aparece |
|---|---|
| Qualidade de código | Page Objects (web), API Clients (api), `conftest.py`, fixtures, sem repetição |
| Estratégia de testes | Cenários positivos + negativos, asserções no status + payload + schema |
| CI/CD | `.github/workflows/ci.yml` com 2 jobs, artefatos de relatório |
| Domínio | README com prints, comentários só onde for essencial |

---

## 2. Pré-requisitos locais

```bash
python --version       # 3.11+
pip --version
git --version
google-chrome --version  # ou chromium
```

Selenium 4 já baixa o ChromeDriver sozinho via Selenium Manager — não precisa instalar driver manualmente.

---

## 3. Estrutura final do repositório

```
qa-automation-bootcamp/
├── README.md
├── requirements.txt
├── pytest.ini
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── api/
│   ├── conftest.py
│   ├── clients/
│   │   ├── __init__.py
│   │   ├── base_client.py
│   │   ├── user_client.py
│   │   ├── store_client.py
│   │   └── pet_client.py
│   ├── data/
│   │   └── payloads.py
│   └── tests/
│       ├── test_user.py
│       ├── test_store.py
│       └── test_pet.py
└── web/
    ├── conftest.py
    ├── pages/
    │   ├── __init__.py
    │   ├── base_page.py
    │   ├── login_page.py
    │   ├── inventory_page.py
    │   ├── cart_page.py
    │   ├── checkout_page.py
    │   └── checkout_complete_page.py
    └── tests/
        └── test_e2e_purchase.py
```

---

## 4. Setup inicial do projeto

### 4.1 Criar e inicializar o repositório

```bash
mkdir qa-automation-bootcamp && cd qa-automation-bootcamp
git init
git branch -M main
```

### 4.2 `requirements.txt`

```
pytest==8.3.3
pytest-html==4.1.1
requests==2.32.3
jsonschema==4.23.0
selenium==4.25.0
webdriver-manager==4.0.2
```

### 4.3 `pytest.ini` (na raiz)

```ini
[pytest]
markers =
    api: API tests (Petstore)
    web: Web E2E tests (SauceDemo)
    smoke: Smoke subset
addopts = -ra -v
testpaths = api/tests web/tests
```

### 4.4 `.gitignore`

```
__pycache__/
*.pyc
.venv/
.pytest_cache/
report*.html
assets/
allure-results/
.env
```

### 4.5 Ambiente virtual e instalação

```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 5. Projeto de API — Petstore

Padrão usado: **API Client Pattern** (equivalente ao Page Object para APIs). Cada recurso (User, Store, Pet) tem sua própria classe encapsulando os endpoints. Os testes só chamam métodos do client e fazem asserções.

### 5.1 `api/clients/base_client.py`

```python
import requests

class BaseClient:
    BASE_URL = "https://petstore.swagger.io/v2"

    def __init__(self, session: requests.Session):
        self.session = session

    def _url(self, path: str) -> str:
        return f"{self.BASE_URL}{path}"
```

### 5.2 `api/clients/user_client.py`

```python
from .base_client import BaseClient

class UserClient(BaseClient):
    def create(self, payload: dict):
        return self.session.post(self._url("/user"), json=payload)

    def get(self, username: str):
        return self.session.get(self._url(f"/user/{username}"))

    def update(self, username: str, payload: dict):
        return self.session.put(self._url(f"/user/{username}"), json=payload)

    def delete(self, username: str):
        return self.session.delete(self._url(f"/user/{username}"))

    def login(self, username: str, password: str):
        return self.session.get(
            self._url("/user/login"),
            params={"username": username, "password": password},
        )

    def logout(self):
        return self.session.get(self._url("/user/logout"))
```

### 5.3 `api/clients/store_client.py`

```python
from .base_client import BaseClient

class StoreClient(BaseClient):
    def place_order(self, payload: dict):
        return self.session.post(self._url("/store/order"), json=payload)

    def get_order(self, order_id: int):
        return self.session.get(self._url(f"/store/order/{order_id}"))

    def delete_order(self, order_id: int):
        return self.session.delete(self._url(f"/store/order/{order_id}"))

    def inventory(self):
        return self.session.get(self._url("/store/inventory"))
```

### 5.4 `api/clients/pet_client.py`

```python
from .base_client import BaseClient

class PetClient(BaseClient):
    def create(self, payload: dict):
        return self.session.post(self._url("/pet"), json=payload)

    def get(self, pet_id: int):
        return self.session.get(self._url(f"/pet/{pet_id}"))

    def update(self, payload: dict):
        return self.session.put(self._url("/pet"), json=payload)

    def delete(self, pet_id: int):
        return self.session.delete(self._url(f"/pet/{pet_id}"))

    def find_by_status(self, status: str):
        return self.session.get(
            self._url("/pet/findByStatus"), params={"status": status}
        )
```

### 5.5 `api/data/payloads.py`

```python
import time

def unique_id() -> int:
    return int(time.time() * 1000)

def pet_payload(pet_id: int | None = None) -> dict:
    return {
        "id": pet_id or unique_id(),
        "name": "Rex",
        "category": {"id": 1, "name": "Dogs"},
        "photoUrls": ["https://example.com/rex.png"],
        "tags": [{"id": 1, "name": "vaccinated"}],
        "status": "available",
    }

def user_payload(username: str | None = None) -> dict:
    uname = username or f"user_{unique_id()}"
    return {
        "id": unique_id(),
        "username": uname,
        "firstName": "Andre",
        "lastName": "Tester",
        "email": f"{uname}@test.io",
        "password": "Pass123!",
        "phone": "11999999999",
        "userStatus": 1,
    }

def order_payload(pet_id: int) -> dict:
    return {
        "id": unique_id(),
        "petId": pet_id,
        "quantity": 1,
        "shipDate": "2026-05-01T12:00:00.000Z",
        "status": "placed",
        "complete": True,
    }
```

### 5.6 `api/conftest.py`

```python
import pytest
import requests
from api.clients.user_client import UserClient
from api.clients.store_client import StoreClient
from api.clients.pet_client import PetClient

@pytest.fixture(scope="session")
def http():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json", "Accept": "application/json"})
    yield s
    s.close()

@pytest.fixture
def user_client(http): return UserClient(http)

@pytest.fixture
def store_client(http): return StoreClient(http)

@pytest.fixture
def pet_client(http): return PetClient(http)
```

### 5.7 `api/tests/test_pet.py`

```python
import pytest
from api.data.payloads import pet_payload

@pytest.mark.api
class TestPet:
    def test_create_pet(self, pet_client):
        payload = pet_payload()
        r = pet_client.create(payload)
        assert r.status_code == 200
        body = r.json()
        assert body["id"] == payload["id"]
        assert body["status"] == "available"

    def test_get_pet_by_id(self, pet_client):
        created = pet_client.create(pet_payload()).json()
        r = pet_client.get(created["id"])
        assert r.status_code == 200
        assert r.json()["id"] == created["id"]

    def test_update_pet_status(self, pet_client):
        created = pet_client.create(pet_payload()).json()
        created["status"] = "sold"
        r = pet_client.update(created)
        assert r.status_code == 200
        assert r.json()["status"] == "sold"

    def test_find_by_status_available(self, pet_client):
        r = pet_client.find_by_status("available")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_delete_pet(self, pet_client):
        created = pet_client.create(pet_payload()).json()
        r = pet_client.delete(created["id"])
        assert r.status_code == 200
        assert pet_client.get(created["id"]).status_code == 404

    def test_get_inexistent_pet_returns_404(self, pet_client):
        r = pet_client.get(999999999999)
        assert r.status_code == 404
```

### 5.8 `api/tests/test_store.py`

```python
import pytest
from api.data.payloads import order_payload, pet_payload

@pytest.mark.api
class TestStore:
    def test_place_order(self, store_client, pet_client):
        pet = pet_client.create(pet_payload()).json()
        r = store_client.place_order(order_payload(pet["id"]))
        assert r.status_code == 200
        assert r.json()["status"] == "placed"

    def test_get_order(self, store_client, pet_client):
        pet = pet_client.create(pet_payload()).json()
        order = store_client.place_order(order_payload(pet["id"])).json()
        r = store_client.get_order(order["id"])
        assert r.status_code == 200
        assert r.json()["id"] == order["id"]

    def test_delete_order(self, store_client, pet_client):
        pet = pet_client.create(pet_payload()).json()
        order = store_client.place_order(order_payload(pet["id"])).json()
        r = store_client.delete_order(order["id"])
        assert r.status_code == 200

    def test_inventory(self, store_client):
        r = store_client.inventory()
        assert r.status_code == 200
        assert isinstance(r.json(), dict)
```

### 5.9 `api/tests/test_user.py`

```python
import pytest
from api.data.payloads import user_payload

@pytest.mark.api
class TestUser:
    def test_create_user(self, user_client):
        payload = user_payload()
        r = user_client.create(payload)
        assert r.status_code == 200

    def test_get_user(self, user_client):
        payload = user_payload()
        user_client.create(payload)
        r = user_client.get(payload["username"])
        assert r.status_code == 200
        assert r.json()["username"] == payload["username"]

    def test_update_user(self, user_client):
        payload = user_payload()
        user_client.create(payload)
        payload["firstName"] = "Atualizado"
        r = user_client.update(payload["username"], payload)
        assert r.status_code == 200

    def test_login_logout(self, user_client):
        payload = user_payload()
        user_client.create(payload)
        login = user_client.login(payload["username"], payload["password"])
        assert login.status_code == 200
        assert user_client.logout().status_code == 200

    def test_delete_user(self, user_client):
        payload = user_payload()
        user_client.create(payload)
        r = user_client.delete(payload["username"])
        assert r.status_code == 200
```

### 5.10 Rodar local

```bash
pytest api/tests -m api --html=report-api.html --self-contained-html
```

---

## 6. Projeto Web — SauceDemo (Page Object Pattern)

### 6.1 `web/conftest.py`

```python
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1366,768")
    drv = webdriver.Chrome(options=opts)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()
```

### 6.2 `web/pages/base_page.py`

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    URL: str = ""

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(self.URL)
        return self

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        el = self.find(locator)
        el.clear()
        el.send_keys(text)
```

### 6.3 `web/pages/login_page.py`

```python
from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def login(self, user: str, password: str):
        self.type(self.USERNAME, user)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

    def error_message(self) -> str:
        return self.find(self.ERROR).text
```

### 6.4 `web/pages/inventory_page.py`

```python
from selenium.webdriver.common.by import By
from .base_page import BasePage

class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def add_to_cart(self, product_slug: str):
        self.click((By.ID, f"add-to-cart-{product_slug}"))

    def cart_count(self) -> int:
        try:
            return int(self.find(self.CART_BADGE).text)
        except Exception:
            return 0

    def go_to_cart(self):
        self.click(self.CART_LINK)
```

### 6.5 `web/pages/cart_page.py`

```python
from selenium.webdriver.common.by import By
from .base_page import BasePage

class CartPage(BasePage):
    ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT = (By.ID, "checkout")

    def items_count(self) -> int:
        return len(self.driver.find_elements(*self.ITEMS))

    def checkout(self):
        self.click(self.CHECKOUT)
```

### 6.6 `web/pages/checkout_page.py`

```python
from selenium.webdriver.common.by import By
from .base_page import BasePage

class CheckoutPage(BasePage):
    FIRST = (By.ID, "first-name")
    LAST = (By.ID, "last-name")
    ZIP = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    FINISH = (By.ID, "finish")

    def fill(self, first: str, last: str, zip_code: str):
        self.type(self.FIRST, first)
        self.type(self.LAST, last)
        self.type(self.ZIP, zip_code)
        self.click(self.CONTINUE)

    def finish(self):
        self.click(self.FINISH)
```

### 6.7 `web/pages/checkout_complete_page.py`

```python
from selenium.webdriver.common.by import By
from .base_page import BasePage

class CheckoutCompletePage(BasePage):
    HEADER = (By.CLASS_NAME, "complete-header")

    def confirmation_text(self) -> str:
        return self.find(self.HEADER).text
```

### 6.8 `web/tests/test_e2e_purchase.py`

```python
import pytest
from web.pages.login_page import LoginPage
from web.pages.inventory_page import InventoryPage
from web.pages.cart_page import CartPage
from web.pages.checkout_page import CheckoutPage
from web.pages.checkout_complete_page import CheckoutCompletePage

@pytest.mark.web
class TestPurchaseFlow:
    def test_e2e_purchase(self, driver):
        LoginPage(driver).open().login("standard_user", "secret_sauce")

        inventory = InventoryPage(driver)
        inventory.add_to_cart("sauce-labs-backpack")
        inventory.add_to_cart("sauce-labs-bike-light")
        assert inventory.cart_count() == 2
        inventory.go_to_cart()

        cart = CartPage(driver)
        assert cart.items_count() == 2
        cart.checkout()

        CheckoutPage(driver).fill("Andre", "Tester", "01000-000")
        CheckoutPage(driver).finish()

        assert "Thank you" in CheckoutCompletePage(driver).confirmation_text()

    def test_login_with_invalid_credentials(self, driver):
        login = LoginPage(driver).open()
        login.login("locked_out_user", "secret_sauce")
        assert "locked out" in login.error_message().lower()
```

### 6.9 Rodar local

```bash
pytest web/tests -m web --html=report-web.html --self-contained-html
```

---

## 7. Pipeline CI — GitHub Actions

Crie `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  api-tests:
    name: API Tests (Petstore)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run API tests
        run: pytest api/tests -m api --html=report-api.html --self-contained-html

      - name: Upload API report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: api-report
          path: report-api.html

  web-tests:
    name: Web Tests (SauceDemo)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Install Chrome
        uses: browser-actions/setup-chrome@v1
        with:
          chrome-version: stable

      - name: Run Web tests
        run: pytest web/tests -m web --html=report-web.html --self-contained-html

      - name: Upload Web report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: web-report
          path: report-web.html
```

Pontos importantes:

- Os dois jobs rodam **em paralelo** — atende ao requisito "pipeline deve ser executada nos dois projetos".
- `if: always()` faz subir o relatório mesmo quando o teste falha — útil pra debugar.
- Em runners `ubuntu-latest` o Chrome já vem instalado; o passo `setup-chrome` é uma garantia.
- Selenium Manager (Selenium 4) baixa o ChromeDriver automaticamente — não precisa de step extra.

---

## 8. README.md (raiz)

Esqueleto pronto pra preencher:

````markdown
# QA Automation Bootcamp

[![CI](https://github.com/<seu-usuario>/<seu-repo>/actions/workflows/ci.yml/badge.svg)](https://github.com/<seu-usuario>/<seu-repo>/actions/workflows/ci.yml)

Projeto único cobrindo dois cenários de automação:

- **API** — Swagger Petstore (`/v2`) — endpoints User, Store e Pet.
- **Web** — SauceDemo — fluxo E2E de login → carrinho → checkout.

## Tecnologias

- Python 3.11
- pytest, pytest-html
- requests (API)
- Selenium 4 (Web)
- GitHub Actions (CI)

## Estrutura

```
api/      # Petstore — API Client Pattern
web/      # SauceDemo — Page Object Pattern
.github/  # Pipeline CI
```

## Instalação

```bash
git clone https://github.com/<seu-usuario>/<seu-repo>.git
cd <seu-repo>
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Execução

Tudo:

```bash
pytest
```

Só API:

```bash
pytest api/tests -m api --html=report-api.html --self-contained-html
```

Só Web:

```bash
pytest web/tests -m web --html=report-web.html --self-contained-html
```

## CI

A pipeline `.github/workflows/ci.yml` roda dois jobs em paralelo (API e Web) em todo push/PR para `main`. Relatórios HTML são publicados como artefatos.

## Prints

![API rodando](docs/api-run.png)
![Web rodando](docs/web-run.png)
![Pipeline](docs/pipeline.png)

## Padrões aplicados

- **Page Object Model** para UI
- **API Client** para testes de serviço
- **Fixtures pytest** para isolar setup/teardown
- Asserções específicas em status code + corpo da resposta
````

---

## 9. Prints para o README

Tire prints destas três coisas e salve em `docs/`:

1. Terminal local rodando `pytest api/tests -m api` com tudo verde.
2. Terminal local rodando `pytest web/tests -m web` com tudo verde.
3. A aba **Actions** do GitHub mostrando os dois jobs verdes.

Use Cmd+Shift+4 (mac) ou Win+Shift+S (Windows). Reduza o terminal pra caber só o resumo do pytest.

---

## 10. Ordem de execução recomendada (checklist)

1. Criar repo público vazio no GitHub.
2. Estrutura de pastas + `requirements.txt` + `pytest.ini` + `.gitignore`.
3. Implementar API clients e os 3 arquivos de teste (User, Store, Pet). Rodar local até verde.
4. Implementar Page Objects e o teste E2E. Rodar local até verde.
5. Adicionar `ci.yml`, dar push, conferir Actions.
6. Adicionar prints em `docs/` e finalizar README.
7. Tag de versão `v1.0` e commit final.

---

## 11. Dicas para a apresentação (15 min)

Roteiro sugerido:

1. **0–2 min** — Mostrar o repositório e a estrutura de pastas.
2. **2–5 min** — Explicar o API Client Pattern abrindo `pet_client.py` + um teste; rodar `pytest -m api`.
3. **5–9 min** — Explicar Page Objects abrindo `login_page.py` + `test_e2e_purchase.py`; rodar `pytest -m web -k purchase` (modo headed se conseguir).
4. **9–12 min** — Abrir `ci.yml`, mostrar última execução verde no GitHub Actions e baixar o relatório HTML do artefato.
5. **12–15 min** — Falar de boas práticas aplicadas (fixtures, separação client/teste, asserções específicas, marks) e abrir pra perguntas.

Pontos que a banca costuma cobrar:

- Por que separar o client do teste? (Reuso, manutenção, leitura.)
- Como você isola dados entre testes? (`unique_id()` em payloads, fixtures por teste.)
- O que aconteceria se a Petstore caísse? (Job falha, alerta, possibilidade de retry/skip por marker.)
- Por que `--headless`? (CI não tem display.)

---

## 12. Boas práticas de código (o que evitar)

- Não comentar o óbvio (`# cria o pet`). Comente só decisões não óbvias.
- Não usar `time.sleep` — use `WebDriverWait`/`expected_conditions`.
- Não acoplar dados de teste no código de produção (clients/pages).
- Toda asserção deve ter mensagem clara via comparação direta — evite `assert resp` sozinho.
- Um teste = um cenário. Se cair, deve ser óbvio o que quebrou.

Pronto. Seguindo essa ordem dá pra terminar tudo em um fim de semana e chegar nas apresentações de 07/14 de maio com folga.
