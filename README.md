# baseProjectTemplate

base fastapi &amp;&amp; discord.py project template. with &lt;3 by yxzhin ^^

## requirements

- docker
- uv

## setup

1. clone the repository: `git clone https://github.com/yxzhin/baseProjectTemplate; cd baseProjectTemplate`
2. create python virtual environment &amp;&amp; install the requirements: `uv venv; uv sync`
3. copy `.env.example` to `.env` &amp;&amp; edit the secrets with yours
4. install the pre-commit hooks (done only once): `uv run pre-commit install`
5. (optional) import vscode profile: `baseProjectTemplate.code-profile`

## run

1. run docker compose: `docker compose up -d`
2. in the first powershell instance, run fastapi server: `scripts\run-server` &amp;&amp; go to `https://localhost:8000/test` to test it
3. in the second one, run discord.py bot: `scripts\run-bot` &amp;&amp; use commands `/ping` &amp;&amp; `/api_test` to test it

## credits

- [@Dimitrymas](https://github.com/Dimitrymas) for some stuff
- [@GrygoryZach](https://github.com/GrygoryZach) && [@GrujicFilipRS](https://github.com/GrujicFilipRS) for inspiration &amp;&amp; motivation &lt;3
