#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import subprocess

from locale import gettext as _tr

from Config import Config
from Performance import Performance


# Define class
class Disk:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/DiskTab.ui")

        # Get GUI objects
        self.grid1301 = builder.get_object('grid1301')
        self.drawingarea1301 = builder.get_object('drawingarea1301')
        self.drawingarea1302 = builder.get_object('drawingarea1302')
        self.button1301 = builder.get_object('button1301')
        self.label1301 = builder.get_object('label1301')
        self.label1302 = builder.get_object('label1302')
        self.label1303 = builder.get_object('label1303')
        self.label1304 = builder.get_object('label1304')
        self.label1305 = builder.get_object('label1305')
        self.label1306 = builder.get_object('label1306')
        self.label1307 = builder.get_object('label1307')
        self.label1308 = builder.get_object('label1308')
        self.label1309 = builder.get_object('label1309')
        self.label1310 = builder.get_object('label1310')
        self.label1311 = builder.get_object('label1311')
        self.label1313 = builder.get_object('label1313')
        self.eventbox1301 = builder.get_object('eventbox1301')

        # Connect GUI signals
        self.button1301.connect("clicked", self.on_button1301_clicked)
        self.drawingarea1301.connect("draw", self.on_drawingarea1301_draw)
        self.drawingarea1302.connect("draw", self.on_drawingarea1302_draw)
        self.eventbox1301.connect("button-press-event", self.on_eventbox1301_button_click_event)


    # ----------------------- "customizations menu" Button -----------------------
    def on_button1301_clicked(self, widget):

        from DiskMenu import DiskMenu
        DiskMenu.popover1301p.set_relative_to(widget)
        DiskMenu.popover1301p.set_position(1)
        DiskMenu.popover1301p.popup()


    # ----------------------- Called for opening Disk Details Window -----------------------
    def on_eventbox1301_button_click_event(self, widget, event):

        if event.button == 1:
            from DiskDetails import DiskDetails
            DiskDetails.window1301w.show()


    # ----------------------- Called for drawing Disk read/write speed as line chart -----------------------
    def on_drawingarea1301_draw(self, widget, ctx):

        chart_data_history = Config.chart_data_history
        chart_x_axis = list(range(0, chart_data_history))

        disk_read_speed = Performance.disk_read_speed[Performance.selected_disk_number]
        disk_write_speed = Performance.disk_write_speed[Performance.selected_disk_number]

        chart_line_color = Config.chart_line_color_disk_speed_usage
        chart_background_color = Config.chart_background_color_all_charts

        chart1301_width = Gtk.Widget.get_allocated_width(widget)
        chart1301_height = Gtk.Widget.get_allocated_height(widget)

        ctx.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
        ctx.rectangle(0, 0, chart1301_width, chart1301_height)
        ctx.fill()

        ctx.set_line_width(1)
        ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.25 * chart_line_color[3])
        for i in range(3):
            ctx.move_to(0, chart1301_height/4*(i+1))
            ctx.line_to(chart1301_width, chart1301_height/4*(i+1))
        for i in range(4):
            ctx.move_to(chart1301_width/5*(i+1), 0)
            ctx.line_to(chart1301_width/5*(i+1), chart1301_height)
        ctx.stroke()

        chart1301_y_limit = 1.1 * ((max(max(disk_read_speed), max(disk_write_speed))) + 0.0000001)
        if Config.plot_disk_read_speed == 1 and Config.plot_disk_write_speed == 0:
            chart1301_y_limit = 1.1 * (max(disk_read_speed) + 0.0000001)
        if Config.plot_disk_read_speed == 0 and Config.plot_disk_write_speed == 1:
            chart1301_y_limit = 1.1 * (max(disk_write_speed) + 0.0000001)

        # ---------- Start - This block of code is used in order to show maximum value of the chart as multiples of 1, 10, 100. ----------
        # Chart maximum value is shown as multiples of 1, 10, 100 (For example, 1, 2, 3, ..., 10, 20, 30, ..., 100, 200, 300, ...) in order to simplify the value and avoid misunderstandings of performance data and chart maximum values.
        # Chart maximum value is get as calculated value (instead of Bytes) and number of digits is calculated by using integer part of this value.
        # Next multiple value is calculated, data unit is appended as string and value is shown on a label.
        # "chart1301_y_limit" value is updated by using new (multiple) value.
        data_unit_for_chart_y_limit = 0
        if Config.performance_disk_speed_data_unit >= 8:
            data_unit_for_chart_y_limit = 8
        try:
            chart1301_y_limit_str = f'{self.performance_data_unit_converter_func(chart1301_y_limit, data_unit_for_chart_y_limit, 0)}/s'
        # try-except is used in order to prevent errors if first initial function is not finished and "performance_data_unit_converter_func" is not run.
        except AttributeError:
            return
        chart1301_y_limit_split = chart1301_y_limit_str.split(" ")
        chart1301_y_limit_float = float(chart1301_y_limit_split[0])
        number_of_digits = len(str(int(chart1301_y_limit_split[0])))
        multiple = 10 ** (number_of_digits - 1)
        # "0.0001" is used in order to take decimal part of the numbers into account. For example, 1.9999 (2-0.0001). This number is enough because maximum precision of the performance data is "3" (1.234 MiB/s).
        number_to_get_next_multiple = chart1301_y_limit_float + (multiple - 0.0001)
        next_multiple = int(number_to_get_next_multiple - (number_to_get_next_multiple % multiple))
        self.label1313.set_text(f'{next_multiple} {chart1301_y_limit_split[1]}')
        # "0.0000001"'s are used in order to avoid errors if values are tried to be divided by "0".
        chart1301_y_limit = (chart1301_y_limit * next_multiple / (chart1301_y_limit_float + 0.0000001) + 0.0000001)
        # ---------- End - This block of code is used in order to show maximum value of the chart as multiples of 1, 10, 100. ----------

        ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
        ctx.rectangle(0, 0, chart1301_width, chart1301_height)
        ctx.stroke()

        if Config.plot_disk_read_speed == 1:
            ctx.move_to(chart1301_width*chart_x_axis[0]/(chart_data_history-1), chart1301_height - chart1301_height*disk_read_speed[0]/chart1301_y_limit)
            for i in range(len(chart_x_axis) - 1):
                delta_x_chart1301a = (chart1301_width * chart_x_axis[i+1]/(chart_data_history-1)) - (chart1301_width * chart_x_axis[i]/(chart_data_history-1))
                delta_y_chart1301a = (chart1301_height*disk_read_speed[i+1]/chart1301_y_limit) - (chart1301_height*disk_read_speed[i]/chart1301_y_limit)
                ctx.rel_line_to(delta_x_chart1301a, -delta_y_chart1301a)

            ctx.rel_line_to(10, 0)
            ctx.rel_line_to(0, chart1301_height+10)
            ctx.rel_line_to(-(chart1301_width+20), 0)
            ctx.rel_line_to(0, -(chart1301_height+10))
            ctx.close_path()
            ctx.stroke()

        if Config.plot_disk_write_speed == 1:
            ctx.set_dash([3, 3])
            ctx.move_to(chart1301_width*chart_x_axis[0]/(chart_data_history-1), chart1301_height - chart1301_height*disk_write_speed[0]/chart1301_y_limit)
            for i in range(len(chart_x_axis) - 1):
                delta_x_chart1301b = (chart1301_width * chart_x_axis[i+1]/(chart_data_history-1)) - (chart1301_width * chart_x_axis[i]/(chart_data_history-1))
                delta_y_chart1301b = (chart1301_height*disk_write_speed[i+1]/chart1301_y_limit) - (chart1301_height*disk_write_speed[i]/chart1301_y_limit)
                ctx.rel_line_to(delta_x_chart1301b, -delta_y_chart1301b)

            ctx.rel_line_to(10, 0)
            ctx.rel_line_to(0, chart1301_height+10)
            ctx.rel_line_to(-(chart1301_width+20), 0)
            ctx.rel_line_to(0, -(chart1301_height+10))
            ctx.close_path()
            ctx.stroke()


    # ----------------------- Called for drawing Disk usage as bar chart -----------------------
    def on_drawingarea1302_draw(self, widget, ctx):

        try:
            disk_usage_percent_check = self.disk_usage_percent
        # "disk_usage_percent" value is get in this module and drawingarea may try to use this value before relevant function (which provides this value) is finished.
        except AttributeError:
            return

        chart_line_color = Config.chart_line_color_disk_speed_usage
        chart_background_color = Config.chart_background_color_all_charts


        chart1302_width = Gtk.Widget.get_allocated_width(widget)
        chart1302_height = Gtk.Widget.get_allocated_height(widget)

        ctx.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
        ctx.rectangle(0, 0, chart1302_width, chart1302_height)
        ctx.fill()

        ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.6 * chart_line_color[3])
        ctx.rectangle(0, 0, chart1302_width, chart1302_height)
        ctx.stroke()
        ctx.set_line_width(1)
        ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.3 * chart_line_color[3])
        ctx.rectangle(0, 0, chart1302_width*self.disk_usage_percent/100, chart1302_height)
        ctx.fill()


    # ----------------------------------- Disk - Initial Function -----------------------------------
    def disk_initial_func(self):

        # Define data unit conversion function objects in for lower CPU usage.
        self.performance_define_data_unit_converter_variables_func = Performance.performance_define_data_unit_converter_variables_func
        self.performance_data_unit_converter_func = Performance.performance_data_unit_converter_func

        # Define data unit conversion variables before they are used.
        self.performance_define_data_unit_converter_variables_func()

        disk_list = Performance.disk_list
        selected_disk_number = Performance.selected_disk_number
        selected_disk = disk_list[selected_disk_number]
        # Definition to access to this variable from "DiskDetails" module.
        self.selected_disk = selected_disk

        # Check if disk exists in the disk list and if disk directory exists in order to prevent errors when disk is removed suddenly when the same disk is selected on the GUI. This error occurs because foreground thread and background thread are different for performance monitoring. Tracking of disk list changes is performed by background thread and there may be a time difference between these two threads. This situtation may cause errors when viewed list is removed suddenly. There may be a better way for preventing these errors/fixing this problem.
        try:
            check_value = "/sys/class/block/" + selected_disk
        except Exception:
            return

        # Read pci.ids file. Some disks such as NVMe SSDs have "vendor" file with device id content. pci.ids file will be used for getting disk vendor name by using these ids.
        # Read "pci.ids" file if it is located in "/usr/share/misc/pci.ids" (for Debian-like systems) or in "/usr/share/hwdata/pci.ids" (systems other than Debian-like systems).
        try:
            with open("/usr/share/misc/pci.ids") as reader:
                self.pci_ids_output = reader.read()
        except FileNotFoundError:
            with open("/usr/share/hwdata/pci.ids") as reader:
                self.pci_ids_output = reader.read()


        # Get information.
        disk_type = self.disk_type_func(selected_disk)
        disk_parent_name = self.disk_parent_name_func(selected_disk, disk_type, disk_list)
        disk_vendor_model = self.disk_vendor_model_func(selected_disk, disk_type, disk_parent_name)
        disk_mount_point = self.disk_mount_point_func(selected_disk)
        if_system_disk = self.disk_if_system_disk_func(disk_mount_point)


        # Show information on labels.
        self.label1301.set_text(disk_vendor_model)
        self.label1302.set_text(f'{selected_disk} ({disk_type})')
        self.label1307.set_text(if_system_disk)

        self.initial_already_run = 1


    # ----------------------------------- Disk - Get Disk Data Function -----------------------------------
    def disk_loop_func(self):

        disk_list = Performance.disk_list
        selected_disk_number = Performance.selected_disk_number
        selected_disk = disk_list[selected_disk_number]
        disk_sector_size = Performance.disk_sector_size

        # Run "disk_initial_func" if selected disk is changed since the last loop.
        try:                                                                                      
            if self.selected_disk_prev != selected_disk:
                self.disk_initial_func()
        # try-except is used in order to avoid error if this is first loop of the function.
        except AttributeError:
            pass
        self.selected_disk_prev = selected_disk

        disk_read_speed = Performance.disk_read_speed
        disk_write_speed = Performance.disk_write_speed

        performance_disk_speed_data_precision = Config.performance_disk_speed_data_precision
        performance_disk_usage_data_precision = Config.performance_disk_usage_data_precision
        performance_disk_speed_data_unit = Config.performance_disk_speed_data_unit
        performance_disk_usage_data_unit = Config.performance_disk_usage_data_unit

        self.drawingarea1301.queue_draw()
        self.drawingarea1302.queue_draw()

        # Check if disk exists in the disk list and if disk directory exists in order to prevent errors when disk is removed suddenly when the same disk is selected on the GUI. This error occurs because foreground thread and background thread are different for performance monitoring. Tracking of disk list changes is performed by background thread and there may be a time difference between these two threads. This situtation may cause errors when viewed list is removed suddenly. There may be a better way for preventing these errors/fixing this problem.
        try:
            if os.path.isdir("/sys/class/block/" + selected_disk) == False:
                return
        except Exception:
            return

        # Get content of "/proc/mounts" file which is used by Disk and DiskDetails modules.
        with open("/proc/mounts") as reader:
            self.proc_mounts_output_lines = reader.read().strip().split("\n")


        # Get information.
        disk_read_time, disk_write_time = self.disk_read_write_time_func(selected_disk)
        disk_mount_point = self.disk_mount_point_func(selected_disk)
        disk_capacity, disk_size, disk_available, disk_free, disk_used, self.disk_usage_percent = self.disk_disk_capacity_size_available_free_used_usage_percent_func(disk_mount_point)


        # Show information on labels.
        self.label1303.set_text(f'{self.performance_data_unit_converter_func(disk_read_speed[selected_disk_number][-1], performance_disk_speed_data_unit, performance_disk_speed_data_precision)}/s')
        self.label1304.set_text(f'{self.performance_data_unit_converter_func(disk_write_speed[selected_disk_number][-1], performance_disk_speed_data_unit, performance_disk_speed_data_precision)}/s')
        self.label1305.set_text(f'{self.disk_time_unit_converter_func(disk_read_time)} ms')
        self.label1306.set_text(f'{self.disk_time_unit_converter_func(disk_write_time)} ms')
        if disk_mount_point != "-":
            self.label1308.set_text(f'{self.disk_usage_percent:.0f}%')
        if disk_mount_point == "-":
            self.label1308.set_text("-%")
        self.label1309.set_text(self.performance_data_unit_converter_func(disk_available, performance_disk_usage_data_unit, performance_disk_usage_data_precision))
        self.label1310.set_text(self.performance_data_unit_converter_func(disk_used, performance_disk_usage_data_unit, performance_disk_usage_data_precision))
        self.label1311.set_text(self.performance_data_unit_converter_func(disk_size, performance_disk_usage_data_unit, performance_disk_usage_data_precision))


    # ----------------------------------- Disk - Define Time Unit Converter Variables Function -----------------------------------
    def disk_time_unit_converter_func(self, time):

        w_r_time_days = time / 24 / 60 / 60 / 1000
        w_r_time_days_int = int(w_r_time_days)
        w_r_time_hours = (w_r_time_days - w_r_time_days_int) * 24
        w_r_time_hours_int = int(w_r_time_hours)
        w_r_time_minutes = (w_r_time_hours - w_r_time_hours_int) * 60
        w_r_time_minutes_int = int(w_r_time_minutes)
        w_r_time_seconds = (w_r_time_minutes - w_r_time_minutes_int) * 60
        w_r_time_seconds_int = int(w_r_time_seconds)
        w_r_time_milliseconds = (w_r_time_seconds - w_r_time_seconds_int) * 1000
        w_r_time_milliseconds_int = int(w_r_time_milliseconds)

        # Return time in the following format if time is less than 1 hour.
        if time < 3600000:
            return f'{w_r_time_minutes_int:02}:{w_r_time_seconds_int:02}.{w_r_time_milliseconds_int:03}'
        # Return time in the following format if time is more than 1 hour and less than 1 day.
        if time >= 3600000 and time < 86400000:
            return f'{w_r_time_hours_int:02}:{w_r_time_minutes_int:02}:{w_r_time_seconds_int:02}.{w_r_time_milliseconds_int:03}'
        # Return time in the following format if time is more than 1 day.
        if time >= 86400000:
            return f'{w_r_time_days_int:02}:{w_r_time_hours_int:02}:{w_r_time_minutes_int:02}.{w_r_time_seconds_int:02}:{w_r_time_milliseconds_int:03}'


    # ----------------------- Get disk type (Disk or Partition) -----------------------
    def disk_type_func(self, selected_disk):

        with open("/sys/class/block/" + selected_disk + "/uevent") as reader:
            sys_class_block_disk_uevent_lines = reader.read().split("\n")

        for line in sys_class_block_disk_uevent_lines:
            if "DEVTYPE" in line:
                disk_type = _tr(line.split("=")[1].capitalize())
                break

        return disk_type


    # ----------------------- Get disk parent name -----------------------
    def disk_parent_name_func(self, selected_disk, disk_type, disk_list):

        disk_parent_name = "-"
        if disk_type == _tr("Partition"):
            for check_disk_dir in disk_list:
                if os.path.isdir("/sys/class/block/" + check_disk_dir + "/" + selected_disk) == True:
                    disk_parent_name = check_disk_dir

        return disk_parent_name


    # ----------------------- Get disk vendor and model -----------------------
    def disk_vendor_model_func(self, selected_disk, disk_type, disk_parent_name):

        if disk_type == _tr("Disk"):
            disk_or_parent_disk_name = selected_disk
        if disk_type == _tr("Partition"):
            disk_or_parent_disk_name = disk_parent_name

        # Get disk vendor
        try:
            with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/vendor") as reader:
                disk_vendor = reader.read().strip()
            # Disk vendor information may be available as vendor id on some cases (such as on QEMU virtual machines).
            if disk_vendor.startswith("0x"):
                disk_vendor_id = "\n" + disk_vendor.split("x")[-1].strip() + "  "
                # "vendor" information may not be present in the pci.ids file.
                if disk_vendor_id in self.pci_ids_output:
                    # "1" in the ".split("[string", 1)" is used in order to split only the first instance in the whole text for faster split operation.
                    rest_of_the_pci_ids_output = self.pci_ids_output.split(disk_vendor_id, 1)[1]
                    disk_vendor = rest_of_the_pci_ids_output.split("\n", 1)[0].strip()
                if disk_vendor_id not in self.pci_ids_output:
                    disk_vendor = f'[{_tr("Unknown")}]'

        # Some disks such as NVMe SSDs do not have "vendor" file under "/sys/class/block/" + selected_disk + "/device" directory. They have this file under "/sys/class/block/" + selected_disk + "/device/device/vendor" directory.
        except FileNotFoundError:
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/device/vendor") as reader:
                    disk_vendor_id = "\n" + reader.read().strip().split("x")[-1] + "  "
                # "vendor" information may not be present in the pci.ids file.
                if disk_vendor_id in self.pci_ids_output:
                    rest_of_the_pci_ids_output = self.pci_ids_output.split(disk_vendor_id, 1)[1]
                    disk_vendor = rest_of_the_pci_ids_output.split("\n", 1)[0].strip()
                if disk_vendor_id not in self.pci_ids_output:
                    disk_vendor = f'[{_tr("Unknown")}]'
            except Exception:
                disk_vendor = f'[{_tr("Unknown")}]'

        # Get disk model
        try:
            with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/model") as reader:
                disk_model = reader.read().strip()
            # Disk model information may be available as model id on some cases (such as on QEMU virtual machines).
            if disk_model.startswith("0x"):
                disk_model_id = "\n\t" + disk_model.split("x")[-1] + "  "
                if disk_vendor != f'[{_tr("Unknown")}]':
                    # "device name" information may not be present in the pci.ids file.
                    if disk_model_id in rest_of_the_pci_ids_output:
                        rest_of_the_rest_of_the_pci_ids_output = rest_of_the_pci_ids_output.split(disk_model_id, 1)[1]
                        disk_model = rest_of_the_rest_of_the_pci_ids_output.split("\n", 1)[0].strip()
                    else:
                        disk_model = f'[{_tr("Unknown")}]'
                else:
                    disk_model = f'[{_tr("Unknown")}]'

        except Exception:
            disk_model = f'[{_tr("Unknown")}]'
        disk_vendor_model = disk_vendor + " - " +  disk_model

        # Get disk vendor and model if disk is loop device or swap disk.
        if selected_disk.startswith("loop"):
            disk_vendor_model = "[Loop Device]"
        if selected_disk.startswith("zram"):
            disk_vendor_model = _tr("[SWAP]")
        if selected_disk.startswith("mmcblk"):
            self.disk_mmc_cid_values_func()
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/manfid") as reader:
                    disk_vendor_manfid = reader.read().strip()
                disk_vendor = self.mmc_cid_values_dict[disk_vendor_manfid]
            except Exception:
                disk_vendor = "-"
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/name") as reader:
                    disk_name = reader.read().strip()
                disk_model = disk_name
            except FileNotFoundError:
                disk_model = "-"
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/type") as reader:
                    disk_card_type = reader.read().strip()
            except FileNotFoundError:
                disk_card_type = "-"
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/speed_class") as reader:
                    disk_card_speed_class = reader.read().strip()
            except FileNotFoundError:
                disk_card_speed_class = "-"
            disk_vendor_model = f'{disk_vendor} - {disk_model} ({disk_card_type} Card, Class {disk_card_speed_class})'

        return disk_vendor_model


    # ----------------------- Define register value dictionaries to get CPU information) -----------------------
    def disk_mmc_cid_values_func(self):

        # For more info about CIDs: https://www.kernel.org/doc/Documentation/mmc/mmc-dev-attrs.txt
        # Source: several sources and https://www.cameramemoryspeed.com/sd-memory-card-faq/reading-sd-card-cid-serial-psn-internal-numbers/
        self.mmc_cid_values_dict = {
                                    "0x000001": "Panasonic",
                                    "0x000002": "Toshiba",
                                    "0x000003": "SanDisk",
                                    "0x00001b": "Samsung",
                                    "0x00001d": "AData",
                                    "0x000027": "Phison",
                                    "0x000028": "Lexar",
                                    "0x000031": "Silicon Power",
                                    "0x000041": "Kingston",
                                    "0x000074": "Transcend",
                                    "0x000076": "Patriot",
                                    "0x000082": "Sony",
                                    "0x000027": "Sony"
                                    }


    # ----------------------- Get disk mount point -----------------------
    def disk_mount_point_func(self, selected_disk):

        with open("/proc/mounts") as reader:
            self.proc_mounts_output_lines = reader.read().strip().split("\n")

        disk_mount_point = "-"
        disk_mount_point_list_scratch = []
        for line in self.proc_mounts_output_lines:
            line_split = line.split()
            if line_split[0].split("/")[-1] == selected_disk:
                # String is decoded in order to convert string with escape characters such as "\\040" if they exist.
                disk_mount_point_list_scratch.append(bytes(line_split[1], "utf-8").decode("unicode_escape"))

        if len(disk_mount_point_list_scratch) == 1:
            disk_mount_point = disk_mount_point_list_scratch[0]

        # System disk is listed twice with different mountpoints on some systems (such as systems use btrfs filsystem or chroot). "/" mountpoint information is used.
        if len(disk_mount_point_list_scratch) > 1 and "/" in disk_mount_point_list_scratch:
            disk_mount_point = "/"

        return disk_mount_point


    # ----------------------- Get if system disk -----------------------
    def disk_if_system_disk_func(self, disk_mount_point):

        if disk_mount_point == "/":
            if_system_disk = _tr("Yes")
        else:
            if_system_disk = _tr("No")

        # System disk may not be detected by checking if mount point is "/" on some systems such as some ARM devices. "/dev/root" is the system disk name (symlink) in the "/proc/mounts" file on these systems.
        if if_system_disk == _tr("No"):
            for line in self.proc_mounts_output_lines:
                line_split = line.split(" ", 1)
                if line_split[0] == "dev/root":
                    with open("/proc/cmdline") as reader:
                        proc_cmdline = reader.read()
                    if "root=UUID=" in proc_cmdline:
                        disk_uuid_partuuid = proc_cmdline.split("root=UUID=", 1)[1].split(" ", 1)[0].strip()
                        system_disk = os.path.realpath("/dev/disk/by-uuid/" + disk_uuid_partuuid).split("/")[-1].strip()
                    if "root=PARTUUID=" in proc_cmdline:
                        disk_uuid_partuuid = proc_cmdline.split("root=PARTUUID=", 1)[1].split(" ", 1)[0].strip()
                        system_disk = os.path.realpath("/dev/disk/by-partuuid/" + disk_uuid_partuuid).split("/")[-1].strip()
                    if system_disk == selected_disk:
                        if_system_disk = _tr("Yes")

        return if_system_disk


    # ----------------------- Get disk file system -----------------------
    def disk_file_system_func(self, selected_disk):

        disk_file_system = _tr("[Not mounted]")
        for line in self.proc_mounts_output_lines:
            if line.split()[0].strip() == ("/dev/" + selected_disk):
                disk_file_system = line.split()[2].strip()
                break

        if disk_file_system == _tr("[Not mounted]"):
            # Show "[SWAP]" information for swap disks (if selected swap area is partition (not file))
            with open("/proc/swaps") as reader:
                proc_swaps_output_lines = reader.read().strip().split("\n")
            swap_disk_list = []
            for line in proc_swaps_output_lines:
                if line.split()[1].strip() == "partition":
                    swap_disk_list.append(line.split()[0].strip().split("/")[-1])
            if len(swap_disk_list) > 0 and selected_disk in swap_disk_list:
                disk_file_system = _tr("[SWAP]")

        # Try to get actual file system by using "lsblk" tool if file system has been get as "fuseblk" (this happens for USB drives). Because "/proc/mounts" file contains file system information as in user space. To be able to get the actual file system, root access is needed for reading from some files or "lsblk" tool could be used.
        if disk_file_system  == "fuseblk":
            try:
                disk_for_file_system = "/dev/" + selected_disk
                disk_file_system = (subprocess.check_output(["lsblk", "-no", "FSTYPE", disk_for_file_system], shell=False)).decode().strip()
            except Exception:
                pass

        return disk_file_system


    # ----------------------- Get disk read time and disk write time -----------------------
    def disk_read_write_time_func(self, selected_disk):

        with open("/proc/diskstats") as reader:
            proc_diskstats_lines = reader.read().strip().split("\n")

            for line in proc_diskstats_lines:
                if line.split()[2].strip() == selected_disk:
                    disk_read_time = int(line.split()[6])
                    disk_write_time = int(line.split()[10])

        return disk_read_time, disk_write_time


    # ----------------------- Get disk capacity, size, disk_available, disk_free, disk_used, disk_usage_percent -----------------------
    def disk_disk_capacity_size_available_free_used_usage_percent_func(self, disk_mount_point):

        if disk_mount_point != "-":
            # Values are calculated for filesystem size values (as df command does). lsblk command shows values of mass storage.
            statvfs_disk_usage_values = os.statvfs(disk_mount_point)
            fragment_size = statvfs_disk_usage_values.f_frsize
            disk_capacity = statvfs_disk_usage_values.f_blocks * fragment_size
            disk_size = statvfs_disk_usage_values.f_blocks * fragment_size
            disk_available = statvfs_disk_usage_values.f_bavail * fragment_size
            disk_free = statvfs_disk_usage_values.f_bfree * fragment_size
            disk_used = disk_size - disk_free
            # Gives same result with "lsblk" command
            #self.disk_usage_percent = disk_used / disk_size * 100
            # disk_usage_percent value is calculated as "used disk space / available disk space" in terms of filesystem values. This is real usage percent.
            self.disk_usage_percent = disk_used / (disk_available + disk_used) * 100

        if disk_mount_point == "-":
            disk_capacity = _tr("[Not mounted]")
            disk_size = _tr("[Not mounted]")
            disk_available = _tr("[Not mounted]")
            disk_free = _tr("[Not mounted]")
            disk_used = _tr("[Not mounted]")
            self.disk_usage_percent = 0

        return disk_capacity, disk_size, disk_available, disk_free, disk_used, self.disk_usage_percent


    # ----------------------- Get disk capacity (mass storage) -----------------------
    def disk_capacity_mass_storage_func(self, selected_disk, disk_mount_point, disk_sector_size):

        with open("/sys/class/block/" + selected_disk + "/size") as reader:
            disk_capacity_mass_storage = int(reader.read()) * disk_sector_size

        return disk_capacity_mass_storage


    # ----------------------- Get disk label -----------------------
    def disk_label_func(self, selected_disk):

        disk_label = "-"
        try:
            disk_label_list = os.listdir("/dev/disk/by-label/")
            for label in disk_label_list:
                if os.path.realpath("/dev/disk/by-label/" + label).split("/")[-1] == selected_disk:
                    # String is decoded in order to convert string with escape characters such as "\\040" if they exist.
                    disk_label = bytes(label, "utf-8").decode("unicode_escape")
        except FileNotFoundError:
            pass

        return disk_label


    # ----------------------- Get disk partition label -----------------------
    def disk_partition_label_func(self, selected_disk):

        disk_partition_label = "-"
        try:
            disk_partition_label_list = os.listdir("/dev/disk/by-partlabel/")
            for label in disk_partition_label_list:
                if os.path.realpath("/dev/disk/by-partlabel/" + label).split("/")[-1] == selected_disk:
                    disk_partition_label = label
        except FileNotFoundError:
            pass

        return disk_partition_label


    # ----------------------- Get disk path -----------------------
    def disk_path_func(self, selected_disk):

        disk_path = "-"
        if os.path.exists("/dev/" + selected_disk) == True:
            disk_path = "/dev/" + selected_disk

        return disk_path


    # ----------------------- Get disk revision -----------------------
    def disk_revision_func(self, selected_disk, disk_type):

        disk_revision = "-"
        if disk_type == _tr("Disk"):
            try:
                with open("/sys/class/block/" + selected_disk + "/device/rev") as reader:
                    disk_revision = reader.read().strip()
            except Exception:
                pass

        return disk_revision


    # ----------------------- Get disk serial number -----------------------
    def disk_serial_number_func(self, selected_disk, disk_type):

        disk_serial_number = "-"
        if disk_type == _tr("Disk"):
            disk_id_list = os.listdir("/dev/disk/by-id/")
            for id in disk_id_list:
                if os.path.realpath("/dev/disk/by-id/" + id).split("/")[-1] == selected_disk and ("/dev/disk/by-id/" + id).startswith("wwn-") == False:
                    disk_serial_number = id.split("-")[-1]
                    if "part" in disk_serial_number:
                        disk_serial_number = id.split("-")[-2]

        return disk_serial_number


    # ----------------------- Get disk UUID -----------------------
    def disk_uuid_func(self, selected_disk):

        disk_uuid = "-"
        try:
            disk_uuid_list = os.listdir("/dev/disk/by-uuid/")
            for uuid in disk_uuid_list:
                if os.path.realpath("/dev/disk/by-uuid/" + uuid).split("/")[-1] == selected_disk:
                    disk_uuid = uuid
        except FileNotFoundError:
            pass

        return disk_uuid


# Generate object
Disk = Disk()

