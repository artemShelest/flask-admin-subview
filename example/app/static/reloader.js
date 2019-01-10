(function ($) {
    Subview.addUpdateListener(function (type) {
        if (type === Subview.ERROR) {
            return;
        }
        Subview.reloadExcept(this);
    });
})(jQuery);
