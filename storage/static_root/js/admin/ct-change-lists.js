$('#action-toggle').show().on('click', function () {
    checker($(this).prop("checked"));
    updateCounter();
});