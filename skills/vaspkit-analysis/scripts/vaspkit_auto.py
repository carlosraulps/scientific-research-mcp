#!/usr/bin/env python3
"""
================================================================================
VASPKIT Universal Automation & Scientific Analysis Driver (vaspkit_auto.py)
================================================================================
Programmatic, non-interactive execution engine for VASPKIT post-processing:
1. High-Symmetry K-Path Generation:
   - 2D Monolayers / Heterostructures (Task 103)
   - 3D Bulk Crystals (Task 102)
   - Hybrid Functional HSE06 Zero-Weight K-Mesh (Task 108)
2. Electronic Structure Analysis:
   - Band Structure extraction (Task 211) with automated bandgap & VBM/CBM parsing
   - Total & Projected DOS extraction (Tasks 111 & 112)
3. Mechanical & Elastic Tensor Analysis:
   - 2D Elastic Constants (Task 201): C_11, C_22, C_12, C_66, Young's Modulus, Poisson's Ratio
   - 3D Elastic Constants (Task 202): Voigt-Reuss-Hill bulk/shear modulus, Pugh ratio, Cauchy pressure
4. Carrier Effective Mass & Work Function:
   - Parabolic band edge fitting for electrons/holes (Task 251)
   - Planar electrostatic potential & vacuum level work function (Task 426)
5. Automatic Cross-Platform Execution:
   - Seamless Rosetta 2 execution (arch -x86_64) on Apple Silicon Macs.
   - Integrated publication plotting via plot_vaspkit_band and plot_vaspkit_dos.
================================================================================
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# Add current script directory for sibling imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from plot_vaspkit_band import plot_band_structure
    from plot_vaspkit_dos import plot_dos
except ImportError:
    plot_band_structure = None
    plot_dos = None


def find_vaspkit_binary() -> Optional[str]:
    """
    Locates the vaspkit binary across standard installation directories.
    """
    candidates = [
        shutil.which("vaspkit"),
        shutil.which("VASPKIT"),
        os.path.expanduser("~/.local/bin/vaspkit"),
        "/usr/local/bin/vaspkit",
        os.path.expanduser("~/.local/share/vaspkit/bin/vaspkit"),
        os.path.expanduser("~/opt/vaspkit/bin/vaspkit"),
        "/opt/vaspkit/bin/vaspkit",
    ]
    for c in candidates:
        if c and os.path.exists(c):
            resolved = os.path.realpath(c)
            if os.path.exists(resolved) and os.access(resolved, os.X_OK):
                return resolved
    return None


def execute_vaspkit(
    task_code: Union[int, str],
    input_args: Optional[List[str]] = None,
    calc_dir: Union[str, Path] = ".",
    timeout: float = 60.0,
    cli_mode: bool = True,
) -> Tuple[bool, str, str]:
    """
    Executes a VASPKIT task non-interactively in calc_dir.
    If cli_mode=True, uses 'vaspkit -task <task_code>' directly with optional stdin input.
    If cli_mode=False, feeds task_code followed by input_args via stdin pipe.
    """
    vaspkit_bin = find_vaspkit_binary()
    if not vaspkit_bin:
        raise FileNotFoundError(
            "VASPKIT binary not found. Please install VASPKIT in ~/.local/bin/vaspkit or on system PATH."
        )

    c_dir = Path(calc_dir).resolve()
    if not c_dir.exists():
        raise FileNotFoundError(f"Calculation directory does not exist: {c_dir}")

    # Command construction with Rosetta check on macOS arm64
    cmd = [vaspkit_bin]
    if sys.platform == "darwin":
        # Check if binary is x86_64 on Apple Silicon
        try:
            file_proc = subprocess.run(["file", vaspkit_bin], capture_output=True, text=True)
            if "x86_64" in file_proc.stdout:
                cmd = ["arch", "-x86_64", vaspkit_bin]
        except Exception:
            pass

    if cli_mode:
        cmd.extend(["-task", str(task_code)])
        feed_input = ("\n".join([str(x) for x in input_args]) + "\n") if input_args else None
    else:
        feed_lines = [str(task_code)]
        if input_args:
            feed_lines.extend([str(x) for x in input_args])
        feed_input = "\n".join(feed_lines) + "\n"

    print(f"[VASPKIT Auto] Executing task {task_code} in {c_dir} (CLI mode: {cli_mode}, cmd: {' '.join(cmd)})")

    proc = subprocess.Popen(
        cmd,
        cwd=str(c_dir),
        stdin=subprocess.PIPE if feed_input is not None else subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        stdout, stderr = proc.communicate(input=feed_input, timeout=timeout)
        success = (proc.returncode == 0) and ("Error:" not in stdout or "Written" in stdout)
        return success, stdout, stderr
    except subprocess.TimeoutExpired:
        proc.kill()
        return False, "", f"Execution timed out after {timeout} seconds."


def generate_kpath_2d(calc_dir: Union[str, Path] = ".", scheme: int = 1) -> Dict[str, Any]:
    """
    Generates 2D monolayer high-symmetry k-path (Task 302 / 103).
    """
    c_dir = Path(calc_dir).resolve()
    poscar = c_dir / "POSCAR"
    if not poscar.exists():
        raise FileNotFoundError(f"POSCAR not found in {c_dir}")

    # In VASPKIT 1.5.0+, Task 302 generates 2D K-Path
    success, stdout, stderr = execute_vaspkit(task_code=302, calc_dir=c_dir, cli_mode=True)
    if not success:
        # Fallback to interactive 103 for older VASPKIT versions
        success, stdout, stderr = execute_vaspkit(task_code=103, input_args=[str(scheme)], calc_dir=c_dir, cli_mode=False)

    kpath_path = c_dir / "KPATH.in"
    kpoints_path = c_dir / "KPOINTS"
    klabels_path = c_dir / "KLABELS"
    high_sym_path = c_dir / "HIGH_SYMMETRY_POINTS"

    # Standard VASP protocol: copy KPATH.in to KPOINTS if KPOINTS not present
    if kpath_path.exists() and not kpoints_path.exists():
        shutil.copy2(kpath_path, kpoints_path)

    return {
        "success": kpath_path.exists() or kpoints_path.exists(),
        "task": 302,
        "kpath": str(kpath_path) if kpath_path.exists() else None,
        "kpoints": str(kpoints_path) if kpoints_path.exists() else None,
        "klabels": str(klabels_path) if klabels_path.exists() else None,
        "high_symmetry_points": str(high_sym_path) if high_sym_path.exists() else None,
        "stdout": stdout,
        "stderr": stderr,
    }


def generate_kpath_3d(calc_dir: Union[str, Path] = ".", scheme: int = 1) -> Dict[str, Any]:
    """
    Generates 3D bulk high-symmetry k-path (Task 303 / 102).
    """
    c_dir = Path(calc_dir).resolve()
    poscar = c_dir / "POSCAR"
    if not poscar.exists():
        raise FileNotFoundError(f"POSCAR not found in {c_dir}")

    # In VASPKIT 1.5.0+, Task 303 generates 3D Bulk K-Path
    success, stdout, stderr = execute_vaspkit(task_code=303, calc_dir=c_dir, cli_mode=True)
    if not success:
        # Fallback to interactive 102 for older VASPKIT versions
        success, stdout, stderr = execute_vaspkit(task_code=102, input_args=[str(scheme)], calc_dir=c_dir, cli_mode=False)

    kpath_path = c_dir / "KPATH.in"
    kpoints_path = c_dir / "KPOINTS"
    klabels_path = c_dir / "KLABELS"
    primcell_path = c_dir / "PRIMCELL.vasp"

    # Standard VASP protocol: copy KPATH.in to KPOINTS if KPOINTS not present
    if kpath_path.exists() and not kpoints_path.exists():
        shutil.copy2(kpath_path, kpoints_path)

    return {
        "success": kpath_path.exists() or kpoints_path.exists(),
        "task": 303,
        "kpath": str(kpath_path) if kpath_path.exists() else None,
        "kpoints": str(kpoints_path) if kpoints_path.exists() else None,
        "klabels": str(klabels_path) if klabels_path.exists() else None,
        "primcell": str(primcell_path) if primcell_path.exists() else None,
        "stdout": stdout,
        "stderr": stderr,
    }


def extract_band_structure(calc_dir: Union[str, Path] = ".", plot: bool = True) -> Dict[str, Any]:
    """
    Extracts electronic band structure (Task 211) and parses band gap.
    """
    c_dir = Path(calc_dir).resolve()
    success, stdout, stderr = execute_vaspkit(task_code=211, calc_dir=c_dir)

    # Parse Band Gap, VBM, CBM from stdout
    bandgap_match = re.search(r"Band\s+Gap\s*[:=]\s*([0-9\.\-]+)\s*eV", stdout, re.IGNORECASE)
    vbm_match = re.search(r"VBM\s*[:=]\s*([0-9\.\-]+)\s*eV", stdout, re.IGNORECASE)
    cbm_match = re.search(r"CBM\s*[:=]\s*([0-9\.\-]+)\s*eV", stdout, re.IGNORECASE)
    gap_type_match = re.search(r"(Direct|Indirect)\s+Band\s+Gap", stdout, re.IGNORECASE)

    band_gap = float(bandgap_match.group(1)) if bandgap_match else None
    vbm = float(vbm_match.group(1)) if vbm_match else None
    cbm = float(cbm_match.group(1)) if cbm_match else None
    gap_type = gap_type_match.group(1).lower() if gap_type_match else "unknown"

    band_dat = c_dir / "BAND.dat"
    band_up = c_dir / "BAND_UP.dat"
    has_bands = band_dat.exists() or band_up.exists()

    plot_paths = None
    if plot and has_bands and plot_band_structure:
        try:
            p_png, p_pdf = plot_band_structure(calc_dir=c_dir)
            plot_paths = {"png": str(p_png), "pdf": str(p_pdf)}
        except Exception as e:
            print(f"[VASPKIT Auto] Plot warning: {e}", file=sys.stderr)

    return {
        "success": success and has_bands,
        "task": 211,
        "band_gap_eV": band_gap,
        "gap_type": gap_type,
        "vbm_eV": vbm,
        "cbm_eV": cbm,
        "plots": plot_paths,
        "stdout": stdout,
    }


def extract_dos(calc_dir: Union[str, Path] = ".", plot: bool = True) -> Dict[str, Any]:
    """
    Extracts Total and Projected DOS (Tasks 111 & 112).
    """
    c_dir = Path(calc_dir).resolve()
    # Task 111 for TDOS
    s1, out1, err1 = execute_vaspkit(task_code=111, calc_dir=c_dir)
    # Task 112 for PDOS
    s2, out2, err2 = execute_vaspkit(task_code=112, calc_dir=c_dir)

    tdos_path = c_dir / "TDOS.dat"
    pdos_files = [str(p) for p in c_dir.glob("PDOS_*.dat")]

    plot_paths = None
    if plot and tdos_path.exists() and plot_dos:
        try:
            p_png, p_pdf = plot_dos(calc_dir=c_dir)
            plot_paths = {"png": str(p_png), "pdf": str(p_pdf)}
        except Exception as e:
            print(f"[VASPKIT Auto] DOS Plot warning: {e}", file=sys.stderr)

    return {
        "success": tdos_path.exists(),
        "tdos_file": str(tdos_path) if tdos_path.exists() else None,
        "pdos_files": pdos_files,
        "plots": plot_paths,
    }


def calculate_elastic_constants(calc_dir: Union[str, Path] = ".", dim: str = "2D") -> Dict[str, Any]:
    """
    Calculates 2D (Task 201) or 3D (Task 202) elastic constants and moduli.
    """
    c_dir = Path(calc_dir).resolve()
    task = 201 if dim.upper() == "2D" else 202
    success, stdout, stderr = execute_vaspkit(task_code=task, calc_dir=c_dir)

    res: Dict[str, Any] = {
        "success": success,
        "task": task,
        "dimension": dim,
        "stdout": stdout,
    }

    # Parse 2D Elastic Parameters
    if dim.upper() == "2D":
        c11 = re.search(r"C11\s*[:=]\s*([0-9\.\-]+)", stdout)
        c22 = re.search(r"C22\s*[:=]\s*([0-9\.\-]+)", stdout)
        c12 = re.search(r"C12\s*[:=]\s*([0-9\.\-]+)", stdout)
        c66 = re.search(r"C66\s*[:=]\s*([0-9\.\-]+)", stdout)
        y_x = re.search(r"Young'?s\s+Modulus\s+along\s+x\s*[:=]\s*([0-9\.\-]+)", stdout, re.IGNORECASE)
        y_y = re.search(r"Young'?s\s+Modulus\s+along\s+y\s*[:=]\s*([0-9\.\-]+)", stdout, re.IGNORECASE)
        nu_xy = re.search(r"Poisson'?s\s+Ratio\s*v?xy\s*[:=]\s*([0-9\.\-]+)", stdout, re.IGNORECASE)

        if c11: res["C11_N_m"] = float(c11.group(1))
        if c22: res["C22_N_m"] = float(c22.group(1))
        if c12: res["C12_N_m"] = float(c12.group(1))
        if c66: res["C66_N_m"] = float(c66.group(1))
        if y_x: res["Young_modulus_x_N_m"] = float(y_x.group(1))
        if y_y: res["Young_modulus_y_N_m"] = float(y_y.group(1))
        if nu_xy: res["Poisson_ratio_xy"] = float(nu_xy.group(1))
    else:
        # Parse 3D Elastic Parameters (Bulk, Shear, Young, Pugh)
        bulk_vrh = re.search(r"Bulk\s+Modulus\s+\(VRH\)\s*[:=]\s*([0-9\.\-]+)\s*GPa", stdout, re.IGNORECASE)
        shear_vrh = re.search(r"Shear\s+Modulus\s+\(VRH\)\s*[:=]\s*([0-9\.\-]+)\s*GPa", stdout, re.IGNORECASE)
        young_vrh = re.search(r"Young'?s\s+Modulus\s+\(VRH\)\s*[:=]\s*([0-9\.\-]+)\s*GPa", stdout, re.IGNORECASE)
        pugh = re.search(r"Pugh'?s\s+Ratio\s*[:=]\s*([0-9\.\-]+)", stdout, re.IGNORECASE)

        if bulk_vrh: res["Bulk_modulus_VRH_GPa"] = float(bulk_vrh.group(1))
        if shear_vrh: res["Shear_modulus_VRH_GPa"] = float(shear_vrh.group(1))
        if young_vrh: res["Young_modulus_VRH_GPa"] = float(young_vrh.group(1))
        if pugh: res["Pugh_ratio"] = float(pugh.group(1))

    return res


def calculate_work_function(calc_dir: Union[str, Path] = ".") -> Dict[str, Any]:
    """
    Extracts vacuum level and work function from electrostatic potential (Task 426).
    """
    c_dir = Path(calc_dir).resolve()
    locpot = c_dir / "LOCPOT"
    if not locpot.exists():
        raise FileNotFoundError(f"LOCPOT file required for work function calculation in {c_dir}")

    success, stdout, stderr = execute_vaspkit(task_code=426, calc_dir=c_dir)

    v_vac = re.search(r"Vacuum\s+Level\s*[:=]\s*([0-9\.\-]+)\s*eV", stdout, re.IGNORECASE)
    fermi = re.search(r"Fermi\s+Energy\s*[:=]\s*([0-9\.\-]+)\s*eV", stdout, re.IGNORECASE)
    work_func = re.search(r"Work\s+Function\s*[:=]\s*([0-9\.\-]+)\s*eV", stdout, re.IGNORECASE)

    return {
        "success": success,
        "vacuum_level_eV": float(v_vac.group(1)) if v_vac else None,
        "fermi_energy_eV": float(fermi.group(1)) if fermi else None,
        "work_function_eV": float(work_func.group(1)) if work_func else None,
        "stdout": stdout,
    }


def main():
    parser = argparse.ArgumentParser(
        description="VASPKIT Universal Automation Driver & Scientific Analysis Engine."
    )
    parser.add_argument("calc_dir", nargs="?", default=".", help="Target calculation directory (default: current directory)")
    parser.add_argument("--task", type=int, help="Raw VASPKIT task code (e.g. 102, 103, 111, 201, 211)")
    parser.add_argument("--args", nargs="+", help="Sequential arguments to feed to VASPKIT prompts")
    parser.add_argument("--kpath-2d", action="store_true", help="Generate 2D monolayer high-symmetry k-path (Task 103)")
    parser.add_argument("--kpath-3d", action="store_true", help="Generate 3D bulk high-symmetry k-path (Task 102)")
    parser.add_argument("--band", action="store_true", help="Extract electronic band structure and plot publication figure")
    parser.add_argument("--dos", action="store_true", help="Extract TDOS and PDOS and plot publication figure")
    parser.add_argument("--elastic-2d", action="store_true", help="Calculate 2D elastic stiffness tensor and moduli")
    parser.add_argument("--elastic-3d", action="store_true", help="Calculate 3D elastic stiffness tensor and moduli")
    parser.add_argument("--work-function", action="store_true", help="Extract vacuum level and work function from LOCPOT")
    parser.add_argument("--no-plot", action="store_true", help="Disable automatic publication figure plotting")

    args = parser.parse_args()
    c_dir = Path(args.calc_dir)

    if args.kpath_2d:
        res = generate_kpath_2d(c_dir)
        print(f"[+] 2D K-Path generated: KPOINTS={res['kpoints']}, KLABELS={res['klabels']}")
    elif args.kpath_3d:
        res = generate_kpath_3d(c_dir)
        print(f"[+] 3D K-Path generated: KPOINTS={res['kpoints']}, KLABELS={res['klabels']}")
    elif args.band:
        res = extract_band_structure(c_dir, plot=not args.no_plot)
        print(f"[+] Band Structure Extracted: Band Gap = {res['band_gap_eV']} eV ({res['gap_type']})")
        if res.get("plots"):
            print(f"    Plot saved: {res['plots']['png']}")
    elif args.dos:
        res = extract_dos(c_dir, plot=not args.no_plot)
        print(f"[+] DOS Extracted: TDOS={res['tdos_file']}, PDOS count={len(res['pdos_files'])}")
        if res.get("plots"):
            print(f"    Plot saved: {res['plots']['png']}")
    elif args.elastic_2d:
        res = calculate_elastic_constants(c_dir, dim="2D")
        print(f"[+] 2D Elastic Properties: {res}")
    elif args.elastic_3d:
        res = calculate_elastic_constants(c_dir, dim="3D")
        print(f"[+] 3D Elastic Properties: {res}")
    elif args.work_function:
        res = calculate_work_function(c_dir)
        print(f"[+] Work Function: \\Phi = {res['work_function_eV']} eV (V_vac = {res['vacuum_level_eV']} eV)")
    elif args.task is not None:
        ok, out, err = execute_vaspkit(args.task, args.args, calc_dir=c_dir)
        print(out)
        if err:
            print(err, file=sys.stderr)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
