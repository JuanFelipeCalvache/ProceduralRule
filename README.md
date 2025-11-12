# ProceduralRuleCreator

**ProceduralRuleCreator** is an application designed to automate the creation of **CGA (Computer Generated Architecture)** files used in **Esri CityEngine**.  
It takes user-defined inputs and converts them into procedural rules for 3D modeling and urban environment generation.

---

## 🚀 Features

- **Multiple Input Modes:**  
  The application offers **three main views** to generate CGA files from different data sources:
  1. **Manual Input:** Users can directly define architectural parameters and attributes manually.  
  2. **CSV Import:** Automatically generate CGA rules by importing data from structured CSV files.  
  3. **Image Capture:** Uses an AI model trained with **YOLOv5** to detect architectural features such as **doors**, **windows**, and **balconies** from images and converts them into procedural CGA rules.

- **AI-Powered Detection:**  
  The image capture module leverages a **custom YOLOv5 model** trained for object detection of building elements, enabling semi-automatic rule creation based on visual input.

- **Seamless CGA Generation:**  
  Converts input data—whether from manual, CSV, or AI detection—into syntactically correct **.cga** files, ready for use in **CityEngine**.

---

## 🚀 Execution

To run the project from **Visual Studio Code**, follow these steps:

1. Open **Visual Studio Code** and load the project folder.

2. Open the integrated terminal (`Ctrl + ñ` or `Ctrl + Shift + ~`).

3. Navigate to the project directory (if not already there), for example:
   ```bash
   cd E:\workSpace\ArregloCE\AppCE\ProceduralRule

4. Execute the main file with:
  
   python main.py  

---

## 🧠 Technologies Used

- **Python 3**
- **YOLOv5** (for object detection)
- **Tkinter** (for GUI development)
- **OpenCV** (for image processing)
- **Pandas** (for CSV data handling)
- **Custom CGA Rule Generator**

---

## 📁 Project Structure

```
ProceduralRuleCreator/
├── models/
│   └── best.pt                # YOLOv5 trained model
├── src/
│   ├── main.py                # Main application entry point
│   ├── gui/
│   │   ├── manual_view.py     # Manual input interface
│   │   ├── csv_view.py        # CSV import interface
│   │   └── image_view.py      # Image detection interface
│   ├── utils/
│   │   ├── cga_generator.py   # CGA file generation logic
│   │   └── file_manager.py    # File handling utilities

└── README.md
```

---

## ⚙️ How It Works

1. **Select Input Method:** Choose between *Manual*, *CSV*, or *Image Capture* mode.  
2. **Provide Input Data:** Enter data manually, upload a CSV file, or select an image of a building.  
3. **Process Data:**  
   - For images, the YOLOv5 model detects architectural elements.  
   - For CSV/manual modes, the system parses user data directly.  
4. **Generate CGA File:** The app automatically creates a `.cga` file containing procedural modeling rules.  
5. **Export and Use in CityEngine.**

---

## 🧩 Example Use Case

- Upload a photo of a building.  
- The AI detects **windows**, **doors**, and **balconies**.  
- The system generates a **CGA rule file** that defines facade structure and textures for use in CityEngine.  

This streamlines the **procedural modeling** workflow, reducing manual rule creation time and improving accuracy.

---
