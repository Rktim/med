# 🩺 Medical Data Categorization Tool

**Status**: Experimental Phase

## 📖 Overview

This project is designed to process medical datasets, specifically focusing on analyzing patient haemoglobin and platelet counts. It categorizes patients based on predefined thresholds, facilitating better understanding and visualization of patient health metrics.

## 🧰 Features

- **Data Ingestion**: Accepts `.xlsx` files containing patient data.
- **Categorization Logic**:
  - **Category A**: Haemoglobin ≥ 8 & Platelets ≥ 50
  - **Category B**: Haemoglobin ≥ 8 & Platelets < 50
  - **Category C**: Haemoglobin < 8 & Platelets ≥ 50
  - **Category D**: Haemoglobin < 8 & Platelets < 50
- **Output**: Displays categorized patient data directly in the console.




### Usage

1. **Prepare Your Data**:

   - Ensure your Excel file (`.xlsx`) contains the following columns:
     - `HAEMOGLOBIN`
     - `PLATELETS COUNT`
   - Place the Excel file in the project directory.

2. **Run the Script**:

   ```bash
   python med.py
   ```

   - The script will read the Excel file, categorize patients based on the defined thresholds, and display the results in the console.



## 📝 Notes

- The project is currently in the experimental phase. Contributions and suggestions are welcome!
- Ensure that the Excel file's headers match exactly with `HAEMOGLOBIN` and `PLATELETS COUNT` for accurate processing.

## 📬 Contact

For any questions or feedback, please reach out to [Raktim Kalita ](https://github.com/Rktim).

---
## License
This project is licensed under the MIT License – you are free to use, modify, distribute, and even sell it under the terms of the license.

See the (LICENSE) file for details.
