# Library Automation Program
An under development library automation program that writed in Python 3 witk tkinter.

## Notes

In exe.zip file there is an executable file of this program. If you want to run it you must close your antivirus software.
In Linux you must delete 45th row in main_1.py. This code just suitable for Windows.
If you have better ideas for this project you can communicate with me.


## The Modules Needed

- xlrd
- PIL
- sqlite3
- time
- datetime

For Linux
`pip install xlrd Pillow sqlite3 time datetime`

For Windows
`python -m pip install xlrd Pillow sqlite3 time datetime`


## Convert to Executable File

Need for PyInstaller

For Linux
`pip install pyinstaller`
`pyinstaller --onefile --hidden-import "PIL._tkinter_finder" --hidden-import "PIL.imagingtk" main_1.py`

For Windows
`python -m pip install PyInstaller`
`python -m PyInstaller --onefile --hidden-import "PIL._tkinter_finder" --hidden-import "PIL.imagingtk" main_1.py`

