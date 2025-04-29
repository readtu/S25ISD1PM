const htmlElement = document.querySelector("html");
if (htmlElement.getAttribute("data-bs-theme") === "auto") {
    function updateTheme() {
        document
            .querySelector("html")
            .setAttribute(
                "data-bs-theme",
                window.matchMedia("(prefers-color-scheme: dark)").matches
                    ? "dark"
                    : "light"
            );
    }

    window
        .matchMedia("(prefers-color-scheme: dark)")
        .addEventListener("change", updateTheme);
    updateTheme();
}

document.querySelectorAll("input[data-refresh]").forEach(function (element) {
    element.addEventListener("change", function (event) {
        event.target.form.submit();
    });
});

document
    .querySelectorAll("input[data-filter-kind]")
    .forEach(function (filterElement) {
        const filterKind = filterElement.dataset.filterKind;
        filterElement.addEventListener("input", function (event) {
            const filterValue = filterElement.value.toLowerCase();
            document
                .querySelectorAll(`[data-kind="${filterKind}"][data-value]`)
                .forEach(function (item) {
                    const $itemValue = item.dataset.value.toLowerCase();
                    if (filterValue && !$itemValue.includes(filterValue)) {
                        item.style.display = "none";
                    } else {
                        item.style.display = "";
                    }
                });
        });
    });

function setResetsClass(resetElements, resetsElement) {
    if (
        Array.from(resetElements).some((resetElement) => resetElement.checked)
    ) {
        resetsElement.classList.add("btn-primary");
        resetsElement.classList.remove("btn-light");
    } else {
        resetsElement.classList.remove("btn-primary");
        resetsElement.classList.add("btn-light");
    }
}

document.querySelectorAll("[data-resets]").forEach(function (resetsElement) {
    const resets = resetsElement.dataset.resets;
    const resetElements = document.querySelectorAll(`[data-reset="${resets}"]`);
    resetElements.forEach(function (resetElement) {
        resetElement.addEventListener("change", function (event) {
            setResetsClass(resetElements, resetsElement);
        });
    });
    resetsElement.addEventListener("click", function (event) {
        resetElements.forEach(function (resetElement) {
            resetElement.checked = false;
        });
        setResetsClass(resetElements, resetsElement);
        setQueries();
        query();
    });
});

const delimiter = "+";

document.querySelectorAll("[data-query]").forEach(function (queryElement) {
    queryElement.addEventListener("change", function (event) {
        const url = new URL(window.location.toString());
        const params = new URLSearchParams(url.search);
        const tokens = new Set(
            (params.get(queryElement.name) || "").split(delimiter)
        );
        if (queryElement.checked) {
            tokens.add(queryElement.value);
        } else {
            tokens.delete(queryElement.value);
        }
        if (tokens.size) {
            params.set(queryElement.name, Array.from(tokens).join(delimiter));
        } else {
            params.delete(queryElement.name);
        }
        url.search = params.toString();
        window.history.pushState({ path: url.toString() }, "", url.toString());
        query();
    });
});

function setQueries() {
    const url = new URL(window.location.toString());
    const params = new URLSearchParams(url.search);
    document.querySelectorAll("[data-query]").forEach(function (queryElement) {
        queryElement.checked = (params.get(queryElement.name) || "")
            .split(delimiter)
            .includes(queryElement.value);
    });
}

function query() {
    const url = new URL(window.location.toString());
    const params = new URLSearchParams(url.search);
    document
        .querySelectorAll(`[data-queried]`)
        .forEach(function (queriedElement) {
            for (const [name, value] of params.entries()) {
                const valueTokens = value
                    .split(delimiter)
                    .filter((token) => token.length);
                const _value = queriedElement.dataset[`attribute-${name}`];
                if (
                    valueTokens.length &&
                    valueTokens.every((token) => !_value.includes(token))
                ) {
                    queriedElement.style.display = "none";
                } else {
                    queriedElement.style.display = "";
                }
            }
        });
}

window.addEventListener("load", () => {
    setQueries();
    query();
});
window.addEventListener("popstate", () => {
    setQueries();
    query();
});

document
    .querySelectorAll(`input[type="checkbox"][data-all]`)
    .forEach(function (allElement) {
        const all = allElement.dataset.all;
        allElement.addEventListener("change", function (event) {
            document
                .querySelectorAll(`input[type="checkbox"][data-one="${all}"]`)
                .forEach(function (oneElement) {
                    oneElement.checked = allElement.checked;
                });
        });
    });

document.querySelectorAll("form[data-confirm]").forEach(function (element) {
    element.addEventListener("submit", function (event) {
        if (!confirm(element.dataset.confirm)) {
            event.preventDefault();
        }
    });
});
