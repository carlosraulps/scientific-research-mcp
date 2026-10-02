#!/usr/bin/env python3
"""
volumetric_unwrap.py

Periodic boundary unwrapping for VASP volumetric files (CHGCAR, LOCPOT, ELFCAR, PARCHG, .cube).
Resolves artifact issues where reactive moieties at unit cell boundaries are split
across the periodic boundary, causing truncated, misleading contours in 2D slices.
"""

import argparse
import sys
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from typing import Tuple, List, Optional, Dict, Any

# Set typography to Times New Roman for scientific plots
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.serif'] = ['Times New Roman'] + matplotlib.rcParams['font.serif']
matplotlib.rcParams['mathtext.fontset'] = 'stix'


def read_chgcar(filepath: str) -> Tuple[np.ndarray, List[str], np.ndarray, np.ndarray, List[str]]:
    """
    Read VASP CHGCAR/LOCPOT volumetric file.
    
    Args:
        filepath: Path to the VASP volumetric file
        
    Returns:
        Tuple of (lattice, atoms, grid_data, ngrid, header_lines)
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    # Keep header up to the grid dimensions
    # VASP5/6 POSCAR format:
    # 0: Comment
    # 1: Scale
    # 2-4: Lattice vectors
    # 5: Species names
    # 6: Species counts
    # 7: Direct/Cartesian
    # 8 to 8+sum(counts)-1: coordinates
    # Empty line
    # NGX NGY NGZ
    # Data...
    
    scale = float(lines[1].strip())
    lattice = np.zeros((3, 3))
    for i in range(3):
        lattice[i] = [float(x) for x in lines[2+i].split()]
    lattice *= scale
    
    species_names = lines[5].split()
    species_counts = [int(x) for x in lines[6].split()]
    total_atoms = sum(species_counts)
    
    atoms = []
    # Read coordinates
    coord_start = 8
    for i in range(total_atoms):
        atoms.append(lines[coord_start+i])
        
    # Find grid dimensions
    grid_line_idx = coord_start + total_atoms
    while lines[grid_line_idx].strip() == '':
        grid_line_idx += 1
        
    ngx, ngy, ngz = [int(x) for x in lines[grid_line_idx].split()]
    ngrid = np.array([ngx, ngy, ngz])
    
    header_lines = lines[:grid_line_idx+1]
    
    # Read volumetric data
    data_lines = lines[grid_line_idx+1:]
    
    # We only read the first volumetric dataset, ignore spin polarization or augmentation occupancies for now
    n_points = ngx * ngy * ngz
    data = []
    
    for line in data_lines:
        vals = line.split()
        data.extend([float(v) for v in vals])
        if len(data) >= n_points:
            break
            
    # Reshape using Fortran order (VASP format: x changes fastest)
    grid_data = np.array(data[:n_points]).reshape((ngx, ngy, ngz), order='F')
    
    return lattice, atoms, grid_data, ngrid, header_lines


def unwrap_volumetric(grid_data: np.ndarray, shift_fractions: Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> np.ndarray:
    """Roll volumetric grid by fractional shifts to center features.
    
    Args:
        grid_data: 3D numpy array (NGX, NGY, NGZ)
        shift_fractions: Tuple of (dx, dy, dz) fractional shifts (0.0-1.0)
    
    Returns:
        Rolled 3D array
    """
    ngx, ngy, ngz = grid_data.shape
    rolled = np.roll(grid_data, int(shift_fractions[0] * ngx), axis=0)
    rolled = np.roll(rolled, int(shift_fractions[1] * ngy), axis=1)
    rolled = np.roll(rolled, int(shift_fractions[2] * ngz), axis=2)
    return rolled


def auto_center_feature(grid_data: np.ndarray, method: str = 'max_gradient') -> Tuple[np.ndarray, Tuple[float, float, float]]:
    """Automatically detect the reactive feature and center it.
    
    Args:
        grid_data: 3D numpy array (NGX, NGY, NGZ)
        method: 
            'max_gradient': Center on the point of maximum |grad(rho)|
            'max_abs': Center on the point of maximum |rho| (for CDD files)
            'centroid': Center on charge-weighted centroid
            
    Returns:
        Tuple of (centered_grid_data, applied_shift_fractions)
    """
    ngx, ngy, ngz = grid_data.shape
    
    if method == 'max_gradient':
        # Calculate gradients using central differences, respecting periodic boundaries
        grad_x = np.gradient(grid_data, axis=0)
        grad_y = np.gradient(grid_data, axis=1)
        grad_z = np.gradient(grid_data, axis=2)
        grad_mag = np.sqrt(grad_x**2 + grad_y**2 + grad_z**2)
        max_idx = np.unravel_index(np.argmax(grad_mag), grid_data.shape)
        
    elif method == 'max_abs':
        max_idx = np.unravel_index(np.argmax(np.abs(grid_data)), grid_data.shape)
        
    elif method == 'centroid':
        abs_data = np.abs(grid_data)
        total_weight = np.sum(abs_data)
        if total_weight == 0:
            max_idx = (ngx // 2, ngy // 2, ngz // 2)
        else:
            x_indices = np.arange(ngx)[:, np.newaxis, np.newaxis]
            y_indices = np.arange(ngy)[np.newaxis, :, np.newaxis]
            z_indices = np.arange(ngz)[np.newaxis, np.newaxis, :]
            
            cx = int(np.sum(x_indices * abs_data) / total_weight)
            cy = int(np.sum(y_indices * abs_data) / total_weight)
            cz = int(np.sum(z_indices * abs_data) / total_weight)
            max_idx = (cx, cy, cz)
    else:
        raise ValueError(f"Unknown auto-center method: {method}")
        
    # Calculate shifts required to move max_idx to the center (ngx/2, ngy/2, ngz/2)
    shift_x = (ngx // 2) - max_idx[0]
    shift_y = (ngy // 2) - max_idx[1]
    shift_z = (ngz // 2) - max_idx[2]
    
    frac_x = shift_x / ngx
    frac_y = shift_y / ngy
    frac_z = shift_z / ngz
    
    shift_fractions = (frac_x, frac_y, frac_z)
    centered_data = unwrap_volumetric(grid_data, shift_fractions)
    
    return centered_data, shift_fractions


def write_chgcar(filepath: str, lattice: np.ndarray, atoms: List[str], grid_data: np.ndarray, header_lines: List[str]) -> None:
    """Write back the unwrapped CHGCAR with same header format."""
    with open(filepath, 'w') as f:
        # Write header verbatim (Note: coordinates of atoms are NOT shifted in this script!
        # This script purely shifts the volumetric grid for visualization purposes.
        # If atomic alignment is needed, POSCAR modification would be required.)
        f.writelines(header_lines)
        
        # Write grid data (5 values per line)
        flat_data = grid_data.flatten(order='F')
        
        for i in range(0, len(flat_data), 5):
            chunk = flat_data[i:i+5]
            f.write(" ".join([f"{val:18.11E}" for val in chunk]) + "\n")


def extract_2d_slice(grid_data: np.ndarray, lattice: np.ndarray, plane: str = 'xy', frac_pos: float = 0.5) -> np.ndarray:
    """Extract a 2D slice from the 3D volumetric grid.
    
    Args:
        grid_data: 3D numpy array
        lattice: 3x3 lattice vectors
        plane: 'xy', 'xz', or 'yz'
        frac_pos: fractional position along the normal axis
        
    Returns:
        2D numpy array representing the slice
    """
    ngx, ngy, ngz = grid_data.shape
    
    if plane == 'xy':
        z_idx = int(frac_pos * ngz) % ngz
        return grid_data[:, :, z_idx]
    elif plane == 'xz':
        y_idx = int(frac_pos * ngy) % ngy
        return grid_data[:, y_idx, :]
    elif plane == 'yz':
        x_idx = int(frac_pos * ngx) % ngx
        return grid_data[x_idx, :, :]
    else:
        raise ValueError("Plane must be 'xy', 'xz', or 'yz'")


def plot_slice(slice_data: np.ndarray, out_path: str, plane: str, title: str = "") -> None:
    """Plot and save a 2D slice."""
    plt.figure(figsize=(8, 6))
    
    # Use a diverging colormap suitable for charge density
    # For CDD, coolwarm is good. For regular density, viridis.
    vmax = np.max(np.abs(slice_data))
    vmin = -vmax if np.min(slice_data) < -1e-5 else 0
    
    cmap = 'coolwarm' if vmin < 0 else 'viridis'
    
    plt.imshow(slice_data.T, origin='lower', cmap=cmap, aspect='auto', vmin=vmin, vmax=vmax)
    plt.colorbar(label='Electron Density / CDD (e/Bohr^3)')
    
    if plane == 'xy':
        plt.xlabel('X (grid points)')
        plt.ylabel('Y (grid points)')
    elif plane == 'xz':
        plt.xlabel('X (grid points)')
        plt.ylabel('Z (grid points)')
    elif plane == 'yz':
        plt.xlabel('Y (grid points)')
        plt.ylabel('Z (grid points)')
        
    if title:
        plt.title(title)
        
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Volumetric grid periodic unwrap tool")
    parser.add_argument("input", help="Input volumetric file (CHGCAR format)")
    parser.add_argument("--shift", nargs=3, type=float, metavar=('DX', 'DY', 'DZ'),
                        help="Fractional shifts (0.0-1.0) along x, y, z axes")
    parser.add_argument("--auto-center", action="store_true", help="Automatically center the feature")
    parser.add_argument("--method", type=str, default="max_gradient", choices=['max_gradient', 'max_abs', 'centroid'],
                        help="Method for auto-centering")
    parser.add_argument("-o", "--output", type=str, help="Output unwrapped volumetric file")
    
    parser.add_argument("--slice", type=str, choices=['xy', 'xz', 'yz'], help="Extract 2D slice along specified plane")
    parser.add_argument("--slice-pos", type=float, default=0.5, help="Fractional position of slice along normal axis")
    parser.add_argument("--slice-out", type=str, help="Output image file for slice")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found.")
        sys.exit(1)
        
    print(f"Reading {args.input}...")
    lattice, atoms, grid_data, ngrid, header = read_chgcar(args.input)
    print(f"Grid dimensions: {ngrid[0]} x {ngrid[1]} x {ngrid[2]}")
    
    needs_shift = args.shift is not None or args.auto_center
    
    if needs_shift:
        if args.auto_center:
            print(f"Auto-centering using method: {args.method}")
            grid_data, applied_shifts = auto_center_feature(grid_data, method=args.method)
            print(f"Applied shifts: {applied_shifts[0]:.3f}, {applied_shifts[1]:.3f}, {applied_shifts[2]:.3f}")
        else:
            print(f"Applying manual shifts: {args.shift}")
            grid_data = unwrap_volumetric(grid_data, tuple(args.shift))
            
    if args.output:
        print(f"Writing shifted volumetric data to {args.output}...")
        write_chgcar(args.output, lattice, atoms, grid_data, header)
        
    if args.slice and args.slice_out:
        print(f"Extracting 2D slice on {args.slice} plane at position {args.slice_pos}...")
        slice_data = extract_2d_slice(grid_data, lattice, plane=args.slice, frac_pos=args.slice_pos)
        
        # Support headless rendering via xvfb-run or simple backend
        matplotlib.use('Agg')
        plot_slice(slice_data, args.slice_out, args.slice, title=f"{args.slice} slice at {args.slice_pos}")
        print(f"Saved slice to {args.slice_out}")

if __name__ == "__main__":
    main()
