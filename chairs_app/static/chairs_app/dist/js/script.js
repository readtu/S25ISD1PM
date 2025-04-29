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
    });
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
