document.querySelectorAll("input[data-refresh]").forEach(function (element) {
    element.addEventListener("change", function (event) {
        event.target.form.submit();
    })
})

document.querySelectorAll("form[data-confirm]").forEach(function (element) {
    element.addEventListener("submit", function (event) {
        if (!confirm(element.dataset.confirm)) {event.preventDefault()}
    })
})