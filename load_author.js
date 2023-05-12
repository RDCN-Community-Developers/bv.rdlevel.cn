'use strict';

function addAuthor(name, uid, imageUrl) {
    var template = `<li>
    <details>
        <summary><span class="author"><span>来自作者：<a href="https://space.bilibili.com/${uid}"
                        target="_blank">${name}</a> </span>${(typeof imageUrl) == 'string' ? `<img src="${imageUrl}" alt="${name}" width="20" height="20">` : ''}</span></summary>
        <ul class="list", id="author-list-${uid}">
        </ul>
    </details>
</li>`;
    $('#author-list').append(template);
}

fetch('./authors.txt').then(res => {
    res.text()
    .split('\n')
    .filter(line => line.length > 0 && line[0] != '#')
    .forEach(line => {
        var args = line.split('|');
        if (args.length < 2) {
            return;
        }
        addAuthor(args[0], args[1], args[2]);
    });
});