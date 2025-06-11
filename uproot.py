import uproot
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os

def gaussian(x, amp, mean, sigma):
    return amp * np.exp(-0.5 * ((x - mean) / sigma) ** 2)

class TFile:
    def __init__(self, filename, mode="READ"):
        self.file = uproot.open(filename)
    
    def Get(self, key):
        return TTree(self.file[key])

class TTree:
    def __init__(self, tree):
        self.tree = tree
        self.last_hist_data = None
        self.last_hist_label = None
    
    def GetBranch(self, branch_name):
        return self.tree[branch_name]
    
    def _parse_cut(self, cut_str):
        if not cut_str:
            return None

        # Basic: only supports branch OP value format
        import re
        pattern = r"([A-Za-z0-9_]+)\s*([<>=!]+)\s*([0-9\.]+)"
        match = re.match(pattern, cut_str.strip())
        if not match:
            raise ValueError("Invalid cut string format")

        branch, op, value = match.groups()
        data = self.tree[branch].array(library="np")
        expr = f"data {op} {value}"
        return eval(expr)

    def Draw(self, branch_name, bins=100, range=None, fit=None, cut=None):
        data = self.tree[branch_name].array(library="np")

        if cut:
            try:
                mask = self._parse_cut(cut)
                data = data[mask]
            except Exception as e:
                print(f"[!] Cut parsing failed: {e}")
        
        self.last_hist_data = data
        self.last_hist_label = branch_name

        plt.hist(data, bins=bins, range=range, histtype='stepfilled',
                 color='skyblue', edgecolor='black', alpha=0.7, label=branch_name)

        if fit == "gaus":
            counts, bin_edges = np.histogram(data, bins=bins)
            bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
            try:
                popt, _ = curve_fit(gaussian, bin_centers, counts, p0=[max(counts), np.mean(data), np.std(data)])
                x_fit = np.linspace(min(data), max(data), 1000)
                plt.plot(x_fit, gaussian(x_fit, *popt), 'r--',
                         label=f'Gaussian Fit\nμ={popt[1]:.2f}, σ={popt[2]:.2f}')
            except RuntimeError:
                plt.text(0.5, 0.9, "Fit failed", transform=plt.gca().transAxes, ha="center", color="red")

        plt.xlabel(branch_name)
        plt.ylabel("Counts")
        plt.title(f"{branch_name} Distribution")
        plt.legend()
        plt.grid(True)
        plt.show()

    def Draw2D(self, x_branch, y_branch, bins=50, range=None, cut=None):
        x = self.tree[x_branch].array(library="np")
        y = self.tree[y_branch].array(library="np")

        if cut:
            try:
                mask = self._parse_cut(cut)
                x = x[mask]
                y = y[mask]
            except Exception as e:
                print(f"[!] Cut parsing failed: {e}")

        plt.hist2d(x, y, bins=bins, range=range, cmap="viridis")
        plt.colorbar(label="Counts")
        plt.xlabel(x_branch)
        plt.ylabel(y_branch)
        plt.title(f"{x_branch} vs {y_branch}")
        plt.grid(True)
        plt.show()

    def SaveHistogram(self, branch_name, filename="histogram.png"):
        if self.last_hist_data is None:
            print("No histogram to save. Please run .Draw() first.")
            return

        plt.hist(self.last_hist_data, bins=100, histtype='stepfilled',
                 color='skyblue', edgecolor='black', alpha=0.7, label=self.last_hist_label)
        plt.xlabel(self.last_hist_label)
        plt.ylabel("Counts")
        plt.title(f"{self.last_hist_label} Distribution")
        plt.grid(True)
        plt.savefig(filename)
        print(f"[+] Histogram saved as: {os.path.abspath(filename)}")
