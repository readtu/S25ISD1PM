# Chairs

Chairs is a class scheduling website designed for use by Taylor University.

Developed by the Zeta Core team in the Spring 2025 semester for the Information Systems Design class at Taylor University, taught by Professor Doug Read. 💪

## Configuration & Execution

### Development

1. Install [Python 3.13](https://python.org), and configure it properly on your PATH.
2. **Optional**: configure a [Python virtual environment](https://docs.python.org/3/library/venv.html) in a directory.
3. Install all the necessary requirements from `requirements.txt` by running:

    ```bash
    pip install -r requirements.txt
    ```

4. Install [Dart Sass](https://sass-lang.com), and run:

    ```bash
    ./compile_scss.sh
    ```

5. Create the `.env` file, which specifies:

    ```ini
    DEBUG=True
    SECRET_KEY=<an_arbitrary_secret_key>
    BANNER_API_KEY=<the_banner_api_key>
    ```

    Contact the project maintainer to recieve any missing credentials.

6. Instantiate the database by running:

    ```bash
    python manage.py migrate
    ```

7. If this is your first time cloning the repository, populate the local database by running:

    ```bash
    python manage.py populate
    ```

    This command only works in production.
8. Start the development server by clicking the Play button in the Run & Debug pane in Visual Studio Code, or otherwise run this command:

    ```bash
    python manage.py runserver
    ```

### Production

This app is designed to be deployed using ASGI, to allow the app to support asynchronous features and WebSockets. Specifically, the app is designed to be [deployed with Daphne](https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/daphne/). The server deploying the app should be configured with Nginx to reverse proxy to Daphne.

For production, the .env file must also specify:

```ini
DATABASE_PASSWORD=<the_database_password>
```

Currently, the server is at `ssh isd2025s-1pm.cse.taylor.edu`, and can be authenticated into using CSE credentials.

Some notes about deployment:

- The global Nginx configuration file is stored in `/etc/nginx/nginx.conf`.
- The configuration file for the Nginx site specific to Chairs is in `/etc/nginx/sites-available/chairs.conf`.
- The repository files are stored in `/home/chairs_user/chairs/S25ISD1PM`. This is where you'll need to run `git pull` inside.
- A Python virtual environment for storing the pip packages is stored in the parent directory of the repository, and can be activated by running `source /home/chairs_user/chairs/bin/activate`.
- Nginx is configured as a service, and the systemd configuration file is stored in `/lib/systemd/system/nginx.service`.
    - You can check on the service status using `systemctl status nginx`.
    - If you change the configuration file above, you'll need to run `systemctl daemon-reload`.
    - You can restart the service using `systemctl restart nginx`.
- Daphne is also configured as a service, and the system configuration file is stored in `/etc/systemd/system/chairs_daphne.service`.
    - You can check on the service status using `systemctl status chairs_daphne`.
    - If you change the configuration file above, you'll need to run `systemctl daemon-reload`.
    - You can restart the service using `systemctl restart chairs_daphne`.

Currently, Chairs is deployed at `chairs.cse.taylor.edu`.

## Linting & Formatting

The code in this repo was [linted](https://code.visualstudio.com/docs/python/linting) and formatted with [Ruff](https://docs.astral.sh/ruff/). Please continue using Ruff to lint and format the code frequently, to avoid inconsistent syntax, ambiguous code, sneaky bugs, and unnecessary Git merge conflicts due to whitespace.

Annoying false positives from Ruff can be muted on a per-line basis using `# noqa` comments, a per-file basis using `# ruff: noqa` comments, or on a global scale inside the `pyproject.toml` file. Please do not mute issues on a global scale if it is only a false positive for a few lines or a few files.

## Styling

This app uses the [Bootstrap](https://getbootstrap.com) CSS and JS framework. Bootstrap is built on [SCSS (also known as SASS)](https://sass-lang.com), which is a superset of CSS that compiles to CSS. In this project, SCSS is used to override the Bootstrap variables that are used all throughout the compiled Bootstrap CSS, in order to get a more custom look.

SCSS must be installed on the system. Check the website linked above for instructions.

Instead of pulling Bootstrap from a CDN like JSDeliver (which forces extra requests, introduces more security risks, and has the SCSS precompiled which prevents customization), this repo contains a fixed copy of the uncompiled Bootstrap SCSS source files. (The JS does not (yet) need to be customized and thus the precompiled source JS is simply included.) The SCSS files are imported in the `custom.scss` file, where any customization to variables can be made. The Bootstrap documentation side (linked above) contains tons of information on what the available variables for customization are, including everything from font-sizes to colors to border-radiuses to shadows.

**The SCSS must be recompiled anytime a change is made to the custom.scss file.** A convenience command for doing just this is supplied with this repo and is shown below. [Make sure SCSS is installed for your platform](https://sass-lang.com/install/) before running the command. **Note**: currently, this command dumps out dozens of warnings because Bootstrap is using legacy SCSS syntax constructs. Ignore them, it compiles successfully.

```bash
./compile_scss.sh
```

### Database

When in local development, this app uses SQLite 3 as the database backend. This makes development easy because SQLite comes bundled with Python, instead of needing to be installed on the system. Additionally, all the database information is stored inside a single file, `db.sqlite3`, which can be copy-pasted to backup or restore the database, or deleted to drop the database. Most importantly, it keeps the production data safe, and is not shared between developers. Note that the database file is and should be `.gitignore`-d.

When in production, this app uses PostgreSQL as the database backend. This does require installation and configuration on the system.

## Troubleshooting

- **I'm getting `python: command not found` or `pip: command not found`** Try using `python3` and `pip3`. Make sure it's the right version of Python.
- **I'm getting an unexpected `SyntaxError`.** Make sure you're using the right version of Python.
- **I'm getting an unexpected `ModuleNotFoundError`.** Make sure you have all the most recent dependencies installed from `requirements.txt`.
- **I'm getting an `OperationalError: no such column/table`.** Make sure your database exists, has migrations made for models.py, and has the migrations applied. See the [databases](#database) section.
- **The site looks unstyled.** Make sure you have compiled the SCSS. See the [Styling](#styling) section.
