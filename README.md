# Heben Odoo 13.0 CE

## Clone

`git clone --recurse-submodules --branch 13.0 https://github.com/calyx-servicios/heben.git`

## .conf File

This file is for reference of how is the `odoo.conf` addons path is configured in production.

## requirements.txt

This file has all the python packages using in production. It has the Odoo 14.0 dependencies as well.

Useful to create a new python environment.

Consider to add there if a module has new dependencies.

`pip3 install -r requirements.txt`
