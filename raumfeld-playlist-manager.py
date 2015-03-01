#!/usr/bin/env python

import click
import time

from twisted.internet import reactor

from coherence.base import Coherence
from coherence.upnp.devices.control_point import ControlPoint
from coherence.upnp.devices.media_server_client import MediaServerClient
from coherence.upnp.core.utils import parse_xml
from coherence.upnp.core import DIDLLite
from coherence.extern.et import ET

MEDIA_SERVER_DEVICE_TYPE = 'urn:schemas-upnp-org:device:MediaServer:1'

def do_with_device(func):
    config = {'logmode': 'none'}
    coherence = Coherence(config)
    controlpoint = ControlPoint(coherence,auto_client=[])

    def device_found(device):
        device_type = device.get_device_type()
        if device_type == MEDIA_SERVER_DEVICE_TYPE:
            name = device.get_friendly_name()
            if name.startswith('Raumfeld'):
                print 'Found device', name
                func(device)

    coherence.connect(device_found, 'Coherence.UPnP.RootDevice.detection_completed')
    reactor.run()

def do_with_playlists(device, func):
    service = device.get_service_by_type('ContentDirectory')
    browse = service.get_action('Browse')
    d = browse.call(ObjectID='0/Playlists/MyPlaylists', BrowseFlag='BrowseDirectChildren', Filter='*', StartingIndex='0',
                    RequestedCount='0', SortCriteria='')
    def reply(response):
        xml = parse_xml(response['Result'], 'utf-8')
        elt = xml.getroot()
        for child in elt:
            #stored_didl_string = DIDLLite.element_to_didl(child)
            stored_didl_string = DIDLLite.element_to_didl(ET.tostring(child))
            didl = DIDLLite.DIDLElement.fromString(stored_didl_string)
            item = didl.getItems()[0]
            func(device, item)
    d.addCallback(reply)

@click.group()
def cli():
    pass

@cli.command()
def list_playlists():
    def print_playlist(device, item):
        print item.title, item.id
    do_with_device(lambda device: do_with_playlists(device, print_playlist))

@cli.command()
@click.argument('name')
def create(name):
    def create_playlist(device):
        service = device.get_service_by_type('ContentDirectory')
        browse = service.get_action('Browse')
        create_queue = service.get_action('CreateQueue')
        add_item = service.get_action('AddItemToQueue')

        def reply2(resp):
            d = browse.call(ObjectID='0/My Music/AllTracks', BrowseFlag='BrowseDirectChildren', Filter='*', StartingIndex='0',
                RequestedCount='3', SortCriteria='')

            def reply(response):
                xml = parse_xml(response['Result'], 'utf-8')
                elt = xml.getroot()
                for child in elt:
                    stored_didl_string = DIDLLite.element_to_didl(ET.tostring(child))
                    didl = DIDLLite.DIDLElement.fromString(stored_didl_string)
                    item = didl.getItems()[0]
                    print item.title, item.id
                    print item.__dict__
                    add_item.call(QueueID=resp['QueueID'], ObjectID=item.id, Position='-1')

            d.addCallback(reply)
            print resp

        d2 = create_queue.call(DesiredName=name, ContainerID='0/Playlists/MyPlaylists')
        d2.addCallback(reply2)
    do_with_device(create_playlist)

@cli.command()
@click.argument('name')
def delete(name):
    def delete_playlist(device, item):
        if name.lower() in item.title.lower():
            print 'Delete', item.title
            service = device.get_service_by_type('ContentDirectory')
            destroy = service.get_action('DestroyObject')
            destroy.call(ObjectID=item.id)

    do_with_device(lambda device: do_with_playlists(device, delete_playlist))


if __name__ == '__main__':
    cli()
