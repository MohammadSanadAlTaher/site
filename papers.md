---
layout: articles
title: "Papers"
permalink: /papers/
---

Published work.

<h3 style="font-weight: lighter;">2026:</h3>

#### [Immersion Cooling Fixture for High Power Testing of Planar Microwave Transmission Lines]({{ site.url }}{{ site.baseurl }}/MjAyNi1FUEVQUy1wYXBlcg)
[**M. Sanad AlTaher**]({{ site.url }}{{ site.baseurl }}/about-me),
[Thomas Weller](https://ieeexplore.ieee.org/author/37274715300)

<h3 style="font-weight: lighter;">2025:</h3>


#### [Direct Contact Liquid Cooling for Thermal Management of Printed Coplanar Waveguide Lines](https://ieeexplore.ieee.org/document/11134055)
[Omer Faruk Firat](https://ieeexplore.ieee.org/author/37086916379),
[**M. Sanad AlTaher**]({{ site.url }}{{ site.baseurl }}/about-me),
[Joshua Gess](https://ieeexplore.ieee.org/author/37085529069),
[Thomas Weller](https://ieeexplore.ieee.org/author/37274715300)


<h3 style="font-weight: lighter;">2024:</h3>

#### [Design and Simulation of Square Aperture Multi-hole Legendre Waveguide Directional Couplers](https://link.springer.com/article/10.1007/s40998-023-00688-5)
[**Mohammad Sanad AlTaher**]({{ site.url }}{{ site.baseurl }}/about-me),
[Nihad Dib](https://www.just.edu.jo/eportfolio/Pages/Default.aspx?email=nihad),


{%for post in site.posts %}
{% if post.url contains 'paper' %}
<li><a href="{{site.url}}{{post.url}}">{{post.title}}</a></li>
{% endif %}
{% endfor %}