$(options.allToggle).show().on('click', function () {
    checker($(this).prop("checked"));
    updateCounter();
});

$.fn.actions.defaults = {
    allToggle: "#action-toggle",
}