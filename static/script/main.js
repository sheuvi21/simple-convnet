$(function () {
    var form = $('#processForm'),
        imageInput = $('#imageInput'),
        resultArea = $('#resultArea');

    function getResult(url) {
        resultArea.empty();

        var timer = setInterval(function () {
            $.get(url, function (response) {
                if (response['ok']) {
                    clearInterval(timer);

                    imageInput.fileinput('clear');

                    var result = _.max(response['result'], function (item) {
                        return item['prediction'];
                    });
                    resultArea.append('Я думаю, это ' + result['label'] + '.\n');
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
        uploadUrl: form.attr('action'),
        uploadExtraData: {
            csrf_token: form.find('[name=csrf_token]').val()
        },
        showRemove: false,
        showPreview: false,
        showCancel: false,
        msgPlaceholder: 'Выберите изображение...',
        layoutTemplates: {
            fileIcon: '<i class="fa fa-file-image"></i>&nbsp;'
        },
        browseLabel: 'Выбрать изображение',
        browseIcon: '<i class="fa fa-images"></i>&nbsp;',
        uploadLabel: 'Распознать',
        uploadTitle: 'Распознать выбранное изображение',
        uploadIcon: '<i class="fa fa-magic"></i>&nbsp;',
        msgUploadEnd: 'Распознавание...'
    });

    imageInput.on('fileuploaded', function (e, data) {
        var response = data.response;
        if (response['ok']) {
            getResult(response['get_url']);
        }
    });
});