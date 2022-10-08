import os
os.system("pip uninstall -y py-cord")
os.system("pip uninstall -y discord.py")
os.system("pip install -U discord.py==1.7.3")
os.system("pip install -U py-cord==2.0.0b7")
os.system("pip install -U jishaku")
os.system("python create_db.py")
os.system("python bot.py")