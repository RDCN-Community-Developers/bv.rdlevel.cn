'use strict';

function addVideo(uid, videoId, videoName) {
    var template = `<li class="level-name">
    <a href="https://www.bilibili.com/video/${videoId}" target="_blank">${videoName}</a>
</li>`;
    $(`#author-list-${uid}`).append(template);
}

fetch('./videos.txt').then(res => {
    res.text()
    .split('\n')
    .filter(line => line.length > 0 && line[0] != '#')
    .forEach(line => {
        var args = line.split('|');
        if (args.length < 2) {
            return;
        }
        addVideo(args[0], args[1], args[2]);
    });
});