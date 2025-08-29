// Service Worker for BioinfoNav
const CACHE_NAME = 'bioinfonav-v1';
const urlsToCache = [
    '/',
    '/index.html',
    '/databases_processed.json',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // 如果有缓存，返回缓存
                if (response) {
                    return response;
                }
                return fetch(event.request);
            })
    );
});