---
layout: articles
title: "Tools"
permalink: /tools/
---

<!--- maybe add navigation pane on the side --->

Below are tools that I previously developed to help me with my research. Most of those tools were initially created as extensions for simulation programs, but I adapted them to become interactive web tools. If you wish to use them in the simulation programs, you can find a link to the Github repositiories as well.  

If you have any concerns, please [contact]({{ site.url }}{{ site.baseurl }}/contact/) me.

<p>&nbsp;</p>
----
<p>&nbsp;</p>

<div class="accordion accordion--toggle">
<div class="accordion__title"><h3 style="font-weight: bold;">Superformula Shapes</h3></div>

<div class="accordion__dropdown">
(GITHUB Repo Coming Soon)

<br>

<!-- <p style="text-align:center;">View below or <a href="{{site.url}}{{site.baseurl}}/assets/code_files/sf_r_loop.m">click here</a> to access the repository for the PyAEDT extension.
</p> -->

<div class="web-tool">
<iframe src="{{ '/webapps/sf_calc/sf_calc_gui.html' | relative_url }}"></iframe>
</div>

</div></div>


<p>&nbsp;</p>
----
<p>&nbsp;</p>

<div class="accordion">
  <div class="accordion__title"><h3 style="font-weight: bold;">Trace Similarity</h3></div>

<div class="accordion__dropdown">
(GITHUB Repo Coming Soon)

<br>

<!-- <p style="text-align:center;">View below or <a href="{{site.url}}{{site.baseurl}}/assets/code_files/sf_r_loop.m">click here</a> to access the repository for the PyAEDT extension.
</p> -->



<!-- <div class="web-tool">
<iframe src="{{ '/webapps/trace_similarity/trace_similarity_gui.html' | relative_url }}"></iframe>
</div> -->

</div></div>


<p>&nbsp;</p>
----
<p>&nbsp;</p>


<style>
.gui {
    background: transparent;
    font-size: 16px;
    font-family: monospace;
    word-wrap: break-word;
}
</style>

<script>
  document.addEventListener("DOMContentLoaded", () => {
    const accordions = document.querySelectorAll('.accordion');

    accordions.forEach(acc => {
      const title = acc.querySelector('.accordion__title');

      title.addEventListener('click', () => {
        accordions.forEach(other => {
          if (other !== acc) other.classList.remove('accordion--toggle');
        });

        acc.classList.toggle('accordion--toggle');
      });
    });
  });
</script>


<!---
### All Tools

{%for post in site.posts %}
{% if post.url contains 'course-resources' %}

* <a href="{{post.url}}">{{post.title}}</a><br>
{% endif %}
{% endfor %}
--->

  