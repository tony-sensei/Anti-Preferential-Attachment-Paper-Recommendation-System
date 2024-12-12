# Project Setup Instructions

This project utilizes the **ANN Dataset** as referenced in the following paper:  
https://link.springer.com/article/10.1007/s10579-012-9211-2

The recommended Python version for running this project is **Python 3.12.4**. Follow the instructions below to set up the project and run it.

### Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.x (Recommended version: 3.12.4)
- `pip` (Python package installer)

### Step-by-Step Guide

1. **Clone the repository**:
   Open your terminal or command prompt, navigate to your desired folder, and run:
   
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Create a virtual environment** (recommended):
   It is recommended to create a virtual environment to manage dependencies.
   Run the following commands:
   
   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:
   - **For Windows**:
   
   ```bash
     venv\Scripts\activate
   ```
     
   - **For macOS/Linux**:
   
   ```bash
     source venv/bin/activate
   ```

3. **Install dependencies**:
   Once you have the virtual environment activated, install the required packages by running:
   
   ```bash
   pip install -r requirements.txt
   ```

   This command will install all the necessary packages, including the Neo4j Python driver, and any other dependencies for the project.

4. **Setup**:
   Create a `.env` file in the root directory with the following content:

   ```env
   NEO4J_URI=<your_uri_here>
   NEO4J_USERNAME=<your_username_here>
   NEO4J_PASSWORD=<your_password_here>
   ```

5. **Run the application**:
   Most of the results are stored in `visulization/preview` 
   and `experiments/results`. 

   To prepare the dataset, Neo4j, and re-run the experiments, execute:

   ```bash
   python main.py
   ```


6. **Weight Reaccessment of Edges**
   Execute python files in `weight_reaccessment_of_edges` for doing Weight Reaccessment of Edges modification.


7. **Model evaluation**
   Execute python file in `model_evaluation` for doing model evaluation.