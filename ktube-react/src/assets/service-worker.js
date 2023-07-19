self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open('my-cache').then(function(cache) {
      return cache.addAll([
        // Add URLs of static files to cache
        '/',
        '/css/loaders/loader0.css',
        '/css/cdn/all.css',
        '/css/cdn/bootstrap.css',
        '/css/cdn/bootstrap.min.css',
        '/css/cdn/cssFamilycookie.css',
        '/css/cdn/font-awesome.min.css',
        '/css/cdn/free-v4-font-face.min.css',
        '/css/cdn/free-v4-shims.min.css',
        '/css/cdn/free-v5-font-face.min.css',
        '/css/cdn/free.min.css',
        '/css/footer.css',
        '/css/home.css',
        '/css/main.css',
        '/css/profile.css',
        '/css/tube.css',
        '/js/bootstrap.bundle.min.js',
        '/js/bootstrap.min.js',
        '/js/c44ff25b2e.js',
        '/js/jquery-3.7.0.min.js',
        '/js/popper.min.js',
        '/js/watch.js',
        '/js/main.js',
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
