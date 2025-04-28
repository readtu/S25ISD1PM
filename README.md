# Chairs

Chairs is a class scheduling website designed for use by Taylor University.

Developed by the Zeta Core team in the Spring 2025 semester for the Information Systems Design class at Taylor University, taught by Professor Doug Read. 💪

## Linting & Formatting

The code in this repo was [linted](https://code.visualstudio.com/docs/python/linting) and formatted with [Ruff](https://docs.astral.sh/ruff/). Please continue using Ruff to lint and format the code frequently, to avoid inconsistent syntax, ambiguous code, sneaky bugs, and unnecessary Git merge conflicts due to whitespace.

Annoying false positives from Ruff can be muted on a per-line basis using `# noqa` comments, a per-file basis using `# ruff: noqa` comments, or on a global scale inside the `pyproject.toml` file. Please do not mute issues on a global scale if it is only a false positive for a few lines or a few files.

## Styling

This app uses the [Bootstrap](https://getbootstrap.com) CSS and JS framework. Bootstrap is built on [SCSS (also known as SASS)](https://sass-lang.com), which is a superset of CSS that compiles to CSS. In this project, SCSS is used to override the Bootstrap variables that are used all throughout the compiled Bootstrap CSS, in order to get a more custom look.

SCSS must be installed on the system. Check the website linked above for instructions.

Instead of pulling Bootstrap from a CDN like JSDeliver (which forces extra requests, introduces more security risks, and has the SCSS precompiled which prevents customization), this repo contains a fixed copy of the uncompiled Bootstrap SCSS source files. (The JS does not (yet) need to be customized and thus the precompiled source JS is simply included.) The SCSS files are imported in the `custom.scss` file, where any customization to variables can be made. The Bootstrap documentation side (linked above) contains tons of information on what the available variables for customization are, including everything from font-sizes to colors to border-radiuses to shadows.

**The SCSS must be recompiled anytime a change is made to the custom.scss file.** A convenience command for doing just this is supplied with this repo and is shown below. [Make sure SCSS is installed for your platform](https://sass-lang.com/install/) before running the command.

```bash
./compile_scss.sh
```

### Database

When in local development, this app uses SQLite 3 as the database backend. This makes development easy because SQLite comes bundled with Python, instead of needing to be installed on the system. Additionally, all the database information is stored inside a single file, `db.sqlite3`, which can be copy-pasted to backup or restore the database, or deleted to drop the database. Most importantly, it keeps the production data safe, and is not shared between developers. Note that the database file is and should be `.gitignore`-d.

When in production, this app uses PostgreSQL as the database backend. This does require installation and configuration on the system.

## Troubleshooting

-   **I'm getting `python: command not found` or `pip: command not found`** Try using `python3` and `pip3`. Make sure it's the right version of Python.
-   **I'm getting an unexpected `SyntaxError`.** Make sure you're using the right version of Python.
-   **I'm getting an unexpected `ModuleNotFoundError`.** Make sure you have all the most recent dependencies installed from `requirements.txt`.
-   **I'm getting an error when installing the dependencies.** Installing the `mysqlclient` library frequently causes a build error when it has not been installed before. MySQL must be installed on the system for the package install to work. So either:
    1. Install MySQL on the current platform (sometimes easy, such as using brew install—sometimes hard)
    2. Skip the MySQL dependency by commenting it out of the requirements file locally or installing the listed dependencies one-by-one
-   **I'm getting an `OperationalError: no such column/table`.** Make sure your database exists, has migrations made for models.py, and has the migrations applied. See the [databases](#database) section.
-   **The site looks unstyled.** Make sure you have compiled the SCSS. See the [Styling](#styling) section.
