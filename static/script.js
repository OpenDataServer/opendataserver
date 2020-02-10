$('select[name=language]').on('change', () => {
    $('#selectLanguageForm').submit();
});

$('.dropdown').on('click', (event) => {
    event.stopPropagation();
    event.currentTarget.classList.toggle("is-active");
});