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


addonspath = os.path.dirname(__cwd__)
# xbmcgui.Dialog().ok('profile', __profile__ )
__spc = xbmc.translatePath("special://xbmc")
__spcaddon = xbmc.translatePath("special://xbmcbinaddons")
__keybordpath = xbmc.translatePath('special://masterprofile/keyboardlayouts')
__home = xbmc.translatePath('special://home/media/Fonts')
# 'special://xbmc'
# xbmcgui.Dialog().textviewer('_masterprofile',_keybordpath)
# xbmcgui.Dialog().ok('_masterprofile',_keybordpath)
# xbmcgui.Dialog().ok('_home',_home)
# addonlist = []
# for addonid in os.listdir(addonspath):
#     # xbmcgui.Dialog().ok('addonpa', addonid)
#
#     if addonid[:4] == 'skin':
#         addon = xbmcaddon.Addon(id=addonid)
#         xbmcgui.Dialog().ok('addonpa', addonid)
#         addonname = addon.getAddonInfo('name')
#         skinpath = addon.getAddonInfo('path')
#         xbmcgui.Dialog().ok('skinpath', skinpath)
#         addonlist.append((addonid, addonname, skinpath))
#
# for addonid in os.listdir(spcaddon):
#     # xbmcgui.Dialog().ok('addonpa', addonid)
#
#     if addonid[:4] == 'skin':
#         addon = xbmcaddon.Addon(id=addonid)
#         addonname = addon.getAddonInfo('name')
#         skinpath = addon.getAddonInfo('path')
#         # xbmcgui.Dialog().ok('skinpath', skinpath)
#         addonlist.append((addonid, addonname, skinpath))
#
#
# list = [x[1] for x in addonlist]
#
# if not list:
#     xbmcgui.Dialog().ok('Skin Font', '未找到可用皮肤！')
# else:
#     sel = xbmcgui.Dialog().select('plese select skin', list)
#     if sel != -1:
#
#         addonid = addonlist[sel][0]
#         skinpath= addonlist[sel][2]
#         # xbmcgui.Dialog().ok('Skin ', addonid)
#         # xbmcgui.Dialog().ok('addonpath', __cwd__)
#         # xbmcgui.Dialog().ok('skinpath', skinpath)
#
#         skin_font_path = os.path.join(skinpath, 'fonts')
#         # xbmcgui.Dialog().ok('skinpath', skin_font_path)
#
#         shutil.copy(__cwd__+'/arial.ttf', skin_font_path+'/arial.ttf')
#         # shutil.copy(__cwd__ + '/arial.ttf', skin_font_path + '/arial.ttf')
#         # shutil.copy(__cwd__ + '/arial.ttf', _home + '/arial.ttf')
#         shutil.copy(__cwd__ + '/thai.xml', _keybordpath + '/thai.xml')
#         # xbmcgui.Dialog.input('testinput',defaultt='dede',1)
#         xbmc.Keyboard('test','teeet',).doModal()
#         xbmcgui.Dialog().ok('finish','success')
#         # kb = xbmc.Keyboard('default', 'heading')
#         # kb.setDefault('Enter Search Word')
#         # kb.setHeading( 'Search')
#         # kb.setHiddenInput(False)
#         # kb.doModal()
#
#         # for folder in getres(addonid):
#         #     xbmcgui.Dialog().ok('Skin folder ', folder)
#         #     addfont(addonid, folder)
def main():
    # xbmc.executebuiltin("ActivateWindow(10147)")
    # xbmcaddon.Addon(id='skin.confluence').openSettings()
    # xbmc.getSkinDir()
    # ActivateWindow(Settings)
    # xbmcgui.skin()
    # xbmcgui.Dialog().textviewer('_masterprofile', __keybordpath)
    # xbmcgui.Dialog().ok('specail',__spc)
    # xbmcgui.Dialog().ok('_home',__home)
    shutil.copy(__cwd__ + '/arial.ttf', __spc + '/media/Fonts/arial.ttf')
    # xbmcgui.Dialog().ok('finish', 'success')
    # xbmcgui.Dialog().ok('Sub font', ' Go to player Setting ->Langeuge -> font to use for the text, and refresh font to Arail ')
    # xbmc.executebuiltin("ActivateWindow(InterfaceSettings)",False)
    xbmcgui.Dialog().ok('Sub font',
                        ' Go to Interface Setting ->Skin -> font to use for the text, and refresh font to Arail ')
    xbmc.executebuiltin("ActivateWindowAndFocus(interfacesettings,-100,0,-5,0)")

    # xbmc.executebuiltin("ActivateWindow()")
    # a  =(xbmc.executebuiltin("ActivateWindowAndFocus(playersettings,-96,0,-71,0)"))
    # xbmc.sleep(20000)
    # xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
    # xbmcgui.Window(12000)
    # s = xbmcgui.getCurrentWindowDialogId()
    # xbmcgui.DialogBusyNoCancel
    # xbmcgui.Dialog().ok('_home', str(s))


    # xbmc.executebuiltin("ActivateWindow(interfacesettings)")
    # xbmc.executebuiltin("Action(Right)")
    # xbmc.executebuiltin("Action(Down)")
    # xbmc.executebuiltin("Action(Down)")
    # xbmc.executebuiltin("Action(Select)")
    # xbmc.executebuiltin("Action(Down)")
    # xbmc.executebuiltin("Action(Select)")
    # xbmc.executebuiltin("Dialog.Close(all,true)")

    # xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
    # xbmc.executebuiltin()
    # xbmcgui.Dialog().ok('Add font', ' Go to Setting -> -> font, and refresh font to Arail ')
    # xbmc.executebuiltin("ActivateWindow(PlayerSettings)",True)
    # shutil.copy(__cwd__ + '/arial.ttf', skin_font_path + '/arial.ttf')
    # shutil.copy(__cwd__ + '/arial.ttf', _home + '/arial.ttf')
    # shutil.copy(__cwd__ + '/arial.ttf', __spc + '/media/Fonts/thai.xml')

main()

if __name__ == '__main__':
    pass
    # 'C:\Users\Administrator\AppData\Roaming\Kodi\media\Fonts'
    # 'C:\Users\Administrator\AppData\Roaming\Kodi\userdata\keyboardlayouts'
    # 'C:\Users\Administrator\AppData\Roaming\Kodi\addons\skin.confluence\fonts'
    # 'C:\Program Files (x86)\Kodi\media\Fonts'
    # 'C:\Program Files (x86)\Kodi\media\Fonts'
