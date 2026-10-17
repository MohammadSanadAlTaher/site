---
layout: about
title: About Me
permalink: /about-me/
---

My name is Mohammad Sanad AlTaher (Sanad). I'm currently in my fourth year as a PhD student at [University of Nevada, Reno](https://unr.edu/) in electrical engineering, researching thermal management of RF devices. 

<div class="about-photo" markdown="0">
  <div class="about-links">
    <div style="font-size:20px">Click for:</div>
    <a href="/resume/">Résumé</a>
    <a href="https://www.linkedin.com/in/sanad-altaher/">LinkedIn</a>
    <a href="/papers/">Papers</a>
  </div>
  <figure>
    <img src="/assets/img/selfphoto26.jpg" alt="Sanad AlTaher" width="242px" style= "border-radius:12px; margin-left: auto; margin-right: auto;">
    <figcaption style="text-align: center; margin:8px; font-size: 14px; opacity: 0.6"><i>April, 2026, San Francisco.</i></figcaption>
  </figure>
</div>

I previously studied at [Oregon State University](https://oregonstate.edu/)
(Corvallis, Oregon), where I worked in the [Integrated Electronics](https://engineering.oregonstate.edu/EECS/research/integrated-electronics) research group, and focused on electromagnetics. At OSU, I completed three years and passed the qualifying exam for a PhD in electrical and computer engineering. However, I relocated to UNR to continue research with my advisor, [Prof. Tom Weller](https://www.unr.edu/engineering/about/deans-office/weller) and to utilize the UNR labs and facilities.

My current research centers on developing and testing novel passive RF devices (such as antennas, transmission lines, resonators, etc.) and thermal management approaches for them. Recently, I have worked on:
- Coplanar waveguides (CPWs) with non-intrusive temperature measurement.
- Planar antennas and waveguide probes for high-power testing of the CPWs.
- Active liquid cooling test-fixtures for high-power planar transmission lines.
<div class="section-gap"></div>

Before graduate studies, I obtained my bachelor’s degree in Electrical Engineering from 
[Jordan University of Science and Technology](https://www.just.edu.jo/Pages/Default.aspx), where I
graduated with a 3.92/4.0 CGPA, ranking 4<sup>th</sup> in a cohort of 78 students. Additionally, I specialized
in Telecommunications and ranked 1<sup>st</sup> in that track, around half of the EE cohort.

During my undergraduate studies, I gained international experience in entrepreneurship, 
academics, and research through the Hult Prize in Dubai (2019), an Erasmus+ exchange semester 
in Istanbul (2021), and a research internship in India (2022).

<div class="section-gap"></div>

I am mostly interested in electromagnetics, RF telecommunications, and applied physics. I hope to work on developing advanced technologies in those fields after finishing my PhD.


<style>
  .about-photo {
    display: grid;
    grid-template-columns: 1fr 242px 1fr;
    align-items: center;
    gap: 32px;
    margin: 32px 0;
  }

  .about-photo figure {
    grid-column: 2;
    grid-row: 1;
    margin: 0;
  }

  .about-links {
    grid-column: 1;
    grid-row: 1;
    justify-self: end;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 14px;
    font-size: 22px;
  }

  .section-gap {
    height: 12px;
  }

  @media (max-width: 400px) {
    .about-photo {
      grid-template-columns: 1fr;
      justify-items: center;
      gap: 16px;
    }
    .about-photo figure,
    .about-links {
      grid-column: 1;
      grid-row: auto;
    }
    .about-links {
      justify-self: center;
      flex-direction: row;
      flex-wrap: wrap;
      justify-content: center;
      gap: 6px 18px;
    }
  }
</style>