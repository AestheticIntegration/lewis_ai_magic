# Functions for testing and plotting results from functions in dists.ml

from scipy.special import gamma
import scipy.stats as st
import numpy as np
import matplotlib.pyplot as plt


# Helper functions and constants

python = "dist_tests/python_output/"
ocaml = "dist_tests/ocaml_output/"
comparisons = "dist_tests/error_plots/"
samples = "dist_tests/samples/"
constraints = "dist_tests/constraints/"
sample_plots = "dist_tests/sample_plots/"
constraint_plots = "dist_tests/constraint_plots/"

functions = ["q_bernoulli",
            "q_binomial",
            "q_cauchy",
            "q_exponential",
            "q_laplace",
            "q_logistic",
            "q_poisson",
            "q_uniform",
            "c_bernoulli",
            "c_binomial",
            "c_cauchy",
            "c_exponential",
            "c_laplace",
            "c_logistic",
            "c_poisson",
            "c_uniform",
            "d_beta",
            "d_gamma",
            "d_gaussian",
            "d_lognormal"]

dists = {\
        "bernoulli": st.bernoulli(0.3),
        "beta": st.beta(2.3, 4.9),
        "binomial": st.binom(40, 0.62),
        "categorical": None,
        "cauchy": st.cauchy(6.2, 1.1),
        "exponential": st.expon(scale=1/3.76),
        "gamma": st.gamma(4.3),
        "gaussian": st.norm(100, 15),
        "laplace": st.laplace(-13.9, 4.4),
        "logistic": st.logistic(0.9, 0.22),
        # "lognormal": st.lognorm(0.8, 0, np.exp(0.2)),
        "poisson": st.poisson(14.5),
        "uniform": st.uniform(-209.6, 44.7 - 209.6)
        }

const = {"bernoulli": [(0,0)],
        "beta": [(-0.1,0.28), (0.34,0.38), (0.5,0.9)],
        "binomial": [(0,7), (12,12), (17,26), (30,40)],
        "categorical": [(1,1), (2,2), (5,5)],
        "cauchy": [(0.,5.4), (12.,13.)],
        "exponential": [(0.4,0.99), (2.01,2.8)],
        "gamma": [(11,20), (24,100)],
        "gaussian": [(30.,50.), (100.,150.), (155.,170.)],
        "laplace": [(-20,-10)],
        "logistic": [(-0.3,0), (0.5,0.81), (1.5,15)],
        "lognormal": [(3.22,3.28), (3.57,3.67)],
        "poisson": [(4,12), (16,18), (30,60)],
        "uniform": [(-141.3,-141.3), (-101.1,-75.5), (-50.6,-26.7)]}

qf_range = np.linspace(0,1,101)

def save(x, name):

    np.savetxt(python + name, x, fmt='%.6f')


# Check QFs

def save_qfs():

    save(st.bernoulli.ppf(qf_range, 0.73), "q_bernoulli.csv")
    save(st.binom.ppf(qf_range, 30, 0.2), "q_binomial.csv")
    save(st.cauchy.ppf(qf_range, 5.6, 1.3), "q_cauchy.csv")
    save(st.expon.ppf(qf_range, scale=1/2.356), "q_exponential.csv")
    save(st.laplace.ppf(qf_range, -53, 12), "q_laplace.csv")
    save(st.logistic.ppf(qf_range, -0.004, 0.02), "q_logistic.csv")
    save(st.poisson.ppf(qf_range, 4.3), "q_poisson.csv")
    save(st.uniform.ppf(qf_range, 13.444, 56.876 - 13.444), "q_uniform.csv")


# Check CDFs

def save_cdfs():

    save(st.bernoulli.cdf([True, False, False, True], 0.6), "c_bernoulli.csv")
    save(st.binom.cdf(np.linspace(0,30,31), 30, 0.34), "c_binomial.csv")
    save(st.cauchy.cdf(np.linspace(-25.66, 198.1, 101), -5.3, 4), "c_cauchy.csv")
    save(st.expon.cdf(np.linspace(-1.22, 13.99, 101), scale=1/2.8), "c_exponential.csv")
    save(st.laplace.cdf(np.linspace(-1.22, 5.99, 101), 3.01, 0.667), "c_laplace.csv")
    save(st.logistic.cdf(np.linspace(-14.2, 53.29, 101), 15.9, 4.32), "c_logistic.csv")
    save(st.poisson.cdf(np.linspace(0, 100, 101), 36.3), "c_poisson.csv")
    save(st.uniform.cdf(np.linspace(-1440.2, 13000.4, 101), 10.334, 10009.8 - 10.334), "c_uniform.csv")


# Check PDFs

