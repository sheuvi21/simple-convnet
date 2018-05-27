$(function () {
    var form = $('#processForm'),
        submitButton = form.find('input[type=submit]'),
        resultArea = $('#resultArea');

    function getResult(url) {
        var timer = setInterval(function () {
            $.get(url, function (response) {
                if (response['ok']) {
                    clearInterval(timer);

                    submitButton.prop('disabled', false);

                    var result = _.max(response['result'], function (item) {
                        return item['prediction'];
                    });
                    resultArea.append('Я думаю, это ' + result['label'] + '\n');
                }
                else {
                    resultArea.append('...\n');
                }
                resultArea.scrollTop(resultArea[0].scrollHeight);
            });
        }, 2000);
    }

    form.submit(function (e) {
        e.preventDefault();

        submitButton.prop('disabled', true);

        $.ajax({
            method: form.attr('method'),
            url: form.attr('action'),
            processData: false,
            contentType: false,
            data: new FormData(form[0])
        })
            .done(function (response) {
                if (response['ok']) {
                    getResult(response['get_url']);
                }
            });
    });
});