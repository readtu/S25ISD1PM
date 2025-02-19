document.querySelectorAll("input[data-refresh]").forEach(function (element) {
    element.addEventListener("change", function (event) {
        event.target.form.submit();
    })
})