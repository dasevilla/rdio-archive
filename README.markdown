Overview
========

New Release Archive for Rdio® downloads everything it can from the
`getNewReleases` API method and builds a static website to browse them.


Setup
=====

1. Clone the repository

        git clone git://github.com/dasevilla/rdio-archive.git
        cd rdio-archive/

2. Download the new releases for this week, last week, and two weeks ago

        make archive
    
3. Build the site

        make site
        cd _generated/


Resources
=========

* [Rdio Python client](https://github.com/rdio/rdio-python)

  Used to download the site

* [Pystache](https://github.com/defunkt/pystache)

  Used to generate the HTML

* [Bootstrap](http://twitter.github.com/bootstrap/)

  Used to style the HTML
