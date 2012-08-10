.. contents::

Introduction
============
This package implements some Plone configurations in order
to make the development of Plone sites easier.

It will hide from the contextual menu some views usually useless for end-users like:
 - Thumbnail view
 - All content view
 - Tabular view

It will remove some Content Types from 'add' menu:
 - Link
 - Event
 - News Item

It remove the possibility to add some portlets:
 - Calendar portlet
 - Classic portlet
 - News portlet
 - Events portlet
 - Recent portlet
 - Review portlet

Workflow
--------
This 'reset' package also provides a 'two state workflow' and set it as the default content workflow.

This workflow is similar to default Plone workflow
(Simple Publication Workflow) without:
* pending state
* submit transition
* reject transition

Versioning
----------
Abstract policy configures a custom policy for contents versioning
In setuphandlers we limit the defaul number of versions per content stored
in portal_history and, eventually we can remove all versioning policies.

Decomment this line to remove default versioning policies::

    >>> disable_cmfedition_versioning(site)


More dependencies
-----------------

This package also depends on some "most wanted" add-ons, so that you don't need to remember to add them to the buildout, like:
- collective.portletpage
- collective.contentleadimage
- collective.quickupload
- collective.oembed
- collective.js.oembed

Installation
============

You can install this package with zc.buildout:

    [instance]
    eggs =
        simplemanagement.policy

Before you include this package in a buildout environment you have to uncomment the right dependencies in setup.py and metadata.xml files:


      # -*- loadcontent requirements: -*-
      'plone.app.transmogrifier',
      'transmogrify.dexterity',
      # -*- suggested requirements: -*-
      'collective.portletpage',
      'collective.contentleadimage',
      'collective.quickupload',
      'collective.oembed',
      'collective.js.oembed',



Development environment
=======================
Abstract policy package contains a special profile useful to create a development environment.

To enable this profile configure your buildout in this way:

    [instance]
    eggs =
      ...
      simplemanagement.policy [development]

After re-run buildout you will find a new profile portal_setup tool
called: Abstract Policy (Development)


This profile installs:
 * collective.loremipsum

