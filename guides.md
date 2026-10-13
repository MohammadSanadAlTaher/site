---
layout: articles
title: "Guides & More"
permalink: /misc/
---

Here, you'll find guides I prepared, my unpublished research, class projects, and other miscellaneous work. 

<!-- <h3 style="font-weight: lighter;">Projects</h3> -->

<!-- #### [CPW Antenna]({{ site.url }}{{ site.baseurl }}/guides/initialization)

#### [FDTD]({{ site.url }}{{ site.baseurl }}/guides/initialization)

#### [MoM Capacitance]({{ site.url }}{{ site.baseurl }}/guides/initialization)

#### [MoM Inductance]({{ site.url }}{{ site.baseurl }}/guides/Proteus) -->


<h3 style="font-weight: lighter;">Guides</h3>

#### [Website Initialization Guide]({{ site.url }}{{ site.baseurl }}/guides/initialization)

#### [Getting Started with Proteus 8]({{ site.url }}{{ site.baseurl }}/guides/Proteus)

<p>&nbsp;</p>
<p>&nbsp;</p>
----
<p>&nbsp;</p>
<p>&nbsp;</p>

{%for post in site.posts %}
{% if post.url contains 'guides' %}
<li><a href="{{site.baseurl}}{{post.url}}">{{post.title}}</a></li>
{% endif %}
{% endfor %}