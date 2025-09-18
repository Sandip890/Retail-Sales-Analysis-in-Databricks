Absolutely! Here’s a **GitHub-friendly, visually appealing README.md** for your project with emojis and proper formatting:

---

# 🛒 Retail Sales Analysis in Databricks

## 📖 Project Overview

This project performs a **Retail Sales Analysis** using **Databricks** and **PySpark**.
The goal is to analyze sales and store data to:

* Optimize store performance 📈
* Identify top-selling products 🏆
* Discover high-performing stores 🏬

The project includes **data cleaning, transformation, analysis**, and **storing results** in DBFS.

---

## 📂 Dataset

The analysis uses **two CSV files**:

1. **`sales_data.csv`** – Sales transactions

   * `sale_id`
   * `store_id`
   * `product_id`
   * `sale_date`
   * `quantity`
   * `total_amount`

2. **`store_data.csv`** – Store information

   * `store_id`
   * `store_region`
   * `store_size`
   * `open_date`

---

## 🧹 Data Cleaning

### Sales Data

* Fill null values in `quantity` and `total_amount` with `0`
* Remove rows with null `sale_id`, `store_id`, or `sale_date`
* Remove negative values in `quantity` and `total_amount`
* Remove duplicate rows

### Store Data

* Remove rows with null `store_id`
* Replace null `store_size` with **average store size**
* Remove rows with null `open_date`

---

## 🔄 Data Transformation

* Join `sales_df` and `store_df` on `store_id`
* Add a `year` column extracted from `sale_date` 🗓️
* Calculate `sales_per_sqrft`:

  ```
  sales_per_sqrft = total_amount / store_size
  ```

---

## 📊 Analysis

* **Total sales and quantity per store and region**
* **Top 5 products** by total quantity sold 🥇
* **Top 5 stores** by total sales 💰

---

## 💾 Storing Results

* Save **top products** and **top stores** as **Parquet files** in DBFS:

  ```
  /FileStore/tables/top_products
  /FileStore/tables/top_stores
  ```

---

## 🛠️ Tools & Technologies

* **Databricks** – Notebook environment
* **PySpark** – Data processing
* **SQL** – Aggregations and analytics
* **Parquet** – Efficient storage format

---

## ⚡ How to Run

1. Upload `sales_data.csv` and `store_data.csv` to Databricks FileStore
2. Open the notebook `Retail Sales Analysis Project.py` in Databricks
3. Run all cells sequentially
4. Access the results in DBFS as Parquet files

---

## 🎯 Output

* Cleaned and transformed sales and store data ✅
* Top 5 products sold 🏆
* Top 5 stores by sales 💵
* Parquet files for downstream analysis 🗄️

---
**THANK YOU!!!**
