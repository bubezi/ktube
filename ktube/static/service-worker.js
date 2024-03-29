self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open('my-cache').then(function(cache) {
      return cache.addAll([
        // Add URLs of static files to cache
        '/',
        '/static/css/loaders/loader0.css',
        '/static/css/cdn/all.css',
        '/static/css/cdn/bootstrap.css',
        '/static/css/cdn/bootstrap.min.css',
        '/static/css/cdn/cssFamilycookie.css',
        '/static/css/cdn/font-awesome.min.css',
        '/static/css/cdn/free-v4-font-face.min.css',
        '/static/css/cdn/free-v4-shims.min.css',
        '/static/css/cdn/free-v5-font-face.min.css',
        '/static/css/cdn/free.min.css',
        '/static/css/footer.css',
        '/static/css/home.css',
        '/static/css/main.css',
        '/static/css/profile.css',
        '/static/css/tube.css',
        '/static/js/bootstrap.bundle.min.js',
        '/static/js/bootstrap.min.js',
        '/static/js/c44ff25b2e.js',
        '/static/js/jquery-3.7.0.min.js',
        '/static/js/popper.min.js',
        '/static/js/watch.js',
        '/static/js/main.js',
      ]);
    })
  );
});

self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      // Delete old caches if needed
      return Promise.all(
        cacheNames.filter(function(cacheName) {
          // Identify and delete old cache(s) if any
          return cacheName.startsWith('my-cache') && cacheName !== 'my-cache';
        }).map(function(cacheName) {
          return caches.delete(cacheName);
        })
      );
    })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request).then(function(response) {
      return response || fetch(event.request);
    })
  );
});


if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js', {
    scope: '/' // Adjust the scope as per your requirements
    // scope: 'http://127.0.0.1:8000/' // Adjust the scope as per your requirements
  })
  .then(registration => {
    console.log('Service worker registered with scope:', registration.scope);
  })
  .catch(error => {
    console.error('Failed to register service worker:', error);
  });
}
