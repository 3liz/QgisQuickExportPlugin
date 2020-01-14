Quick Export - Export a vector layer to CSV, HTML, PDF or printer in 1 click
=============================================================================

This plugin has been developped by 3liz ( http://3liz.com )  .

    begin       : 2014-03-20
    copyright   : (C) 201 by 3liz
    authors     : René-Luc D'Hont and Michaël Douchin
    email       : info@3liz.com
    website     : http://www.3liz.com

Features
----------

Export tools
_____________

**Quick Export** adds a new toolbar in QGIS, with 4 actions to export any vector layer :

* **to CSV**: the exported file does not contains the geometries yet (may be a option in future versions). The delimiter can be set in the option dialog (comma, tab, semicolon or pipe).
* **to HTML**: the file can be opened in any browser, and displays the attribute table styled via CSS
* **to PDF**: the PDF contains the same table. It may be cut if too many fields are present in the attribute table. (a future version may correct this by dividing the table into pages when needed)
* **to default printer** : the PDF is generated in a temporary file, and the printer configuration dialog is opened. The user can select the printer and change the options.


Options dialog
________________

Some settings can be changed in the Options dialog, which can be opened via the fifth grey button [O] in the toolbar :

* General settings

  - Export hidden attributes : if checked, all the fields will be exported, even if marked as Hidden via the edit type option (fields tab of the vector layer properties dialog)

* CSV export

  - The delimiter can be chosen between tab, comma, pipe and semicolon


The Original Code is 3liz code.

Compatibility with old QGIS versions
------------------------------------

The current version is compatible with QGIS 3.x.

An old version of the plugin can be installed and used with QGIS 1.8 to 2.x.

In QGIS 1.8, some features are a bit different :

* **PDF export** : the attribute table is not divided into one table per page, because of a bug in the related version of the QT lib. The lines of the tables may be cut in half between pages.
* **Communication with the user** : the message bar is only available since QGIS 2.0. In QGIS 1.8, messages boxes (smal dialogs with buttons) are shown instead to warn the user or let him open the file after a successful export.
* **Performance** : the export is faster with QGIS 2.0, thanks to changes in the api.

Authors
-------

The Initial Developer of the Original Code is Michaël Douchin <mdouchin@3liz.com>. Portions created by the Initial Developer are Copyright (C) 2014 the Initial Developer. All Rights Reserved.

Funders
--------------

The plugin has been initially funded by the **Conseil Général des Pyrénées-Atlantiques** (France) : http://www.cg64.fr
