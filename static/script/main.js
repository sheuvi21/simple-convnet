$(function () {
    var form = $('#processForm'),
        submitButton = form.find('input[type=submit]'),
        imageInput = $('#imageInput'),
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

    imageInput.fileinput({
        language: 'ru',
        theme: 'fa',
        allowedFileTypes: ['image'],
        showRemove: false,
        showPreview: false,
        browseLabel: 'Выбрать изображение',
        browseIcon: '<i class="fa fa-file-image"></i>&nbsp;',
        uploadLabel: 'Распознать',
        uploadTitle: 'Распознать выбранное изображение',
        uploadIcon: '<i class="fa fa-magic"></i>&nbsp;'
    });

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