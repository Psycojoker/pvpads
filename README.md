# Introduction

If you are in a situation where:

* you are in a group/association where you take your meetings notes (PV) in a pad (etherpad(-lite))
* you don't have any place to store this information
* meetings notes hang around with not place to be put, start to be lost, aren't visible or easily findable

Then PVPADs is a tool for you and your group/association. It is a very simple
website where you put a pad URL and a date (and more stuff if needed) and
PVPADs will store the pad contents and renders it in html and list it
chronologically so everything is at the same place and everyone can reads it easily.

PVPADs is also multi organisations, meaning that you can handle several
organisations on the same instance and filter organisations based on the URL.

# Usage

Go to <code>/admin</code>, create and organisation, the start adding meetings for it.

# Technical details

PVPADs is a standard python/django website, the only difference is that you can
add this django command in a crontab if you want to regulary update the content
of the stored pads (otherwise it is only fetched once):

    python manage.py update_pads

PVPADs works with etherpad-lite and the old java etherpad.

PVPADs supports those kind of renderers (for translating the pad content into html):

* etherpad (meaning that PVPADs will use etherpad(-lite) html export feature)
* markdown
* mediawiki

PVPADs is XSS safe, the html is cleaned using
[Bleach](https://bleach.readthedocs.org/en/latest/) from Mozilla.

# Licence

AGPLv3+
