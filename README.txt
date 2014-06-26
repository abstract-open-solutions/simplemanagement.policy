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


OpenERP integration
===================

Simplemanagement provides a behaviour called 'IOrderNumber' that allow to insert
a specific order number to different content types.

This order number should be referenced to a real order number defined into OpenERP.


From Simplemanagement to OpenERP
---------------------------------

The join between Simplemanagement and OpenERP is performed by this view:

* openerp_order_redirect/<order number>

By calling the view with the parameter 'ordernumber' the user will be redirect
to OpenERP object with the same order number.


The Order number could be written in two forms:

1. a simple order number referenced to the default OpenERP database
2. a sequence of two strings separated by | (pipe) representing the OpenERP db and the order number eg.: snc|SO1110 or srl|SO22222

In the first case Simplemanagement will search for the order number in the default OpenERP database. In the second caso simplemanagement will search for a specific OpenERP database.

From OpenERP to Simplemanagement
--------------------------------

An openerp user could watch Simplemanagement's information about a specific
order by calling this view:

* openerp_view/<order number>

the user will be redirect to a specific content type that provides the order number
requested.




