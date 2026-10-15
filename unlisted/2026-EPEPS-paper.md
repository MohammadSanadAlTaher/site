---
layout: articles
permalink: /epeps2026
date: 2026-10-11
sitemap: false
noindex: true
---

<h2 style="text-align:center;">EPEPS 2026 Paper</h2>

<br>

The full paper titled _"Immersion Cooling Fixture for High Power Testing
of Planar Microwave Transmission Lines"_ is available below during the [EPEPS](https://www.epeps.org/) conference from Oct. 18 to 21.


<p style="text-align:center;">Tap on page below to view</p>
<div class="page-grid">
  <div><a href="{{ site.url }}{{ site.baseurl }}/assets/img/AlTaher_EPEPS2026-1.png"><img src="{{ site.url }}{{ site.baseurl }}/assets/img/AlTaher_EPEPS2026-1.png" alt="Page 1"></a></div>
  <div><a href="{{ site.url }}{{ site.baseurl }}/assets/img/AlTaher_EPEPS2026-2.png"><img src="{{ site.url }}{{ site.baseurl }}/assets/img/AlTaher_EPEPS2026-2.png" alt="Page 2"></a></div>
  <div><a href="{{ site.url }}{{ site.baseurl }}/assets/img/AlTaher_EPEPS2026-3.png"><img src="{{ site.url }}{{ site.baseurl }}/assets/img/AlTaher_EPEPS2026-3.png" alt="Page 3"></a></div>
</div>


<p style="text-align:center;">View PDF below or <a href="{{ site.url }}{{ site.baseurl }}/assets/pdf/AlTaher_EPEPS2026.pdf">
click here</a></p>



<div class="pdf-frame">
<object data="{{ site.url }}{{ site.baseurl }}/assets/pdf/AlTaher_EPEPS2026.pdf" width="100%" height="720" type="application/pdf"></object>
</div>




<style>
  .page-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    max-width: 1000px;
    margin: 0 auto 1.5em;
  }

  .page-grid a {
    display: block;
    border-radius: 8px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, .15);
    transition: transform 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  }

  /* Hover: grow slightly and show a left accent in the link colour, like the PDF frame.
     !important switches off the site-wide link contrast effect for these pages only. */
  .page-grid a:hover {
    transform: scale(1.04);
    box-shadow: -4px 0 0 currentColor, 0 4px 12px rgba(0, 0, 0, .2);
    filter: none !important;
  }

  .page-grid img {
    display: block;
    width: 100%;
    height: auto;
    border-radius: 8px;
  }

  /* Full-screen page view */
  .page-viewer {
    width: 100vw;
    height: 100vh;
    height: 100dvh;
    max-width: none;
    max-height: none;
    margin: 0;
    padding: 0;
    border: 0;
    background: rgba(10, 10, 10, .96);
    color: #fff;
  }
  .page-viewer[open] {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .page-viewer::backdrop { background: transparent; }
  .page-viewer img {
    max-width: calc(100% - 24px);
    max-height: calc(100% - 100px);
    object-fit: contain;
    background: #fff;
  }
  .page-viewer-nav {
    position: absolute;
    bottom: 18px;
    left: 0;
    right: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 24px;
    font: 15px/1 sans-serif;
  }
  .page-viewer button {
    width: 44px;
    height: 44px;
    border: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, .14);
    color: #fff;
    font: 28px/1 sans-serif;
    cursor: pointer;
  }
  .page-viewer button:disabled {
    opacity: 0.3;
    cursor: default;
  }
</style>

<dialog class="page-viewer" aria-label="Page viewer">
  <img alt="">
  <div class="page-viewer-nav">
    <button type="button" class="page-prev" aria-label="Previous page">&#8249;</button>
    <span class="page-count"></span>
    <button type="button" class="page-next" aria-label="Next page">&#8250;</button>
  </div>
</dialog>

<script>
  (function () {
    var links = Array.prototype.slice.call(document.querySelectorAll('.page-grid a'));
    var viewer = document.querySelector('.page-viewer');
    if (!links.length || !viewer || !viewer.showModal) return;   // old browsers: links just open the image

    var img = viewer.querySelector('img');
    var count = viewer.querySelector('.page-count');
    var index = 0;

    function show(i) {
      index = Math.max(0, Math.min(links.length - 1, i));   // stop at the first and last page
      img.src = links[index].href;
      img.alt = links[index].querySelector('img').alt;
      count.textContent = (index + 1) + ' / ' + links.length;
      viewer.querySelector('.page-prev').disabled = index === 0;
      viewer.querySelector('.page-next').disabled = index === links.length - 1;
    }

    function close() {
      if (viewer.open) history.back();   // closing happens in the popstate handler below
    }

    links.forEach(function (a, i) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        show(i);
        viewer.showModal();
        document.documentElement.style.overflow = 'hidden';
        history.pushState({ pageViewer: true }, '');   // so the phone's Back button closes it too
      });
    });

    window.addEventListener('popstate', function () {
      if (viewer.open) {
        viewer.close();
        document.documentElement.style.overflow = '';
      }
    });

    viewer.addEventListener('click', function (e) { if (e.target === viewer) close(); });   // tap outside the page
    viewer.addEventListener('cancel', function (e) { e.preventDefault(); close(); });      // Escape key
    viewer.querySelector('.page-prev').addEventListener('click', function () { show(index - 1); });
    viewer.querySelector('.page-next').addEventListener('click', function () { show(index + 1); });
    document.addEventListener('keydown', function (e) {
      if (!viewer.open) return;
      if (e.key === 'ArrowLeft') show(index - 1);
      if (e.key === 'ArrowRight') show(index + 1);
    });

    // Swipe left or right to change page; ignored while pinch-zoomed in.
    var startX = null, startY = 0;
    viewer.addEventListener('touchstart', function (e) {
      var zoomed = window.visualViewport && window.visualViewport.scale > 1.01;
      if (e.touches.length === 1 && !zoomed) {
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
      } else {
        startX = null;
      }
    }, { passive: true });
    viewer.addEventListener('touchend', function (e) {
      if (startX === null) return;
      var dx = e.changedTouches[0].clientX - startX;
      var dy = e.changedTouches[0].clientY - startY;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) show(index + (dx < 0 ? 1 : -1));
      startX = null;
    });
  })();
</script>
