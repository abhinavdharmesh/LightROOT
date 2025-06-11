# LightROOT
## 📦 PyROOT-Like Wrapper for `uproot` in Google Colab

This Python module simulates a subset of PyROOT-style syntax using the `uproot` library for seamless use in environments like Google Colab, where native PyROOT is hard to install. The goal is to allow physics students (like myself) to learn and practice basic ROOT workflows such as plotting, histogramming, and fitting using familiar commands — all without setting up a full Linux ROOT environment. This wrapper provides a class-based interface (`TFile`, `TTree`) and supports commonly used operations like `Get`, `Draw`, and Gaussian fitting, mimicking PyROOT behavior.

---

### 🧠 Command Mapping Table (PyROOT ➡️ uproot Wrapper)

| PyROOT Syntax                      | Wrapper Equivalent                 | Notes                                                  |
| ---------------------------------- | ---------------------------------- | ------------------------------------------------------ |
| `TFile("file.root")`               | `TFile("file.root")`               | Opens ROOT file via `uproot.open` internally           |
| `file.Get("tree")`                 | `file.Get("tree")`                 | Returns a `TTree` wrapper object                       |
| `tree.GetBranch("branch")`         | `tree.GetBranch("branch")`         | Provides access to a branch (can be removed if unused) |
| `tree.Draw("Muon_pt")`             | `tree.Draw("Muon_pt")`             | Plots histogram using matplotlib, optional fit support |
| `tree.Draw("Muon_pt", fit="gaus")` | `tree.Draw("Muon_pt", fit="gaus")` | Applies Gaussian fit with `scipy.optimize.curve_fit`   |
| `tree.Draw(..., range=(a,b))`      | `tree.Draw(..., range=(a,b))`      | Custom histogram x-range                               |

---

> ✅ Currently supports histogram plotting, Gaussian fitting, branch access, and future extensions like cut strings (`"Muon_pt > 30 && isElectron"`) are planned.
> ⚠️ This is *not* a full PyROOT replacement — but it does 80% of the work you need for basic analysis and learning.


## ✅ Quickstart

### 🧪 Step-by-step to run it on Google Colab:

1. **Create a new notebook** in [Google Colab](https://colab.research.google.com/).

2. Install the required packages:

   ```python
   !pip install uproot matplotlib scipy
   ```

3. **Import the wrapper from GitHub**:

   ```python
   !wget https://raw.githubusercontent.com/abhinavdharmesh/ROOT/main/uproot_wrapper.py
   from uproot_wrapper import TFile
   ```

4. **Use it like PyROOT!**

   ```python
   file = TFile("test_data.root")
   tree = file.Get("Events")
   tree.Draw("Muon_pt", bins=100, fit="gaus")
   ```

---

## 🔄 PyROOT vs Wrapper Syntax Comparison

| PyROOT                       | This Wrapper (Uproot under hood)     |
| ---------------------------- | ------------------------------------ |
| `TFile("file.root")`         | `TFile("file.root")`                 |
| `file.Get("tree")`           | `file.Get("tree")`                   |
| `tree.Draw("branch")`        | `tree.Draw("branch")`                |
| `tree.GetBranch("branch")`   | `tree.GetBranch("branch")`           |
| Gaussian fit (`TF1 + Fit()`) | `fit="gaus"` inside `Draw()`         |
| `TH1F` Histogram object      | Auto-done with `matplotlib.hist()`   |
| `canvas.SaveAs("file.png")`  | `plt.savefig("file.png")` (if added) |

> **Not Supported Yet:**
> `TTree::Scan`, `TCanvas`, `TLegend`, event loop macros, object trees, TChain, etc.
> You’re in the “stat plotting and fitting” comfort zone – perfect for learning and small demos.

---

## ⚠️ Notes

* This wrapper is **not a full ROOT simulator**.
* It’s ideal for *histograms*, *basic data inspection*, and *Gaussian fitting*.
* You can extend it further with functions like:

  * `tree.SaveHistogram()`
  * `tree.PlotOverlay(branch1, branch2)`
  * or add `TGraph`-like support with `matplotlib.plot()`
