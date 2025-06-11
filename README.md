#LightROOT
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
