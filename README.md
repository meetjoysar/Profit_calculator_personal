# 💰 Profit Calculator with GST

A streamlined vibecoded web application for calculating business profit with GST (Goods and Services Tax) considerations, compliant with Indian tax regulations.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

## 📋 Overview

This Streamlit app helps businesses and individuals calculate net profit after considering:
- Purchase and sale prices with flexible GST input methods
- GST differences between purchase and sale
- Multiple expense categories
- Tax calculations based on Indian tax logic

Optimized for both mobile and desktop devices.

## ✨ Features

- **Dual Sale Price Input Methods**
  - Method 1: Enter sale price WITHOUT GST
  - Method 2: Enter sale price WITH GST (inclusive)

- **Comprehensive Calculations**
  - Gross profit and net profit after tax
  - GST difference tracking
  - Automated expense calculations (transport, goodwill, and other expenses)
  - Tax computation (applied only on positive profits)

- **Mobile-First Design**
  - Responsive layout for all screen sizes
  - Batched input with single "Calculate" action
  - Auto-scroll to results after calculation

- **Detailed Breakdown**
  - Purchase and sale details with GST
  - Expense itemization
  - Before-tax and after-tax profit views

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
  git clone https://github.com/meetjoysar/Profit_calculator_personal.git
  cd Profit_calculator_personal

2. Install dependencies:
  streamlit run profit_calculator_vibecoded.py

The app will open in your default browser at `http://localhost:8501`