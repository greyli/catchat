$(document).ready(function () {
    var popupLoading = '<i class="notched circle loading icon green"></i> Loading...';

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    function scrollToBottom() {
        var $messages = $('.messages');
        $messages.scrollTop($messages[0].scrollHeight);
    }

    function activateSemantics() {
        $('.ui.dropdown').dropdown();
        $('.ui.checkbox').checkbox();

        $('.message .close').on('click', function () {
            $(this).closest('.message').transition('fade');
        });

        $('#toggle-sidebar').on('click', function () {
            $('.menu.sidebar').sidebar('setting', 'transition', 'overlay').sidebar('toggle');
        });

        $('.pop-card').popup({
            inline: true,
            on: 'hover',
            hoverable: true,
            html: popupLoading,
            delay: {
                show: 200,
                hide: 200
            },
            onShow: function () {
                var popup = this;
                popup.html(popupLoading);
                $.get({
                    url: $(popup).prev().data('href')
                }).done(function (data) {
                    popup.html(data);
                }).fail(function () {
                    popup.html('Failed to load profile.');
                });
            }
        });
    }

    function init() {
        activateSemantics();
        scrollToBottom();
    }

    init();

});
