#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog

# Compatible import for pymodbus 2.x and 3.x
try:
    # pymodbus 3.x
    from pymodbus.client import ModbusClient
except ImportError:
    # fallback for older 2.x versions
    from pymodbus.client.sync import ModbusSerialClient as ModbusClient

param_dict = {
    51: {"param_num": 0, "name": "Line Volts", "unit": None, "scale": 1,
         "map": {0: "High", 1: "Low", 2: "Auto"}},
    52: {"param_num": 1, "name": "Speed #1", "unit": "Hz", "scale": 100},
    53: {"param_num": 2, "name": "Speed #2", "unit": "Hz", "scale": 100},
    54: {"param_num": 3, "name": "Speed #3", "unit": "Hz", "scale": 100},
    55: {"param_num": 4, "name": "Speed #4", "unit": "Hz", "scale": 100},
    56: {"param_num": 5, "name": "Skip Freq #1", "unit": "Hz", "scale": 100},
    57: {"param_num": 6, "name": "Skip Freq #2", "unit": "Hz", "scale": 100},
    58: {"param_num": 7, "name": "Band Width", "unit": "Hz", "scale": 100},
    59: {"param_num": 8, "name": "Acceleration", "unit": "sec", "scale": 10},
    60: {"param_num": 9, "name": "Deceleration", "unit": "sec", "scale": 10},
    61: {"param_num": 10, "name": "Minimum Frequency", "unit": "Hz", "scale": 100},
    62: {"param_num": 11, "name": "Maximum Frequency", "unit": "Hz", "scale": 100},
    63: {"param_num": 12, "name": "DC Brake Voltage", "unit": "VDC", "scale": 1},
    64: {"param_num": 13, "name": "DC Brake Time", "unit": "sec", "scale": 10},
    65: {"param_num": 14, "name": "Dynamic Brake", "unit": None, "scale": 1,
         "map": {0: "Off", 1: "On"}},
    66: {"param_num": 15, "name": "Reserved", "unit": None, "scale": 1},
    67: {"param_num": 16, "name": "Current Limit", "unit": "%", "scale": 1},
    68: {"param_num": 17, "name": "Motor Overload", "unit": "%", "scale": 1},
    69: {"param_num": 18, "name": "Base Frequency", "unit": "Hz", "scale": 100},
    70: {"param_num": 19, "name": "Flux Boost", "unit": "%", "scale": 100},
    71: {"param_num": 20, "name": "AC Boost", "unit": "%", "scale": 100},
    72: {"param_num": 21, "name": "Slip Compensation", "unit": "%", "scale": 100},
    73: {"param_num": 22, "name": "Torque Mode", "unit": None, "scale": 1,
         "map": {0: "Constant", 1: "Variable", 2: "CT/NOCMP"}},

    74: {"param_num": 23, "name": "Carrier Frequency", "unit": "kHz", "scale": 1,
         "map": {0: "2.5 kHz", 1: "6 kHz", 2: "8 kHz",
                 3: "10 kHz", 4: "12 kHz", 5: "14 kHz"}},

    75: {"param_num": 24, "name": "Reserved", "unit": None, "scale": 1},
    76: {"param_num": 25, "name": "Start Mode", "unit": None, "scale": 1,
         "map": {0: "Normal", 1: "Power-Up", 2: "Auto Restart", 3: "Re-Brake"}},

    77: {"param_num": 26, "name": "Stop Mode", "unit": None, "scale": 1,
         "map": {0: "Ramp", 1: "Coast"}},

    78: {"param_num": 27, "name": "Rotation", "unit": None, "scale": 1,
         "map": {0: "Forward", 1: "Reverse", 2: "FWD & REV", 3: "FWD@LOC"}},

    79: {"param_num": 28, "name": "Auto/Manual", "unit": None, "scale": 1,
         "map": {0: "Both", 1: "Auto", 2: "Manual"}},

    80: {"param_num": 29, "name": "Manual Source", "unit": None, "scale": 1,
         "map": {0: "Keypad", 1: "0–10 VDC"}},

    81: {"param_num": 30, "name": "Control Mode", "unit": None, "scale": 1,
         "map": {0: "Local", 1: "Remote", 2: "Both", 3: "Keypad",
                 4: "TB Strip", 5: "Keypad 2"}},

    82: {"param_num": 31, "name": "Hz Units", "unit": None, "scale": 1,
         "map": {0: "Hertz", 1: "RPM", 2: "% Hz", 3: "/SEC", 4: "/MIN", 5: "/HR",
                 6: "GPH", 7: "None", 8: "%", 9: "PSI", 10: "FPM", 11: "CFM",
                 12: "GPM", 13: "IN", 14: "FT", 15: "/SEC", 16: "/MIN",
                 17: "/HR", 18: "F", 19: "C", 20: "MPM", 21: "GPH"}},
    83: {"param_num": 32, "name": "Hz Multiplier", "unit": None, "scale": 100},
    84: {"param_num": 33, "name": "Speed Display DP", "unit": None, "scale": 1,
         "map": {0: "XXXXX", 1: "XXX.X", 2: "XX.XX", 3: "X.XXX", 4: ".XXXX"}},
    85: {"param_num": 34, "name": "Load Multiplier", "unit": "%", "scale": 1},
    86: {"param_num": 35, "name": "Display Contrast", "unit": None, "scale": 1},
    87: {"param_num": 36, "name": "Sleep Threshold", "unit": "Hz", "scale": 100},
    88: {"param_num": 37, "name": "Sleep Delay", "unit": "Hz", "scale": 10},
    89: {"param_num": 38, "name": "Sleep Bandwidth", "unit": None, "scale": 1},
    90: {"param_num": 39, "name": "TB5 Min", "unit": "Hz", "scale": 100},
    91: {"param_num": 40, "name": "TB5 Max", "unit": "Hz", "scale": 100},
    92: {"param_num": 41, "name": "Analog In Filter", "unit": "sec", "scale": 100},
    93: {"param_num": 42, "name": "TB10A Output", "unit": None, "scale": 1},
    94: {"param_num": 43, "name": "@TB10A Freq", "unit": "Hz", "scale": 100},
    95: {"param_num": 44, "name": "TB10B Output", "unit": None, "scale": 1},
    96: {"param_num": 45, "name": "@TB10B %", "unit": "%", "scale": 1},
    97: {"param_num": 46, "name": "Reserved", "unit": None, "scale": 1},
    98: {"param_num": 47, "name": "TB13A Input", "unit": None, "scale": 1},
    99: {"param_num": 48, "name": "TB13B Input", "unit": None, "scale": 1},
    100: {"param_num": 49, "name": "TB13C Input", "unit": None, "scale": 1},
    101: {"param_num": 50, "name": "TB13D Input", "unit": None, "scale": 1},
    102: {"param_num": 51, "name": "Reserved", "unit": None, "scale": 1},
    103: {"param_num": 52, "name": "TB14 Output", "unit": None, "scale": 1},
    104: {"param_num": 53, "name": "TB15 Output", "unit": None, "scale": 1},
    105: {"param_num": 54, "name": "Relay Output", "unit": None, "scale": 1},
    106: {"param_num": 55, "name": "TB5B Loss Action", "unit": None, "scale": 1},
    107: {"param_num": 56, "name": "Reserved", "unit": None, "scale": 1},
    108: {"param_num": 57, "name": "Serial Link", "unit": None, "scale": 1},
    109: {"param_num": 58, "name": "Drive Address", "unit": None, "scale": 1},
    110: {"param_num": 59, "name": "Reserved", "unit": None, "scale": 1},
    111: {"param_num": 60, "name": "Reserved", "unit": None, "scale": 1},
    112: {"param_num": 61, "name": "Password", "unit": None, "scale": 1},
    113: {"param_num": 62, "name": "Reserved", "unit": None, "scale": 1},
    114: {"param_num": 63, "name": "Software Version", "unit": None, "scale": 1,
          "map": {21263: "M108315"}},
    115: {"param_num": 64, "name": "Monitor Enable", "unit": None, "scale": 1},
    116: {"param_num": 65, "name": "Program Reset", "unit": None, "scale": 1},
    117: {"param_num": 66, "name": "History Reset", "unit": None, "scale": 1},
    118: {"param_num": 67, "name": "Reserved", "unit": None, "scale": 1},
    119: {"param_num": 68, "name": "Reserved", "unit": None, "scale": 1},
    120: {"param_num": 69, "name": "Language", "unit": None, "scale": 1},
    121: {"param_num": 70, "name": "PID Mode", "unit": None, "scale": 1},
    122: {"param_num": 71, "name": "Reserved", "unit": None, "scale": 1},
    123: {"param_num": 72, "name": "Reserved", "unit": None, "scale": 1},
    124: {"param_num": 73, "name": "Reserved", "unit": None, "scale": 1},
    125: {"param_num": 74, "name": "PID Feedback Source", "unit": None, "scale": 1},
    126: {"param_num": 75, "name": "PID FB @ MIN", "unit": "%", "scale": 1},
    127: {"param_num": 76, "name": "PID FB @ MAX", "unit": "%", "scale": 1},
    128: {"param_num": 77, "name": "Reserved", "unit": None, "scale": 1},
    129: {"param_num": 78, "name": "PID I Gain", "unit": "sec", "scale": 10},
    130: {"param_num": 79, "name": "PID D Gain", "unit": "sec", "scale": 10},
    131: {"param_num": 80, "name": "PID Accel", "unit": "sec", "scale": 10},
    132: {"param_num": 81, "name": "PID Min Alarm", "unit": "%", "scale": 1},
    133: {"param_num": 82, "name": "PID Max Alarm", "unit": "%", "scale": 1},
    # 134–150 are mostly reserved or view-only (software/fault history)
}
# Factory default register values (raw Modbus representation)
factory_defaults = {
    51: 2,  # Line Volts → Auto
    52: 2000,  # Speed #1 = 20.00 Hz
    53: 2000,  # Speed #2 = 20.00 Hz
    54: 2000,  # Speed #3 = 20.00 Hz
    55: 2000,  # Speed #4 = 20.00 Hz
    56: 0,  # Skip #1
    57: 0,  # Skip #2
    58: 100,  # Bandwidth
    59: 300,  # Accel = 30.0 sec (scale=10)
    60: 300,  # Decel = 30.0 sec (scale=10)
    61: 50,  # Min Freq = 0.50 Hz
    62: 6000,  # Max Freq = 60.00 Hz
    63: 0,  # DC Brake Voltage = 0
    64: 0,  # DC Brake Time = 0.0 sec
    65: 0,  # Dynamic Brake = Disabled
    67: 180,  # Current Limit = 180 %
    68: 100,  # Motor Overload = 100 %
    69: 6000,  # Base Frequency = 60.00 Hz
    70: 100,  # Flux Boost = 1.00 %
    71: 0,  # AC Boost = 0
    72: 0,  # Slip Compensation = 0
    74: 0,  # Carrier Freq = 2.5 kHz (default)
    76: 0,  # Start Mode = Normal
    77: 1,  # Stop Mode = Coast
    78: 0,  # Rotation = Forward
    79: 0,  # Auto/Manual = Both
    80: 0,  # Manual Source = Keypad
    81: 0,  # Control = Local
    82: 0,  # Units = Hertz
    83: 100,  # Hz Multiplier = 1.00
    84: 0,  # Speed Display Format = XXXXX
    85: 100,  # Load Multiplier = 100 %
    87: 0,  # Sleep Threshold = 0.00 Hz
    88: 3000,  # Sleep Delay = 30.00 hz
    89: 0,  # Sleep Bandwidth = 0
    90: 0,  # TB5 Min = 0 (.00 Hz)
    91: 0,  # TB5 Max = 0 (.00 Hz)
    92: 2,  # Analog In Filter = 0.02 sec (raw 2, scale .01 sec)
    93: 0,  # TB10A Output = 00 -> None
    94: 6000,  # @TB10A Freq = 60.00 Hz (raw 6000)
    95: 0,  # TB10B Output = 00 -> None
    96: 125,  # @TB10B % = 125 (%) (raw 125)
    98: 0,  # TB13A Input = 00 -> None
    99: 0,  # TB13B Input = 00 -> None
    100: 0,  # TB13C Input = 00 -> None
    101: 0,  # TB13D Input = 00 -> EXT Fault (default)
    103: 0,  # TB14 Output = 00 -> None
    104: 0,  # TB15 Output = 00 -> None
    105: 0,  # Relay Output = 00 -> None
    106: 0,  # TB5B Loss Action = 00 -> Fault
    108: 2,  # SERIAL = 00 -> Enabled w/o Timer (normally is 0 =disabled but keeping serial at 2 since we are
    # using it lol)
    109: 30,  # ADDRESS = 30 (factory example in manual)
    112: 19,  # PASSWORD = 0019 (raw 19)
    115: 1,  # MONITOR = 01 -> ON
    125: 0,  # PID Feedback Source = 00 -> TB-5A (default)
    130: 0,  # PID D Gain = 0.0 sec (raw 0)
    150: 0,  # LANGUAGE = 0 -> English (default)
}


