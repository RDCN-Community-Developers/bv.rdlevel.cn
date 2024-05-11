'use strict';

(() => {
    function addAuthor(name, uid, imageUrl) {
        const template = `<li>
            <details>
                <summary><span class="author"><span>来自作者：<a href="https://space.bilibili.com/${uid}"
                                target="_blank">${name}</a> </span>${(typeof imageUrl) == 'string' ? `<img src="${imageUrl}" alt="${name}" width="20" height="20">` : ''}</span></summary>
                <ul class="list", id="author-list-${uid}">
                </ul>
            </details>
        </li>`;
        $('#author-list').append(template);
    }
    
    function addVideo(uid, videoId, videoName) {
        const template = `<li class="level-name">
            <a href="https://www.bilibili.com/video/${videoId}" target="_blank">${videoName}</a>
        </li>`;
        $(`#author-list-${uid}`).append(template);
    }
    
    function showError(error) {
        console.error(error);
        $('#author-list').append(`<div class="menuline">列表被鸟蛋吃了，请尝试刷新页面。</div>`)
    }
    
    $(() => {
        fetch('./showlist.json')
            .then(res => res.json())
            .then(data => {
                const authors = data.authors;
                for (const author_id in authors) {
                    const author = authors[author_id];
                    addAuthor(author.name, author_id, author.avatar ?? null);
    
                    for (const video_id in author.videos) {
                        const video = author.videos[video_id];
                        addVideo(author_id, video_id, video.title);
                    }
                }
            }).catch(showError);
    });
})();