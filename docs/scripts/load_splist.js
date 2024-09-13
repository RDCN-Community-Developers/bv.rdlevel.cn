'use strict';

(() => {
    function showError(error) {
        console.error(error);
        $('#sp-list').append(`<div class="menuline">列表被鸟蛋吃了，请尝试刷新页面。</div>`)
    }

    function addChapter(name, id) {
        const template = `<li>
            <details>
                <summary>${name}</summary>
                <table>
                    <tbody id="sp-list-${id}"></tbody>
                </table>
            </details>
        </li>`;
        $('#sp-list').append(template);
    }

    function addVideo(chapterId, id, videoData) {
        let nameConfig = `<a href="javascript:void(0)">${videoData.name}</a>`;
        if (videoData.videoId) {
            let link = `https://www.bilibili.com/video/${videoData.videoId}`;
            if (videoData.p) {
                link += `?p=${videoData.p}`;
            }
            nameConfig = `<a href="${link}" target="_blank">${videoData.name}</a>`;
        } else if (videoData.url) {
            nameConfig = `<a href="${videoData.url}" target="_blank">${videoData.name}</a>`;
        }

        let hiddenConfig = ''
        if (videoData.hidden) {
            hiddenConfig += 'class="heimu-blur"'
        }

        const template = `<tr id="sp-list-${chapterId}-${id}" ${hiddenConfig}>
            <td class="level-id">${id}</td>
            <td class="level-name">${nameConfig}</td>
        </tr>`;
        $(`#sp-list-${chapterId}`).append(template);
    }

    $(() => {
        fetch('./splist.json')
        .then(res => res.json())
        .then(data => {
            for (const chapterId in data) {
                const chapter = data[chapterId];
                addChapter(chapter.name, chapterId);

                for (const levelId in chapter.levels) {
                    const level = chapter.levels[levelId];
                    addVideo(chapterId, levelId, level);
                }
            }
        }).catch(showError);
    });
})();