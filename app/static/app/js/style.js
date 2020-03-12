
//ハンバーガーメニュー
(function($) {
    $(function () {
        $('#nav-toggle').on('click', function() {
        $('body').toggleClass('open');
        });
    });
    $(function () {
        $('li').on('click', function() {
        $('body').toggleClass('open');
        });
    });
})(jQuery);

