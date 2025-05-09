if (document.documentElement.getAttribute("data-bs-theme") === "auto") {
    function updateTheme() {
        document.documentElement.setAttribute(
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

const delimiter = "+";

function setURLBasedOnCheckBoxes(queryElement = null) {
    const url = new URL(window.location.toString());
    const params = new URLSearchParams(url.search);
    let queryElements;
    if (queryElement) {
        queryElements = [queryElement];
    } else {
        queryElements = document.querySelectorAll("[data-query]");
    }
    for (const queryElement of queryElements) {
        const tokens = new Set(
            (params.get(queryElement.name) || "")
                .split(delimiter)
                .filter((token) => !!token)
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
    }
    url.search = params.toString();
    window.history.pushState({ path: url.toString() }, "", url.toString());
}

function checkBoxesBasedOnURL() {
    const url = new URL(window.location.toString());
    const params = new URLSearchParams(url.search);
    document.querySelectorAll("[data-query]").forEach(function (queryElement) {
        queryElement.checked = (params.get(queryElement.name) || "")
            .split(delimiter)
            .includes(queryElement.value);
    });
}

function filterListBasedOnURL() {
    const url = new URL(window.location.toString());
    const params = new URLSearchParams(url.search);
    document
        .querySelectorAll(`[data-queried]`)
        .forEach(function (queriedElement) {
            let display = true;
            for (const [name, value] of params.entries()) {
                const valueTokens = value
                    .split(delimiter)
                    .filter((token) => token.length);
                const _value = queriedElement.dataset[`attribute-${name}`];
                if (
                    valueTokens.length &&
                    valueTokens.every((token) => !_value.includes(token))
                ) {
                    display = false;
                    break;
                }
            }
            if (display) {
                queriedElement.style.display = "";
            } else {
                queriedElement.style.display = "none";
            }
        });
}

function setResetterClass(resetElements, resetterElement) {
    if (
        Array.from(resetElements).some((resetElement) => resetElement.checked)
    ) {
        resetterElement.classList.add("btn-primary");
        resetterElement.classList.remove("btn-light");
    } else {
        resetterElement.classList.remove("btn-primary");
        resetterElement.classList.add("btn-light");
    }
}

document
    .querySelectorAll("[data-resetter]")
    .forEach(function (resetterElement) {
        const resetter = resetterElement.dataset.resetter;
        const resetElements = document.querySelectorAll(
            `[data-reset="${resetter}"]`
        );
        resetElements.forEach(function (resetElement) {
            resetElement.addEventListener("change", function (event) {
                setResetterClass(resetElements, resetterElement);
            });
        });
        resetterElement.addEventListener("click", function (event) {
            resetElements.forEach(function (resetElement) {
                resetElement.checked = false;
            });
            setURLBasedOnCheckBoxes();
            setResetterClass(resetElements, resetterElement);
            filterListBasedOnURL();
        });
    });

document.querySelectorAll("[data-query]").forEach(function (queryElement) {
    queryElement.addEventListener("change", function (event) {
        setURLBasedOnCheckBoxes(queryElement);
        filterListBasedOnURL();
    });
});

window.addEventListener("load", () => {
    checkBoxesBasedOnURL();
    filterListBasedOnURL();
});
window.addEventListener("popstate", () => {
    checkBoxesBasedOnURL();
    filterListBasedOnURL();
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
