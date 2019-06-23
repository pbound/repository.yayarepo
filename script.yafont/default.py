# -*- coding: utf-8 -*-
# main import's 
import sys, os, re
import shutil
import xbmc, xbmcaddon, xbmcgui
from xml.dom import minidom

# Script constants

__addon__     = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__cwd__       = xbmc.translatePath(__addon__.getAddonInfo('path')).decode("utf-8")
__profile__   = xbmc.translatePath(__addon__.getAddonInfo('profile')).decode("utf-8")
__language__  = __addon__.getLocalizedString

# Shared resources
BASE_RESOURCE_PATH = os.path.join(__cwd__, 'resources', 'lib')
sys.path.append (BASE_RESOURCE_PATH)

def fixed_writexml(self, writer, indent="", addindent="", newl=""):
    # indent = current indentation
    # addindent = indentation to add to higher levels
    # newl = newline string
    writer.write(indent+"<" + self.tagName)

    attrs = self._get_attributes()
    a_names = attrs.keys()
    a_names.sort()

    for a_name in a_names:
        writer.write(" %s=\"" % a_name)
        minidom._write_data(writer, attrs[a_name].value)
        writer.write("\"")
    if self.childNodes:
        if len(self.childNodes) == 1 \
          and self.childNodes[0].nodeType == minidom.Node.TEXT_NODE:
            writer.write(">")
            self.childNodes[0].writexml(writer, "", "", "")
            writer.write("</%s>%s" % (self.tagName, newl))
            return
        writer.write(">%s"%(newl))
        for node in self.childNodes:
            if node.nodeType is not minidom.Node.TEXT_NODE:
                node.writexml(writer,indent+addindent,addindent,newl)
        writer.write("%s</%s>%s" % (indent,self.tagName,newl))
    else:
        writer.write("/>%s"%(newl))
# replace minidom's function with ours
minidom.Element.writexml = fixed_writexml

def getres(addonid):
    filepath = os.path.join(addonspath, addonid, 'addon.xml')
    doc = minidom.parse(filepath)
    root = doc.documentElement
    items = root.getElementsByTagName('extension')
    for item in items:
        point = item.getAttribute('point')
        if point == 'xbmc.gui.skin':
            ress = item.getElementsByTagName('res')
            list = []
            for res in ress:
                list.append(res.getAttribute('folder'))
            return list
    return []

def addfont(addonid, folder):
    filepath = os.path.join(addonspath, addonid, folder, 'Font.xml')
    doc = minidom.parse(filepath)
    root = doc.documentElement
    fontsets = root.getElementsByTagName('fontset')
    list = []
    arial_pos = None
    for i in range(0,len(fontsets)):
        id = fontsets[i].getAttribute('id')
        if id.lower() == 'arial':
            ret = xbmcgui.Dialog().yesno('Skin Font', 'Arial皮肤字体已存在。', '要重新生成Arial字体吗？')
            if not ret:
                return
            arial_pos = i
        list.append(id)
    sel = xbmcgui.Dialog().select('请选择参照字体(%s)' % (folder.encode('utf-8')), list)
    if sel < 0:
        return
    arial = fontsets[sel].cloneNode(True)
    arial.setAttribute("id","Arial")
    if arial.getAttribute("idloc") and sel != arial_pos:
        arial.removeAttribute("idloc")
    for node in arial.getElementsByTagName("filename"):
        newText = doc.createTextNode("arial.ttf")
        node.replaceChild(newText, node.firstChild)
    if arial_pos:
        root.removeChild(fontsets[arial_pos])
        del fontsets[arial_pos]
    root.appendChild(arial)
    f = open(filepath, 'w')
    doc.writexml(f, addindent="    ", newl="\n")
    f.close()
    xbmc.executebuiltin('Notification(%s,%s,%s)' % (__addonname__, 'Arial皮肤字体已生成(%s)' % (folder.encode('utf-8')), "1000")) 

addonspath = os.path.dirname(__cwd__)
# xbmcgui.Dialog().ok('profile', __profile__ )
spc = xbmc.translatePath("special://xbmc")
spcaddon = xbmc.translatePath("special://xbmcbinaddons")
_keybordpath = xbmc.translatePath('special://masterprofile/keyboardlayouts')
_home = xbmc.translatePath('special://home/media/Fonts')
# 'special://xbmc'
# xbmcgui.Dialog().textviewer('_masterprofile',_keybordpath)
# xbmcgui.Dialog().ok('_masterprofile',_keybordpath)
# xbmcgui.Dialog().ok('_home',_home)
addonlist = []
for addonid in os.listdir(addonspath):
    # xbmcgui.Dialog().ok('addonpa', addonid)

    if addonid[:4] == 'skin':
        addon = xbmcaddon.Addon(id=addonid)
        addonname = addon.getAddonInfo('name')
        skinpath = addon.getAddonInfo('path')
        # xbmcgui.Dialog().ok('skinpath', skinpath)
        addonlist.append((addonid, addonname, skinpath))

for addonid in os.listdir(spcaddon):
    # xbmcgui.Dialog().ok('addonpa', addonid)

    if addonid[:4] == 'skin':
        addon = xbmcaddon.Addon(id=addonid)
        addonname = addon.getAddonInfo('name')
        skinpath = addon.getAddonInfo('path')
        # xbmcgui.Dialog().ok('skinpath', skinpath)
        addonlist.append((addonid, addonname, skinpath))


list = [x[1] for x in addonlist]

if not list:
    xbmcgui.Dialog().ok('Skin Font', '未找到可用皮肤！')
else:
    sel = xbmcgui.Dialog().select('plese select skin', list)
    if sel != -1:

        addonid = addonlist[sel][0]
        skinpath= addonlist[sel][2]
        # xbmcgui.Dialog().ok('Skin ', addonid)
        # xbmcgui.Dialog().ok('addonpath', __cwd__)
        # xbmcgui.Dialog().ok('skinpath', skinpath)

        skin_font_path = os.path.join(skinpath, 'fonts')
        # xbmcgui.Dialog().ok('skinpath', skin_font_path)

        shutil.copy(__cwd__+'/arial.ttf', skin_font_path+'/arial.ttf')
        # shutil.copy(__cwd__ + '/arial.ttf', skin_font_path + '/arial.ttf')
        # shutil.copy(__cwd__ + '/arial.ttf', _home + '/arial.ttf')
        shutil.copy(__cwd__ + '/thai.xml', _keybordpath + '/thai.xml')
        # xbmcgui.Dialog.input('testinput',defaultt='dede',1)
        xbmc.Keyboard('test','teeet',).doModal()
        xbmcgui.Dialog().ok('finish','success')
        # kb = xbmc.Keyboard('default', 'heading')
        # kb.setDefault('Enter Search Word')
        # kb.setHeading( 'Search')
        # kb.setHiddenInput(False)
        # kb.doModal()

        # for folder in getres(addonid):
        #     xbmcgui.Dialog().ok('Skin folder ', folder)
        #     addfont(addonid, folder)
def addskinfont():
    shutil.copy(__cwd__ + '/arial.ttf', skin_font_path + '/arial.ttf')
    shutil.copy(__cwd__ + '/arial.ttf', _home + '/arial.ttf')
    shutil.copy(__cwd__ + '/arial.ttf', _keybordpath + '/arial.ttf')


if __name__ == '__main__':
    pass
    'C:\Users\Administrator\AppData\Roaming\Kodi\media\Fonts'
    'C:\Users\Administrator\AppData\Roaming\Kodi\userdata\keyboardlayouts'
    'C:\Users\Administrator\AppData\Roaming\Kodi\addons\skin.confluence\fonts'