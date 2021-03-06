#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ***********************IMPORTANT NMAP LICENSE TERMS************************
# *                                                                         *
# * The Nmap Security Scanner is (C) 1996-2011 Insecure.Com LLC. Nmap is    *
# * also a registered trademark of Insecure.Com LLC.  This program is free  *
# * software; you may redistribute and/or modify it under the terms of the  *
# * GNU General Public License as published by the Free Software            *
# * Foundation; Version 2 with the clarifications and exceptions described  *
# * below.  This guarantees your right to use, modify, and redistribute     *
# * this software under certain conditions.  If you wish to embed Nmap      *
# * technology into proprietary software, we sell alternative licenses      *
# * (contact sales@insecure.com).  Dozens of software vendors already       *
# * license Nmap technology such as host discovery, port scanning, OS       *
# * detection, and version detection.                                       *
# *                                                                         *
# * Note that the GPL places important restrictions on "derived works", yet *
# * it does not provide a detailed definition of that term.  To avoid       *
# * misunderstandings, we consider an application to constitute a           *
# * "derivative work" for the purpose of this license if it does any of the *
# * following:                                                              *
# * o Integrates source code from Nmap                                      *
# * o Reads or includes Nmap copyrighted data files, such as                *
# *   nmap-os-db or nmap-service-probes.                                    *
# * o Executes Nmap and parses the results (as opposed to typical shell or  *
# *   execution-menu apps, which simply display raw Nmap output and so are  *
# *   not derivative works.)                                                *
# * o Integrates/includes/aggregates Nmap into a proprietary executable     *
# *   installer, such as those produced by InstallShield.                   *
# * o Links to a library or executes a program that does any of the above   *
# *                                                                         *
# * The term "Nmap" should be taken to also include any portions or derived *
# * works of Nmap.  This list is not exclusive, but is meant to clarify our *
# * interpretation of derived works with some common examples.  Our         *
# * interpretation applies only to Nmap--we don't speak for other people's  *
# * GPL works.                                                              *
# *                                                                         *
# * If you have any questions about the GPL licensing restrictions on using *
# * Nmap in non-GPL works, we would be happy to help.  As mentioned above,  *
# * we also offer alternative license to integrate Nmap into proprietary    *
# * applications and appliances.  These contracts have been sold to dozens  *
# * of software vendors, and generally include a perpetual license as well  *
# * as providing for priority support and updates as well as helping to     *
# * fund the continued development of Nmap technology.  Please email        *
# * sales@insecure.com for further information.                             *
# *                                                                         *
# * As a special exception to the GPL terms, Insecure.Com LLC grants        *
# * permission to link the code of this program with any version of the     *
# * OpenSSL library which is distributed under a license identical to that  *
# * listed in the included docs/licenses/OpenSSL.txt file, and distribute   *
# * linked combinations including the two. You must obey the GNU GPL in all *
# * respects for all of the code used other than OpenSSL.  If you modify    *
# * this file, you may extend this exception to your version of the file,   *
# * but you are not obligated to do so.                                     *
# *                                                                         *
# * If you received these files with a written license agreement or         *
# * contract stating terms other than the terms above, then that            *
# * alternative license agreement takes precedence over these comments.     *
# *                                                                         *
# * Source is provided to this software because we believe users have a     *
# * right to know exactly what a program is going to do before they run it. *
# * This also allows you to audit the software for security holes (none     *
# * have been found so far).                                                *
# *                                                                         *
# * Source code also allows you to port Nmap to new platforms, fix bugs,    *
# * and add new features.  You are highly encouraged to send your changes   *
# * to nmap-dev@insecure.org for possible incorporation into the main       *
# * distribution.  By sending these changes to Fyodor or one of the         *
# * Insecure.Org development mailing lists, it is assumed that you are      *
# * offering the Nmap Project (Insecure.Com LLC) the unlimited,             *
# * non-exclusive right to reuse, modify, and relicense the code.  Nmap     *
# * will always be available Open Source, but this is important because the *
# * inability to relicense code has caused devastating problems for other   *
# * Free Software projects (such as KDE and NASM).  We also occasionally    *
# * relicense the code to third parties as discussed above.  If you wish to *
# * specify special license conditions of your contributions, just say so   *
# * when you send them.                                                     *
# *                                                                         *
# * This program is distributed in the hope that it will be useful, but     *
# * WITHOUT ANY WARRANTY; without even the implied warranty of              *
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU       *
# * General Public License v2.0 for more details at                         *
# * http://www.gnu.org/licenses/gpl-2.0.html , or in the COPYING file       *
# * included with Nmap.                                                     *
# *                                                                         *
# ***************************************************************************/

