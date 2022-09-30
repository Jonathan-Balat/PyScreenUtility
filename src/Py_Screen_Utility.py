# importing the required libraries
from pyautogui import screenshot
from time import time, strftime, localtime

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication

from sys import exit

# Custom Library Imports
from src.GUI_Library.Main_Window_Class import MainWindowClass
from src.GUI_Library.Timer_Class import TimerClass
from src.GUI_Custom_Library.Box_Class import BoxClass
from src.Py_Screen_Utility_Designer import PyScreenUtilityDesigner

from src.File_Manager_Class import FileManagerClass
from src.Notification_Class import NotificationManagerClass


class PyScreenUtility(MainWindowClass):

    def __init__(self):
        super(PyScreenUtility, self).__init__()

        self.version = "1.0.0.0"

        self.designer = PyScreenUtilityDesigner()
        self.designer.setup_main(self)

        # GUI Flags
        self.b_mouse_left_pressed = False
        self.b_mouse_right_pressed = False
        self.b_mouse_dragged = False

        # Event variables
        self.mouse_old_pos  = None
        self.min_threshold  = 5
        self.new_width      = 0
        self.new_height     = 0
        self.new_bounds     = (0, 0, 0, 0)
        self.box_dict       = {}
        self.drawn_box_dict = {}

        self.reference_image_dict = {}

        # TODO: Research screen management to:
        #       - Determine absolute sizes of each available screens
        #       - Be able to expand Screen watching to all or specific screens. WARNING: pyautogui may not support this
        # print(QApplication.screens())
        # for screen in QApplication.screens():
        #     print(screen.availableGeometry())
        #     print(screen.devicePixelRatio())

        # Class Instantiations
        self.__file_man = FileManagerClass()
        self.__notif_man = NotificationManagerClass()

        # Timer Instantiations
        self.__create_timers()

        # Program defaults/init states
        self.select_state('selection')

        # show all the widgets
        self.show()

    def __del__(self):
        self.__close_timers()
        self.designer.wdt_tray.hide()
        self.close()

    ####################  TIMERS  ####################
    def __create_timers(self):
        self.overlay_timer = TimerClass(timer_type=0)
        self.overlay_timer.set_timeout_connect(self.__draw_boxes_loop)

        self.monitoring_timer = TimerClass(timer_type=0)
        self.monitoring_timer.set_timeout_connect(self.__validate_images_loop)

    def __close_timers(self):
        self.overlay_timer.stop_timer()
        self.monitoring_timer.stop_timer()

    ####################  TRAY/WINDOW METHODS  ####################
    def show_window_event(self, b_flag=True):
        self.set_visible(b_flag)
        self.designer.wdt_tray.change_tray_state("hide" if b_flag else "show")

    def app_tray_icon(self, b_flag):
        self.set_visible(not b_flag)
        self.designer.wdt_tray.change_tray_state("show" if b_flag else "hide")

    ####################  MOUSE/KEYBOARD EVENTS  ####################
    def keyPressEvent(self, event):
        # TODO:
        #   - Add pause button by using Pause/Break key on keyboard
        if event.key() == Qt.Key_Escape:
            self.__del__()
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.select_state('monitoring')

    def mousePressEvent(self, event):
        position = (event.x(), event.y())

        if event.button() == Qt.LeftButton:
            self.b_mouse_left_pressed = True
            self.mouse_old_pos = position

        if event.button() == Qt.RightButton:
            self.b_mouse_right_pressed = True

            # Checks if user clicked inside the box(es)
            # geo indices = 0,1,2,3 -> x,y,w,h
            valid_list = list(filter(lambda geo: (geo[0] < position[0] < geo[0]+geo[2]) and
                                                 (geo[1] < position[1] < geo[1]+geo[3]), self.box_dict.values()))
            self.remove_box_event(valid_list)

            self.b_mouse_right_pressed = False

    def mouseMoveEvent(self, event):
        if self.b_mouse_left_pressed:
            # Note: This causes a warning on console when dragging between windows.
            x, y = self.mouse_old_pos
            dx = abs(event.x() - x)
            dy = abs(event.y() - y)

            if self.min_threshold < dx or self.min_threshold < dy:
                self.designer.frm_select_overlay.show()

                # This relocates starting point to upper left corner if mouse drag is done in reverse
                start_x = x - dx if event.x() < x else x
                start_y = y - dy if event.y() < y else y

                self.designer.frm_select_overlay.setGeometry(start_x, start_y, dx, dy)

                self.new_bounds = (start_x, start_y, dx, dy)
                self.b_mouse_dragged = True

    def mouseReleaseEvent(self, event):
        if self.b_mouse_dragged:
            if self.new_bounds not in self.box_dict.values():
                self.box_dict[self.box_dict.__len__()+1] = self.new_bounds
            self.new_bounds = (0, 0, 0, 0)  # This gets updated in mouseMoveEvent

        self.designer.frm_select_overlay.hide()
        
        self.b_mouse_left_pressed = False
        self.b_mouse_dragged = False

    def __draw_boxes_loop(self):
        if not self.b_mouse_right_pressed:
            for label, geo in self.box_dict.items():

                # NOTE: Guard added to avoid redrawing previous boxes
                if label not in self.drawn_box_dict:
                    self.drawn_box_dict[label] = BoxClass(self,
                                                          "Box_"+str(label),
                                                          geo,
                                                          "QFrame {background-color: rgba(0,0,0,0);"
                                                          "border: 2px solid rgba(0,0,0,255);}",
                                                          True)

    def remove_box_event(self, remove_list):
        # Cross check in dictionary and remove selected box(es)

        # NOTE: box_dict content structure -> {box_idx: (x,y,w,h), ...}
        # Searches index from values list using geom tuple (x,y,w,h)
        for box in remove_list:
            idx = list(self.box_dict.values()).index(box)
            box = list(self.box_dict)[idx]
            _ = self.box_dict.pop(box)

        # Reindex remaining boxes
        self.box_dict = {idx + 1: box_geo for idx, (_, box_geo) in enumerate(self.box_dict.items())}

        # Clear the drawn box dictionary
        # NOTE: Used temporary to avoid temp_list to change in size during iteration
        temp_list = list(self.drawn_box_dict.items())
        for frame_lbl, frame_widget in temp_list:
            frame_widget.hide()
            frame_widget.deleteLater()
            _ = self.drawn_box_dict.pop(frame_lbl)
            
    ####################  STATE MANAGEMENT  ####################
    def select_state(self, state):
        state_func = self.__states_dict.get(state)
        if state_func is not None:
            state_func(self)

    def __state_selection(self):
        # STATE - Select areas
        self.monitoring_timer.stop_timer()
        self.overlay_timer.start_timer()

        self.show_window_event(True)
        print("STATE: Selection")

    def __state_monitoring(self):
        # STATE - Monitor areas
        self.show_window_event(False)

        self.__capture_event()  # Creates first image used as reference

        self.overlay_timer.stop_timer()
        self.monitoring_timer.start_timer(1000)
        print("STATE: Monitoring")

    __states_dict = {
        "selection":    __state_selection,
        "monitoring":   __state_monitoring,
    }

    ####################  OTHER METHODS  ####################
    def __capture_event(self):
        instance_str = self.__file_man.get_session_instance()
        self.__file_man.create_directory(instance_str)

        # Creates image used as new reference
        self.__capture_screenshot(instance_str)

        return instance_str

    def __capture_screenshot(self, instance_directory):
        """ This function should be called everytime there is a change in the selected sections of screen """

        sshot = screenshot()
        sshot.save(instance_directory + "/MAIN.png")

        self.reference_image_dict = {}
        for label, (x, y, w, h) in self.box_dict.items():
            self.reference_image_dict[label] = sshot.crop((x, y, x+w, y+h))
            self.reference_image_dict[label].save(instance_directory + "/" + str(label) + strftime("_%b_%d_%H_%M_%S", localtime(time())) + ".png")

    def __validate_images_loop(self):
        sshot = screenshot()
        sshot_crop = sshot.crop
        ref_dict = self.reference_image_dict

        changed_list = []
        for label, (x, y, w, h) in self.box_dict.items():
            # Checks if change exists
            if ref_dict[label] != sshot_crop((x, y, x+w, y+h)):
                changed_list.append(label)

        if changed_list:
            instance_str = self.__capture_event()

            # Create file_name and Content for log_file
            file_name = self.__create_log_file_name('/log_file.txt')
            content = self.__create_log_content(instance_str, changed_list)

            # Save log of changes
            self.__file_man.save_txt_file(file_name, content=content)

            # Enable Buzzer alert or flashing
            self.__notif_man.alert_audio()

    def __create_log_file_name(self, file_name):
        return self.__file_man.get_directory() + file_name

    @staticmethod
    def __create_log_content(instance_str, changed_list):
        content_str = ['\n\n' + instance_str + ' Changes:\n']
        for item in changed_list.copy():
            content_str.append("\tBox #" + str(item))
        return content_str


if __name__ == "__main__":
    # create pyqt5 app
    App = QApplication()

    # create the instance of our PyScreenUtility
    window = PyScreenUtility()

    # start the app
    exit(App.exec_())
