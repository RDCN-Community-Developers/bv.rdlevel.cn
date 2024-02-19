'use strict';

$(() => {
    let id_regex = /^((av[0-9]+)|(bv[0-9a-zA-Z]{10}))$/i;

    $.ajaxSetup({
        contentType: "application/json; charset=utf-8"
    });

    $('#submit').click(() => {
        let id = $('#video').val();
        if (!id_regex.test(id)) {
            $('#info').text('错误的视频编号');
            return;
        }

        $('#info').text('');

        try {
            $.post("https://api.rdlevel.cn/bv/video",
                JSON.stringify({ id: id }),
                (data, textStatus, jqXHR) => {
                    if (jqXHR.status !== 200) {
                        $('#info').text('提交失败');
                        return;
                    }

                    $('#info').text('提交成功');
                }
            );
        } catch (e) {
            $('#info').text('提交失败');
        }
    });
});