import os.path
import sys
import gtk

import zenmapCore.I18N

RESPONSE_OPEN_DIRECTORY = 1

class AllFilesFileFilter(gtk.FileFilter):
    def __init__(self):
        gtk.FileFilter.__init__(self)

        pattern = "*"
        self.add_pattern(pattern)
        self.set_name(_("All files (%s)") % pattern)

class ResultsFileFilter(gtk.FileFilter):
    def __init__(self):
        gtk.FileFilter.__init__(self)

        patterns = ["*.xml"]
        for pattern in patterns:
            self.add_pattern(pattern)
        self.set_name(_("Nmap XML files (%s)") % ", ".join(patterns))

class ScriptFileFilter(gtk.FileFilter):
    def __init__(self):
        gtk.FileFilter.__init__(self)

        patterns = ["*.nse"]
        for pattern in patterns:
            self.add_pattern(pattern)
        self.set_name(_("NSE scripts (%s)") % ", ".join(patterns))

class UnicodeFileChooserDialog(gtk.FileChooserDialog):
    """This is a base class for file choosers. It is designed to ease the
    retrieval of Unicode file names. On most platforms, the file names returned
    are encoded in the encoding given by sys.getfilesystemencoding(). On
    Windows, they are returned in UTF-8, even though using the UTF-8 file name
    results in a file not found error. The get_filename method of this class
    handles the decoding automatically."""
    def get_filename(self):
        filename = gtk.FileChooserDialog.get_filename(self)
        if sys.platform == "win32":
            encoding = "UTF-8"
        else:
            encoding = sys.getfilesystemencoding() or "UTF-8"
        try:
            filename = filename.decode(encoding)
        except:
            pass
        return filename

class AllFilesFileChooserDialog(UnicodeFileChooserDialog):
    def __init__(self, title="", parent=None,
                 action=gtk.FILE_CHOOSER_ACTION_OPEN,
                 buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                          gtk.STOCK_OPEN, gtk.RESPONSE_OK), backend=None):

        gtk.FileChooserDialog.__init__(self, title, parent,
                                       action, buttons)
        self.set_default_response(gtk.RESPONSE_OK)
        self.add_filter(AllFilesFileFilter())

class ResultsFileSingleChooserDialog(UnicodeFileChooserDialog):
    """This results file choose only allows the selection of single files, not
    directories."""
    def __init__(self, title="", parent=None,
                 action=gtk.FILE_CHOOSER_ACTION_OPEN,
                 buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                          gtk.STOCK_OPEN, gtk.RESPONSE_OK), backend=None):

        UnicodeFileChooserDialog.__init__(self, title, parent,
                                       action, buttons)
        self.set_default_response(gtk.RESPONSE_OK)
        for f in (ResultsFileFilter(), AllFilesFileFilter()):
            self.add_filter(f)

class ResultsFileChooserDialog(UnicodeFileChooserDialog):
    def __init__(self, title="", parent=None,
                 action=gtk.FILE_CHOOSER_ACTION_OPEN,
                 buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                          "Open Directory", RESPONSE_OPEN_DIRECTORY,
                          gtk.STOCK_OPEN, gtk.RESPONSE_OK), backend=None):

        UnicodeFileChooserDialog.__init__(self, title, parent,
                                       action, buttons)
        self.set_default_response(gtk.RESPONSE_OK)
        for f in (ResultsFileFilter(), AllFilesFileFilter()):
            self.add_filter(f)

