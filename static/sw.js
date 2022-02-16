if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("/sw.js", { scope: "/" }).then(
      function (registration) {
        // Registration was successful
        console.log(
          "ServiceWorker registration successful with scope: ",
          registration.scope
        );
      },
      function (err) {
        // registration failed :(
        console.log("ServiceWorker registration failed: ", err);
      }
    );
  });
}

self.addEventListener("install", (e) => {
  console.log("[Service Worker] Install");
});
self.addEventListener("fetch", (e) => e.respondWith("404"));

self.addEventListener('activate', function(event) {
  // Perform some task
});