def save_pdfs():

    save(st.beta.pdf(qf_range, 2.9, 6.7), "d_beta.csv")
    save((1/3.8) * st.gamma.pdf((1/3.8) * np.linspace(0, 27.1, 101), 3), "d_gamma.csv")
    save(st.norm.pdf(np.linspace(3603.8, 7321.1, 101), 5900.5, 434.5), "d_gaussian.csv")
    save(st.lognorm.pdf(np.linspace(10.66, 13.6, 101), 3.111, 0, np.exp(12.4)), "d_lognormal.csv")


# Function tests

def run_function_tests():

    save_qfs()
    save_cdfs()
    save_pdfs()

def plot_function_tests():

    for f in functions:

        python_x = np.loadtxt(python + f + ".csv")
        ocaml_x = np.loadtxt(ocaml + f + ".csv")
        diff = python_x - ocaml_x
        fig, ax = plt.subplots()
        ax.plot(diff)
        fig.savefig(comparisons + f + "_density.png")


# Sampling tests

def make_plots(use_constraints=False):

    for dist in dists.keys():
        
        # Load samples and create plot
        if use_constraints:
            data = constraints
        else:
            data = samples
        s = np.loadtxt(data + dist + ".csv")
       

        s.sort()
        fig, ax = plt.subplots() 
        
        # Discrete dists
        if dist in ["bernoulli","binomial","poisson","categorical"]:
            if dist == "bernoulli" or dist == "categorical":
                d = None
                w = (1 / s.size) * np.ones(s.shape)
            else:
                d = True
                w = None
            # x = range(int(s.min()), int(s.max()) + 1)
            x = np.unique(s)
            ax.hist(s, bins=len(x), density=d, weights=w, label='Samples')
            if dist == "categorical":
                pmf = np.array([0.1,0.6,0.02,0.08,0.2])

                if use_constraints:
                    pmf = np.array([i / (0.1 + 0.6 + 0.2) for i in [0.1, 0.6, 0.2]])

            else:
                pmf = dists[dist].pmf(x)
                
                if use_constraints:
                    area = 0
                    for (c1, c2) in const[dist]:
                        points = list(range(int(c1),int(c2)+1))
                        domain = (c2 - c1)
                        area += domain * sum([dists[dist].pmf(x) for x in points]) / len(points)

                    print("{} scaling factor: {}".format(dist,area))

                    pmf /= area

            ax.plot(x, pmf, 'o', label='PMF', color='Red')

        # Continuous dists
        else:
            if dist == "cauchy":
                s = s[(s >= -13.8) & (s <= 26.2)]
                b = 100
            if dist == "uniform":
                pdf = np.linspace(-1/(44.7 - 209.6),-1/(44.7 - 209.6),10000)
                pdf /= (pdf.sum() * ((s.max() - s.min()) / s.size))
                b = 25
            elif dist == "gamma":
                pdf = (1/3.4) * dists[dist].pdf((1/3.4) * s)
                b = 100
            else:
                pdf = dists[dist].pdf(s)
                b = 100

            if use_constraints:
                area = 0
                for (c1, c2) in const[dist]:
                    points = np.linspace(c1, c2, 1000)
                    domain = (c2 - c1)
                    if dist == "gamma":
                        area += domain * ((1/3.4) * (dists[dist].pdf((1/3.4) * points))).sum() / points.size
                    else:
                        area += domain * (dists[dist].pdf(points)).sum() / points.size
           
                print("{} scaling factor: {}".format(dist,area))

                pdf /= area

            ax.plot(s, pdf, '.', label='PDF', color='Red')
            ax.hist(s, bins=b, density=True, label='Samples')

        # Plot constraints
        if use_constraints:
            plots = constraint_plots
            for (a, b) in const[dist]:
                ax.axvline(x=a, color='Green')
                ax.axvline(x=b, color='Green')
        else:
            plots = sample_plots

        # Save image
        ax.legend()
        fig.savefig(plots + dist + ".png")


# Test Nemes gamma function approximation

def nemes_closed_form(z):

    return ((z/np.exp(1)) ** z) * np.sqrt(2 * np.pi / z) * ((1 + (1 / (15 * (z ** 2)))) ** (1.25 * z))
    
def nemes_0_1(z):

    return nemes_closed_form(z + 1) / z

def log_nemes(x):

    a = 0
    a += x * (np.log(x) - 1)
    a += 0.5 * (np.log(2*np.pi) - np.log(x))
    a += 1.25 * x * (np.log((15 * (x ** 2)) + 1) - np.log(15 * (x ** 2)))

    return a 

def test_log_nemes():

    t = np.linspace(0.001,100.0,1000)
    n = np.log(nemes_closed_form(t))
    m = log_nemes(t)
    q = n - m
    fig, ax = plt.subplots()
    ax.plot(t, q)
    fig.savefig("log_nemes_test.png")


# Main

if __name__ == "__main__":

    # run_function_tests()
    # plot_function_tests()
    # make_plots()
    make_plots(use_constraints=True)

