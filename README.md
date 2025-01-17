<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">URSim for Docker</h3>

  <p align="center">
    A docker image for Universal Robots Simulator
    <br />
    <br />

</div>

<!-- ABOUT THE PROJECT -->
## About The Project

A docker image for URSim that uses x11vnc, xvfb, and noVNC.  The image provides a web based VNC server for connecting to the polyscope interface via a browser.

This is an alternative to the VMWare/VBox Image provided by Universal Robots.

![Alt text](demo/demo.gif?raw=true "Title")

**This repository is not associated with Universal Robots**

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

[Docker]((https://docs.docker.com/get-docker/)) is required to run this simulator

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/czagrzebski/URSimDocker.git
   ```
3. Enter the directory
   ```sh
    cd URSimDocker
   ```
4. Choose either the CB or eSeries model
   ```sh
   cd CB
   ```
   or

   ```sh
   cd eSeries
   ```
5. Build the image
   ```sh
   . build.bash
   ```
6. Run the image
   ```. run.bash
   ```
7. Open the web interface using the provided URL

**Note: You will need to create a docker volume for persistent storage of robot programs**





















<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/demo.png