# --- MC1000 minimal terminal GUI ---
class MCConsole:
    def __init__(self, root):
        self.root = root
        root.title("MC1000 Terminal")

        self.client = None

        # --- Connection frame ---
        conn_frame = ttk.Frame(root)
        conn_frame.pack(padx=5, pady=5, fill="x")

        ttk.Label(conn_frame, text="Port:").pack(side="left")
        self.port_var = tk.StringVar(value="COM6")
        ttk.Entry(conn_frame, textvariable=self.port_var, width=8).pack(side="left", padx=2)

        ttk.Label(conn_frame, text="Slave:").pack(side="left")
        self.slave_var = tk.IntVar(value=30)
        ttk.Entry(conn_frame, textvariable=self.slave_var, width=4).pack(side="left", padx=2)

        self.conn_btn = ttk.Button(conn_frame, text="Connect", command=self.connect)
        self.conn_btn.pack(side="left", padx=2)
        self.disc_btn = ttk.Button(conn_frame, text="Disconnect", command=self.disconnect, state="disabled")
        self.disc_btn.pack(side="left", padx=2)

        # --- Terminal output ---
        self.terminal = scrolledtext.ScrolledText(root, width=80, height=20)
        self.terminal.pack(padx=5, pady=5)
        self.terminal.insert("end", "MC1000 Terminal Ready\n")

        # --- Command entry ---
        cmd_frame = ttk.Frame(root)
        cmd_frame.pack(fill="x", padx=5, pady=5)

        self.cmd_var = tk.StringVar()
        self.cmd_entry = ttk.Entry(cmd_frame, textvariable=self.cmd_var)
        self.cmd_entry.pack(side="left", fill="x", expand=True, padx=2)
        self.cmd_entry.bind("<Return>", self.process_command)

        ttk.Button(cmd_frame, text="Send", command=self.process_command).pack(side="left", padx=2)

        # --- Quick controls ---
        ctrl_frame = ttk.Frame(root)
        ctrl_frame.pack(padx=5, pady=5, fill="x")

        ttk.Button(ctrl_frame, text="Unlock (0)", command=lambda: self.write_register(48, 0)).pack(side="left", padx=2)
        ttk.Button(ctrl_frame, text="Unlock All (1475)", command=lambda: self.write_register(48, 1475)).pack(
            side="left", padx=2)
        ttk.Button(ctrl_frame, text="Start", command=lambda: self.write_register(1, 0x0008)).pack(side="left", padx=2)
        ttk.Button(ctrl_frame, text="Stop", command=lambda: self.write_register(1, 0x0004)).pack(side="left", padx=2)
        ttk.Button(ctrl_frame, text="Forward", command=lambda: self.write_register(1, 0x0080)).pack(side="left", padx=2)
        ttk.Button(ctrl_frame, text="Reverse", command=lambda: self.write_register(1, 0x0040)).pack(side="left", padx=2)

        # --- Quick parameter read buttons ---
        param_frame = ttk.LabelFrame(root, text="Quick Read Parameters")
        param_frame.pack(padx=5, pady=5, fill="x")

        # (Label, register, optional count)
        self.quick_params = [
            ("Status Block (24..29)", 24, 6),
            ("Speed (40)", 40, 1),
            ("Line Volts (51)", 51, 1),
            ("Accel (59)", 59, 1, 0.1),  # scale 0.1 → 300 becomes 30.0
            ("Decel (60)", 60, 1, 0.1),
            ("Min Freq (61)", 61, 1, 0.01),
        ]

        for param in self.quick_params:
            label_text = param[0]
            reg = param[1]
            count = param[2]
            scale = param[3] if len(param) > 3 else 1.0

            def make_callback(r=reg, c=count, l=label_text, s=scale):
                return lambda: self.read_register(r, count=c, label=l, scale=s)

            ttk.Button(param_frame, text=label_text, command=make_callback()).pack(side="left", padx=2, pady=2)

        # --- Add this inside MCConsole.__init__ after Quick Parameter buttons ---

        # --- Parameter selection frame ---
        sel_frame = ttk.LabelFrame(root, text="Read Parameter")
        sel_frame.pack(padx=5, pady=5, fill="x")

        # Combobox for parameters
        self.param_names = []
        self.param_lookup = {}  # map display string -> register

        for reg, meta in param_dict.items():
            display = f"{meta['param_num']:02d} - {meta['name']}"
            self.param_names.append(display)
            self.param_lookup[display] = reg

        self.param_var = tk.StringVar()
        self.param_combo = ttk.Combobox(sel_frame, textvariable=self.param_var, values=self.param_names,
                                        state="readonly")
        self.param_combo.pack(side="left", padx=5, pady=5, fill="x", expand=True)

        # Entry for formatted value
        self.param_value_var = tk.StringVar()
        self.param_value_entry = ttk.Entry(sel_frame, textvariable=self.param_value_var, width=12)
        self.param_value_entry.pack(side="left", padx=5)

        # Unit label
        self.param_unit_var = tk.StringVar(value="")
        self.param_unit_label = ttk.Label(sel_frame, textvariable=self.param_unit_var, width=6)
        self.param_unit_label.pack(side="left", padx=5)

        self.param_combo.bind("<<ComboboxSelected>>", self.read_selected_param)

        ttk.Button(sel_frame, text="Write", command=self.write_selected_param).pack(side="left", padx=5)

        # --- Bulk parameter upload/download ---
        bulk_frame = ttk.LabelFrame(root, text="Bulk Parameters")
        bulk_frame.pack(padx=5, pady=5, fill="x")

        ttk.Button(bulk_frame, text="Upload", command=self.upload_params).pack(side="left", padx=5,
                                                                               pady=5)
        ttk.Button(bulk_frame, text="Download", command=self.download_params).pack(side="left", padx=5,
                                                                                   pady=5)

        ttk.Button(bulk_frame, text="Factory Defaults", command=self.send_factory_defaults).pack(side="left", padx=5,
                                                                                                 pady=5)

    def send_factory_defaults(self):
        if not self.client:
            self.log("Not connected")
            return
        slave = self.slave_var.get()
        count = 0
        for reg, raw_val in factory_defaults.items():
            try:
                rr = self.client.write_register(reg, raw_val, unit=slave)
                if rr.isError():
                    self.log(f"Write error on {reg}")
                else:
                    count += 1
            except Exception as e:
                self.log(f"Write exception on {reg}: {e}")
        self.log(f"Sent {count} factory default parameters to drive")

    def download_params(self):
        if not self.client:
            self.log("Not connected")
            return
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
        except Exception as e:
            self.log(f"File read error: {e}")
            return

        slave = self.slave_var.get()
        count = 0
        for line in lines[1:]:  # skip header
            try:
                reg, param_num, name, val, unit = line.strip().split(",", 4)
                reg = int(reg)
                val = float(val)
                meta = param_dict.get(reg)
                if not meta:
                    continue
                raw_val = int(round(val * meta["scale"]))
                rr = self.client.write_register(reg, raw_val, unit=slave)
                if rr.isError():
                    self.log(f"Write error on {reg}")
                else:
                    count += 1
            except Exception as e:
                self.log(f"Upload parse error: {e}")
        self.log(f"Downloaded {count} parameters from {file_path} → drive")

    def upload_params(self):
        if not self.client:
            self.log("Not connected")
            return
        slave = self.slave_var.get()
        results = []
        for reg, meta in param_dict.items():
            try:
                rr = self.client.read_holding_registers(reg, 1, unit=slave)
                if rr.isError():
                    self.log(f"Read error on {reg}")
                    continue
                raw = rr.registers[0]
                scaled = raw / meta["scale"]
                results.append(f"{reg},{meta['param_num']},{meta['name']},{scaled},{meta['unit'] or ''}")
            except Exception as e:
                self.log(f"Read exception on {reg}: {e}")

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, "w") as f:
                f.write("Register,ParamNum,Name,Value,Unit\n")
                for line in results:
                    f.write(line + "\n")
            self.log(f"Uploaded {len(results)} parameters from drive → {file_path}")
        except Exception as e:
            self.log(f"File write error: {e}")

    def read_selected_param(self, event=None):
        if not self.client:
            self.log("Not connected")
            return
        selection = self.param_var.get()
        if not selection:
            return

        reg = self.param_lookup[selection]
        meta = param_dict.get(reg)
        if not meta:
            self.log(f"No metadata for register {reg}")
            return

        slave = self.slave_var.get()
        try:
            rr = self.client.read_holding_registers(reg, 1, unit=slave)
            if rr.isError():
                self.log(f"Read error: {rr}")
                return
            raw = rr.registers[0]
            scaled = raw / meta["scale"]
            raw = rr.registers[0]
            scaled = raw / meta["scale"]

            # If parameter has a mapping, decode it
            if "map" in meta and raw in meta["map"]:
                formatted = meta["map"][raw]
                self.param_value_var.set(formatted)
                self.param_unit_var.set("")  # mapped values usually don't need a unit
                self.log(f"Param {meta['param_num']} ({meta['name']}) = {formatted}")
            else:
                formatted = f"{scaled:.2f}" if meta["scale"] != 1 else str(scaled)
                self.param_value_var.set(formatted)
                self.param_unit_var.set(meta["unit"] or "")
                self.log(f"Param {meta['param_num']} ({meta['name']}) = {formatted} {meta['unit'] or ''}")

        except Exception as e:
            self.log(f"Read exception: {e}")

    def write_selected_param(self):
        if not self.client:
            self.log("Not connected")
            return
        selection = self.param_var.get()
        if not selection:
            self.log("No parameter selected")
            return

        reg = self.param_lookup[selection]
        meta = param_dict.get(reg)
        if not meta:
            self.log(f"No metadata for register {reg}")
            return

        try:
            user_val = self.param_value_var.get()

            if "map" in meta:
                # reverse lookup
                inv_map = {v: k for k, v in meta["map"].items()}
                if user_val in inv_map:
                    raw_val = inv_map[user_val]
                else:
                    # fallback: try numeric entry
                    raw_val = int(float(user_val))
            else:
                # normal numeric scaling
                raw_val = int(round(float(user_val) * meta["scale"]))

        except ValueError:
            self.log("Invalid input value")
            return

        slave = self.slave_var.get()
        try:
            rr = self.client.write_register(reg, raw_val, unit=slave)
            if rr.isError():
                self.log(f"Write error: {rr}")
            else:
                self.log(f"Wrote {user_val} {meta['unit'] or ''} "
                         f"(raw {raw_val}) to Param {meta['param_num']} ({meta['name']})")
        except Exception as e:
            self.log(f"Write exception: {e}")

    def log(self, text):
        self.terminal.insert("end", text + "\n")
        self.terminal.see("end")

    def connect(self):
        port = self.port_var.get()
        slave = self.slave_var.get()
        self.client = ModbusClient(method='rtu', port=port, baudrate=9600,
                                   bytesize=8, parity='N', stopbits=2, timeout=1)
        if not self.client.connect():
            messagebox.showerror("Error", f"Cannot connect to {port}")
            self.client = None
            return
        self.conn_btn.config(state="disabled")
        self.disc_btn.config(state="normal")
        self.log(f"Connected to {port} (slave {slave})")

    def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None
        self.conn_btn.config(state="normal")
        self.disc_btn.config(state="disabled")
        self.log("Disconnected")

    # --- Register read/write ---
    # Add an optional scale argument
    def read_register(self, reg, count=1, label=None, scale=1.0):
        if not self.client:
            self.log("Not connected")
            return
        slave = self.slave_var.get()
        try:
            rr = self.client.read_holding_registers(reg, count, unit=slave)
            if rr.isError():
                self.log(f"Read error: {rr}")
            else:
                if count == 1:
                    value = rr.registers[0] * scale
                    self.log(f"{label or f'Register {reg}'} = {value}")
                else:
                    scaled_regs = [v * scale for v in rr.registers]
                    self.log(f"{label or f'Registers {reg}..{reg + count - 1}'} = {scaled_regs}")
        except Exception as e:
            self.log(f"Read exception: {e}")

    def write_register(self, reg, value):
        if not self.client:
            self.log("Not connected")
            return
        slave = self.slave_var.get()
        try:
            rr = self.client.write_register(reg, value, unit=slave)
            if rr.isError():
                self.log(f"Write error: {rr}")
            else:
                self.log(f"Wrote {value} to register {reg}")
        except Exception as e:
            self.log(f"Write exception: {e}")

    # --- Command parsing ---
    def process_command(self, event=None):
        cmd = self.cmd_var.get().strip()
        if not cmd:
            return
        self.log(f"> {cmd}")
        parts = cmd.split()
        try:
            if len(parts) == 1:
                reg = int(parts[0])
                self.read_register(reg)
            elif len(parts) == 2:
                reg = int(parts[0])
                val = int(parts[1])
                self.write_register(reg, val)
            else:
                self.log("Invalid command. Use: <reg> or <reg> <value>")
        except ValueError:
            self.log("Invalid numbers")
        self.cmd_var.set("")


def main():
    root = tk.Tk()
    app = MCConsole(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.disconnect(), root.destroy()))
    root.mainloop()


if __name__ == "__main__":
    main()
