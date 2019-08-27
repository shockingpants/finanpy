{
  "cells": [
    {
      "cell_type": "markdown",
      "source": [
        "# Is renting or buying a better idea?\n",
        "## Why people say renting it *BAD*?\n",
        "The common argument against renting is that rents do not go towards\n",
        "building equity. More importantly, they increase with inflation, so\n",
        "rents will likely appreciate in the future. By buying a house, you\n",
        "basically convert rent to interest, which decreases over time due to\n",
        "amortization. Even if I am being generous and look at long term loans,\n",
        "monthly interest rates payment will likely be lower than rent for the same\n",
        "apartment.\n",
        "\n",
        "The next thing to take into account is the mortgage payment. While the\n",
        "portion that covers interest is lower than rent, the total amount is likely\n",
        "higher. It can easily take a toll on a family's cash flow and liquidity. It\n",
        "also commits the owner to **invest in real estate**. How does that work?\n",
        "\n",
        "## Buying a house is a real estate investment.\n",
        "When you take out a long term loan, you are promising to put\n",
        "aside a certain amount of money each month to pay off the loan. Another way to look\n",
        "at it is that you are putting some money aside towards building equity in real\n",
        "estate. To elaborate, suppose you pay off a portion of the loan, and the\n",
        "house appreciates in the mean time. By selling the house, and paying off\n",
        "the debt, you immediately make a capital gain using the money you 'invested'\n",
        "in the house. (We are ignoring fixed cost for now, which can be significant)\n",
        "It is akin to trading on margin.\n",
        "\n",
        "## Rent vs Buying\n",
        "The question boils down to whether the difference in real estate and other\n",
        "gains, and their fixed costs makes it worthwhile for either investment. We\n",
        "will compare between two scenarios:\n",
        "\n",
        "1. We buy a house and sell it after x number of years. There is some fixed\n",
        "  cost, and monthly mortage repayment.\n",
        "2. We rent a house, and invest the rest of our money in a safe investment.\n",
        "  rent is expected to increase with inflation.\n",
        "\n",
        "We will look at different x to get an idea when a crossover happens.\n"
      ],
      "metadata": {}
    },
    {
      "cell_type": "code",
      "source": [
        "import finanpy as fp\n",
        "import pandas as pd\n",
        "import numpy as np\n",
        "import matplotlib.pyplot as plt\n"
      ],
      "outputs": [],
      "execution_count": null,
      "metadata": {
        "collapsed": false,
        "outputHidden": false,
        "inputHidden": false
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "Suppose we pay off the mortgage after 30 years. We assume that rent increases at the same\n",
        "rate as property appreciation. We also assume that rent is valued at a\n",
        "price-to-rent ratio of 30 years in Singapore. These are assumption we will\n",
        "soften later on. Home loan interest rates are based on HDB rates of 2.6%.\n"
      ],
      "metadata": {}
    },
    {
      "cell_type": "code",
      "source": [
        "Y = 30 # Number of years\n",
        "p = 1000000\n",
        "rent = p/30/12.\n",
        "inflation = 0 # Rental inflation\n",
        "REr = inflation # Real estate growth\n",
        "Rr = 0.05 # Low risk interest\n",
        "fc = 0.05 # fixed cost\n",
        "\n",
        "# Annual interest rates for Y number of years\n",
        "pa = np.zeros(Y) + 0.026  # This is the rate for a HDB Loan\n",
        "output = fp.amortize_schedule(p, pa)  # Month, c, cp, ci, debt, ti\n",
        "Ti = output['ti']  # Total Interest over time\n",
        "Tpp = np.cumsum(output['cp'])  # Total Principal Paid\n",
        "\n",
        "# Calculating Home Savings\n",
        "Hp = [p*(1+REr/12)**y for y in range(Y*12+1)]  # House price\n",
        "Hs = np.array(Hp) - fc*p - output['debt'] # Home savings\n",
        "\n",
        "# Calculating Rental Savings\n",
        "rr = [rent*(1+inflation/12)**y for y in range(Y*12)] # real rent\n",
        "Rs = fp.save_series((np.array(output['c'][1:]) - rr), Rr, Y)\n",
        "\n",
        "plt.figure()\n",
        "plt.ion()\n",
        "plt.plot(range(Y*12+1), Hs, label='Home Savings')\n",
        "plt.plot(range(Y*12+1), Rs, label='Rental Savings')\n",
        "plt.xlabel('month')\n",
        "plt.ylabel('savings ($)')\n",
        "plt.legend()\n",
        "plt.grid()\n",
        "plt.title('Assets over time')\n"
      ],
      "outputs": [],
      "execution_count": null,
      "metadata": {
        "collapsed": false,
        "outputHidden": false,
        "inputHidden": false
      }
    },
    {
      "cell_type": "code",
      "source": [
        "Y = 30 # Number of years\n",
        "p = 1000000\n",
        "rent = p/30/12.\n",
        "inflat = 0.03\n",
        "fp.homevsrent(Y, 1000000, inflat, rent, inflat, 0.05, 0.05)  # Y,p,Rer,rent,inflation,Rr,fc\n"
      ],
      "outputs": [],
      "execution_count": null,
      "metadata": {
        "collapsed": false,
        "outputHidden": false,
        "inputHidden": false
      }
    },
    {
      "cell_type": "code",
      "source": [
        "Y = 20 # Number of years\n",
        "p = 1000000\n",
        "rent = p/30/12.\n",
        "inflat = 0.03\n",
        "fp.homevsrent(Y, 1000000, inflat, rent, inflat, 0.05, 0.05)  # Y,p,Rer,rent,inflation,Rr\n"
      ],
      "outputs": [],
      "execution_count": null,
      "metadata": {
        "collapsed": false,
        "outputHidden": false,
        "inputHidden": false
      }
    },
    {
      "cell_type": "code",
      "source": [
        "Y = 40 # Number of years\n",
        "p = 1000000\n",
        "rent = p/30/12.\n",
        "inflat = 0.03\n",
        "fp.homevsrent(Y, 1000000, inflat, rent, inflat, 0.05, 0.05)  # Y,p,Rer,rent,inflation,Rr\n"
      ],
      "outputs": [],
      "execution_count": null,
      "metadata": {
        "collapsed": false,
        "outputHidden": false,
        "inputHidden": false
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "From the plots above, depending on the length of repayment, savings you get\n",
        "by renting will always be lower than buying a house.\n",
        "Also, regardless of term of loan, if you decide to sell the house within 5\n",
        "years of buying, the fixed cost from a home purchase will eat into profits.\n",
        "If the fixed cost is large enough, it can be better to rent,\n",
        "assuming the end goal is to sell the house.\n",
        "\n",
        "Interestingly, notice how savings take a dive at longer terms. The inflation\n",
        "in rental starts eating into savings.\n",
        "\n",
        "What if investment interest rates falls or increases?\n",
        "As you will see below, while a strong investment return will generate\n",
        "savings, it is mostly erased by the ever increasing rent, which is the\n",
        "biggest downside to renting compared to buying a house. Only in\n",
        "situations where equity returns far outweigh the appreciation of real\n",
        "estate (home and/or rent) do you see substantial benefit with renting\n",
        "after a long time. The risk is also much higher since you need the\n",
        "consistently large return year on year while rent increases has to be\n",
        "really low and even then, you don't see a significant increase in savings.\n"
      ],
      "metadata": {}
    },
    {
      "cell_type": "code",
      "source": [
        "Y = 30 # Number of years\n",
        "p = 1000000\n",
        "rent = p/30/12.\n",
        "inflat = 0.03\n",
        "fp.homevsrent(Y, 1000000, inflat, rent, inflat, 0.08, 0.05)  # Y,p,Rer,rent,inflation,Rr,fc\n"
      ],
      "outputs": [],
      "execution_count": null,
      "metadata": {
        "collapsed": false,
        "outputHidden": false,
        "inputHidden": false
      }
    },
    {
      "cell_type": "code",
      "source": [
        "Y = 30 # Number of years\n",
        "p = 1000000\n",
        "rent = p/30/12.\n",
        "inflat = 0.01\n",
        "fp.homevsrent(Y, 1000000, inflat, rent, inflat, 0.08, 0.05)  # Y,p,Rer,rent,inflation,Rr,fc\n"
      ],
      "outputs": [],
      "execution_count": null,
      "metadata": {
        "collapsed": false,
        "outputHidden": false,
        "inputHidden": false
      }
    },
    {
      "cell_type": "code",
      "source": [
        "Y = 30 # Number of years\n",
        "p = 1000000\n",
        "rent = p/30/12.\n",
        "inflat = 0.01\n",
        "fp.homevsrent(Y, 1000000, inflat, rent, inflat, 0.05, 0)  # Y,p,Rer,rent,inflation,Rr,fc\n"
      ],
      "outputs": [],
      "execution_count": null,
      "metadata": {
        "collapsed": false,
        "outputHidden": false,
        "inputHidden": false
      }
    }
  ],
  "metadata": {
    "kernelspec": {
      "argv": [
        "python",
        "-m",
        "ipykernel_launcher",
        "-f",
        "{connection_file}"
      ],
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}