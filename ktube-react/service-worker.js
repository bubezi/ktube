self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open('my-cache').then(function(cache) {
      return cache.addAll([
        // Add URLs of static files to cache
        '/',
        './src/assets/css/loaders/loader0.css',
        './src/assets/css/cdn/all.css',
        './src/assets/css/cdn/bootstrap.css',
        './src/assets/css/cdn/bootstrap.min.css',
        './src/assets/css/cdn/cssFamilycookie.css',
        './src/assets/css/cdn/font-awesome.min.css',
        './src/assets/css/cdn/free-v4-font-face.min.css',
        './src/assets/css/cdn/free-v4-shims.min.css',
        './src/assets/css/cdn/free-v5-font-face.min.css',
        './src/assets/css/cdn/free.min.css',
        './src/assets/css/footer.css',
        './src/assets/css/home.css',
        './src/assets/css/main.css',
        './src/assets/css/profile.css',
        './src/assets/css/tube.css',
        './src/assets/js/bootstrap.bundle.min.js',
        './src/assets/js/bootstrap.min.js',
        './src/assets/js/c44ff25b2e.js',
        './src/assets/js/jquery-3.7.0.min.js',
        './src/assets/js/popper.min.js',
        './src/assets/js/watch.js',
        './src/assets/js/main.js',
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


// if ('serviceWorker' in navigator) {
//   navigator.serviceWorker.register('/service-worker.js', {
//     scope: '/' // Adjust the scope as per your requirements
//     // scope: 'http://127.0.0.1:8000/' // Adjust the scope as per your requirements
//   })
//   .then(registration => {
//     console.log('Service worker registered with scope:', registration.scope);
//   })
//   .catch(error => {
//     console.error('Failed to register service worker:', error);
//   });
// }
