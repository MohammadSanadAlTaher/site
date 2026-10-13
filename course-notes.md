---
layout: articles
title: "Courses"
permalink: /courses/
---


My work in courses I have taken in the past. If you wish to refer to the documents, please note that they are not free from mistakes. 

If you have any concerns, please [contact]({{ site.url }}{{ site.baseurl }}/contact/) me.

<p>&nbsp;</p>
----
<p>&nbsp;</p>

<h3 style="font-weight: lighter;">5th Year EE Courses</h3>

#### EE575 Communication Networks:
* [Course Notes]({{ site.url }}{{ site.baseurl }}/course-resources/networks-notes)

#### EE558 Satellite Communication Systems:
* [Course Notes]({{ site.url }}{{ site.baseurl }}/course-resources/satellite-communication-systems)

#### EE555 Optical Fiber Communication Systems:
* [Course Notes]({{ site.url }}{{ site.baseurl }}/course-resources/optical-fibers-notes)

#### EE551 Digital Communications:
* [Equations]({{ site.url }}{{ site.baseurl }}/course-resources/EE551-equations)

#### EE524 RF Communication Circuits:
* [Course Notes]({{ site.url }}{{ site.baseurl }}/course-resources/rf-communication-circuits)

<p>&nbsp;</p>
----
<p>&nbsp;</p>

<h3 style="font-weight: lighter;">4th Year EE Courses</h3>

#### EE450 Communication Systems:
* [Course Notes]({{ site.url }}{{ site.baseurl }}/course-resources/communication-systems-notes)
  
* [Transforms]({{ site.url }}{{ site.baseurl }}/course-resources/Comm-Systems-Transforms)

#### EE420 Digital Electronic Circuits:
* [Course Notes]({{ site.url }}{{ site.baseurl }}/course-resources/digital-electronics)

#### EE407 Antennas and Radio Wave Propagation:
* [Equations]({{ site.url }}{{ site.baseurl }}/course-resources/EE407-equations)


<p>&nbsp;</p>
----
<p>&nbsp;</p>

<h3 style="font-weight: lighter;">3rd Year EE Courses</h3>


#### EE307 Electromagnetics II:
* [Course Notes]({{ site.url }}{{ site.baseurl }}/course-resources/electromagnetics2)

* [Equations]({{ site.url }}{{ site.baseurl }}/course-resources/EM2-equations)


#### EE305 Numerical Methods:
* [Course Notes]({{ site.url }}{{ site.baseurl }}/course-resources/Numerical-Methods-Notes)

* [Equations]({{ site.url }}{{ site.baseurl }}/course-resources/numericalmethodsequations)

<p>&nbsp;</p>
----
<p>&nbsp;</p>

### All Course Resources
{%for post in site.posts %}
{% if post.url contains 'course-resources' %}

* <a href="{{post.url}}">{{post.title}}</a><br>
{% endif %}
{% endfor %}


  