class ScriptFileChooserDialog(UnicodeFileChooserDialog):
    def __init__(self, title="", parent=None,
                 action=gtk.FILE_CHOOSER_ACTION_OPEN,
                 buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                          gtk.STOCK_OPEN, gtk.RESPONSE_OK), backend=None):

        UnicodeFileChooserDialog.__init__(self, title, parent,
                                       action, buttons)
        self.set_default_response(gtk.RESPONSE_OK)
        self.set_select_multiple(True)
        for f in (ScriptFileFilter(), AllFilesFileFilter()):
            self.add_filter(f)

class SaveResultsFileChooserDialog(UnicodeFileChooserDialog):
    TYPES = (
        (_("By extension"), None, None),
        (_("Nmap XML format (.xml)"), "xml", ".xml"),
        (_("Nmap text format (.nmap)"), "text", ".nmap"),
    )
    # For the "By Extension" choice.
    EXTENSIONS = {
        ".xml": "xml",
        ".nmap": "text",
        ".txt": "text",
    }

    def __init__(self, title="", parent=None,
                 action=gtk.FILE_CHOOSER_ACTION_SAVE,
                 buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                          gtk.STOCK_SAVE, gtk.RESPONSE_OK), backend=None):

        UnicodeFileChooserDialog.__init__(self, title, parent, action, buttons)

        types_store = gtk.ListStore(str, str, str)
        for type in self.TYPES:
            types_store.append(type)

        self.combo = gtk.ComboBox(types_store)
        cell = gtk.CellRendererText()
        self.combo.pack_start(cell, True)
        self.combo.add_attribute(cell, "text", 0)
        self.combo.connect("changed", self.combo_changed_cb)
        self.combo.set_active(1)

        hbox = gtk.HBox(False, 6)
        hbox.pack_end(self.combo, False)
        hbox.pack_end(gtk.Label(_("Select File Type:")), False)
        hbox.show_all()

        self.set_extra_widget(hbox)
        self.set_do_overwrite_confirmation(True)

        self.set_default_response(gtk.RESPONSE_OK)

    def combo_changed_cb(self, combo):
        filename = self.get_filename() or ""
        dir, basename = os.path.split(filename)
        if dir != self.get_current_folder():
            self.set_current_folder(dir)

        # Find the recommended extension.
        new_ext = combo.get_model().get_value(combo.get_active_iter(), 2)
        if new_ext is not None:
            # Change the filename to use the recommended extension.
            root, ext = os.path.splitext(basename)
            if len(ext) == 0 and root.startswith("."):
                root = ""
            self.set_current_name(root + new_ext)

    def get_extension(self):
        return os.path.splitext(self.get_filename())[1]

    def get_format(self):
        """Get the save format the user has chosen. It is a string, either
        "text" or "xml"."""
        filetype = self.combo.get_model().get_value(self.combo.get_active_iter(), 1)
        if filetype is None:
            # Guess based on extension. "xml" is the default if unknown.
            return self.EXTENSIONS.get(self.get_extension(), "xml")
        return filetype

class DirectoryChooserDialog(UnicodeFileChooserDialog):
    def __init__(self, title="", parent=None,
                 action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                 buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                          gtk.STOCK_OPEN, gtk.RESPONSE_OK), backend=None):

        UnicodeFileChooserDialog.__init__(self, title, parent, action, buttons)
        self.set_default_response(gtk.RESPONSE_OK)

class SaveToDirectoryChooserDialog(UnicodeFileChooserDialog):
    def __init__(self, title="", parent=None,
                 action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                 buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                          gtk.STOCK_SAVE, gtk.RESPONSE_OK), backend=None):

        UnicodeFileChooserDialog.__init__(self, title, parent, action, buttons)
        self.set_default_response(gtk.RESPONSE_OK)
