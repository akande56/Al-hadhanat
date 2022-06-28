importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.0.0/workbox-sw.js');

const VERSION = "n-django-pwa-v" + new Date().getTime();

if (workbox) {
  console.log(`Yay! Workbox is loaded 🎉`);
} else {
  console.log(`Boo! Workbox didn't load 😬`);
}

// const OFFLINE_URL = '/offline/';
const appShell = [
    // '/',
    '/offlined/',
    // '/student/dashboard',
    // '/student/formmaster/class',
].map((partialUrl) => `${location.protocol}//${location.host}${partialUrl}`);

// Precache the shell.
workbox.precaching.precacheAndRoute(appShell.map(url => ({
    url,
    revision: 2000,
})));

// Serve the app shell from the cache.
workbox.routing.registerRoute(({url}) => appShell.includes(url), new workbox.strategies.CacheOnly());

// Serve the other pages from the cache and make a request to update the value in the cache.
// Limit the cache to 5 entries.
workbox.routing.registerRoute(
    ({url}) => !appShell.includes(url),
    new workbox.strategies.NetworkFirst({
        cacheName: 'dynamic-cache',
        plugins: [new workbox.expiration.ExpirationPlugin({
            maxEntries: 120,
        })],
    })
);

// Handle offline.
// From https://developers.google.com/web/tools/workbox/guides/advanced-recipes#provide_a_fallback_response_to_a_route
workbox.routing.setCatchHandler(({ event }) => {
    console.log(event)
    switch (event.request.method) {
        case 'GET':
            return caches.match('/offlined/');
        default:
            return Response.error();
    }
});
