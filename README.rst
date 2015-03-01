=========================
Raumfeld Playlist Manager
=========================

Manage Playlists on the Raumfeld MediaServer (integrated in different Raumfeld speaker products).

Only tested with `Raumfeld Cube`_.

Uses the `Coherence Python UPnP framework`_.

Usage
=====

.. code-block::

    $ ./raumfeld-playlist-manager.py list
    $ ./raumfeld-playlist-manager.py create --artist 'My Favorite Artist' 'My New Playlist'

Debugging
=========

Install the `UPnP Inspector`_ to check your UPnP device and browse the MediaServer.

Installing the upnp-inspector package on Ubuntu:

.. code-block::

    $ sudo apt-get install upnp-inspector
    $ upnp-inspector


.. _Raumfeld Cube: http://www.teufelaudio.com/raumfeld-audio-streaming/raumfeld-stereo-cubes-p11468.html
.. _Coherence Python UPnP framework: http://coherence-project.org/
.. _UPnP Inspector: http://coherence.beebits.net/wiki/UPnP-Inspector

