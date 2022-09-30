from src.GUI_Library.Frame_Class import FrameClass
from src.GUI_Library.System_Tray_Class import SystemTrayIcon
from src.GUI_Library.Icon_Class import IconClass
from src.GUI_Library.Menu_Class import MenuClass


from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication


class PyScreenUtilityDesigner(object):

    def setup_main(self, mainwindow):
        # MainWindow configuration
        mainwindow.set_name("Python_Overlay")
        mainwindow.set_window_title("Primary_Overlay")
        # self.set_size(500, 500)
        mainwindow.set_window_opacity(0.30)
        mainwindow.set_window_flag(Qt.FramelessWindowHint)
        mainwindow.set_focus_policy(Qt.StrongFocus)
        mainwindow.set_geometry(0, 0,
                          QApplication.primaryScreen().availableGeometry().width(),
                          QApplication.primaryScreen().availableGeometry().height())

        # Overlay region start
        self.frm_select_overlay = FrameClass(mainwindow,
                                             name="frm_select_overlay",
                                             style="QFrame {background-color: rgba(0,0,0,0); border: 2px solid rgba(255,0,0,255);}")
        self.frm_select_overlay.hide()
        # Overlay region end

        self.menu = MenuClass(None)
        # self.menu.set_new_action('Open Watch Screen', lambda: self.select_state('selection'))
        self.menu.set_new_separator()
        self.menu.set_new_action('Exit', mainwindow.__del__)

        # TODO: Change icon to a fitting design
        self.icn_tray = IconClass(
            "C:\\Users\\JBalat\\OneDrive - Analog Devices, Inc\\Desktop\\Project\\BCLT8585_GUI_208\\bclt8585-test-gui\\01_Src\\Firmware-Python-Framework\\APP\\GUI_images\\Analog_Devices_Blue_Logo.png")
        self.wdt_tray = SystemTrayIcon(None,
                                       name="wdt_tray",
                                       icon=self.icn_tray)
        self.wdt_tray.setContextMenu(self.menu)
        self.wdt_tray.add_tray_state("show", True, "PyScreenWatcher running in background", (None, None, None, None))
        self.wdt_tray.add_tray_state("hide", False, "", ("PyScreenWatcher",
                                                         "Section monitoring is halted.",
                                                         self.icn_tray, 3000))
        # self.wdt_tray.set_activation_reason_slots('double_click', lambda: self.select_state('selection'))