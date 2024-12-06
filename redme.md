# Blood Donor Scraper

This Python script scrapes blood donor information from the Friends2Support website and saves it to CSV files. It allows users to search for donors based on blood group, state, district, and city.

## Prerequisites

Before running the script, ensure you have the following installed on your Windows machine:

1. **Python**: Download and install Python from [python.org](https://www.python.org/downloads/). Make sure to check the box to add Python to your PATH during installation.

2. **Selenium**: Install the Selenium library using pip. Open your command prompt and run:
   ```bash
   pip install selenium
   ```

3. **Web Browser**: This script uses Firefox. Make sure you have it installed on your machine.

4. **Geckodriver**: Download the appropriate version of Geckodriver for your system from [Geckodriver releases](https://github.com/mozilla/geckodriver/releases). Extract the downloaded file and add the path to the `geckodriver.exe` to your system's PATH.

## How to Use

1. **Clone or Download the Repository**: Download the script file `f2s_state_windows.py` to your local machine.

2. **Open Command Prompt**: Navigate to the directory where you saved the script.

3. **Run the Script**: Execute the script by running:
   ```bash
   python f2s_state_windows.py
   ```

4. **Follow the Prompts**: The script will prompt you to select a state from a dropdown menu. Make your selection and wait for the script to complete its execution.

5. **Check the Output**: After the script finishes running, it will create a directory named after the selected state. Inside this directory, you will find CSV files containing the blood donor information for each district.

## Important Notes

- The script may take some time to run, depending on the number of districts and cities in the selected state.
- Ensure you have a stable internet connection while running the script, as it requires access to the website.
- If you encounter any errors, check the console output for error messages that can help you troubleshoot.

## License

This project is open-source and available for anyone to use and modify.

## Contact

For any questions or issues, feel free to reach out to the author.