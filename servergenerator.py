import os, time, subprocess, sys

if "-v" in sys.argv:
    Verbose = True
else:
    Verbose = False

#Utility:
def clearTerm(): os.system('cls' if os.name == 'nt' else 'clear')

#Color Functions
end = "\u001b[0m"
def red(text:str): return "\u001b[31m" + text + end
def green(text:str): return "\u001b[32m" + text + end
def yellow(text:str): return "\u001b[33m" + text + end
def blue(text:str): return "\u001b[34m" +text+end

try:
    import requests
except ImportError:
    print(red("Dependency Needed: Requests. Install with ") + "pip install requests")

javaVersion = subprocess.run(["javac", "--version"], stdout=subprocess.PIPE)
javaVersion = javaVersion.stdout.decode('UTF-8')
if "javac" in javaVersion:
    javaVersion = javaVersion[javaVersion.index(" ")+1:]
else:
    print(red("Failed to find compatible Java runtime. Please install Java before running this script."))
    quit()

def downloadFile(fileName, URL):
    with open(fileName, "wb+") as f:
            print(yellow("Downloading %s" % fileName))
            response = requests.get(URL, stream=True)
            if response.status_code == requests.codes.ok:
                total_length = response.headers.get('content-length')

                if total_length is None: # no content length header
                    f.write(response.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size=4096):
                        dl += len(data)
                        f.write(data)
                        done = int(50 * dl / total_length)
                        sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                        sys.stdout.flush()
                print(green("\nDownload Complete"))
                
            else:
                print(red("Server file Failed to Download. Trying Again"))
                print(yellow("Downloading %s" % fileName))
                response = requests.get(URL, stream=True)
                if response.status_code == requests.codes.ok:
                    total_length = response.headers.get('content-length')

                    if total_length is None: # no content length header
                        f.write(response.content)
                    else:
                        dl = 0
                        total_length = int(total_length)
                        for data in response.iter_content(chunk_size=4096):
                            dl += len(data)
                            f.write(data)
                            done = int(50 * dl / total_length)
                            sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                            sys.stdout.flush()
                else:
                    print(red("Failed to download server file. HTTP Error - " + response.status_code))
                    quit()
            f.close()



while True:
    clearTerm()
    print(yellow("Minecraft Server Generator *Beta*"))
    print("Pick an option:")
    print("Java Version: v" + str(javaVersion))
    if Verbose: print(blue("Verbose Mode On"))
    print(green("1. Generate Vanilla Java Server"))
    print(green("2. Generate Spigot Java Server"))
    print(green("3. Generate Vanilla Bedrock Server"))
    print(green("4. Exit"))
    
    prompt = input("Select ID [1-4]   >")
    try:
        prompt = int(prompt)
    except Exception:
        print(red("Enter a Valid ID"))
        time.sleep(3)
        continue
    if prompt not in [1,2,3,4]:
        print(red("Enter a Valid ID"))
        time.sleep(3)
        continue
    clearTerm()
    if prompt == 4:
        print(red("User prompted to quit."))
        quit()

    print(yellow("Enter name of folder server will be held in."))
    print(yellow("Must be a valid folder name - no spaces"))
    folderName = input(">")
    if " " in folderName:
        print(red("Please enter a valid folder name (ERR: No Spaces)"))
        time.sleep(3)
        continue
    print(yellow("Directory will be created at " + os.path.dirname(os.path.realpath(sys.argv[0]))+ "/"+ folderName))
    if prompt == 1:
        print(green("Preparing to create a Minecraft Java Vanilla server."))
        print(yellow("Would you like to continue? [Y/N]"))
        toContinue = input(">")
        if toContinue.lower() != 'y':
            print(red("User prompted to quit."))
            quit()
        print(yellow("Creating Directory."))
        try:
            directoryName = os.path.dirname(os.path.realpath(sys.argv[0]))
            subprocess.run(["mkdir", directoryName + "/" + folderName]) if Verbose else subprocess.run(["mkdir", directoryName + "/" + folderName], stdout=subprocess.PIPE)
            os.chdir(directoryName + f"/{folderName}")
        except Exception as e:
            print(red("Error Creating Directory"))
            print(red(str(e)))
            quit()
        print(yellow("Starting Download."))
        
        r = requests.get("https://MinecraftGenerator.brysonvan1.repl.co/v1/vanilla")
        if r.status_code != requests.codes.ok:
            print(red("Failed to get download, trying again..."))
            r = requests.get("https://MinecraftGenerator.brysonvan1.repl.co/v1/vanilla")
            if r.status_code != requests.codes.ok:
                print(red("Failed to get Minecraft Java Server Install - HTTP Code " + str(r.status_code)))
                quit()
        serverUrl = r.text
        r = requests.get("https://MinecraftGenerator.brysonvan1.repl.co/v1/vanilla.version")
        if r.status_code == requests.codes.ok:
            serverVersion = r.text
            fServerVersion = "-"+serverVersion
        else:
            serverVersion = ""
            fServerVersion = ""
        print(green("Download URL Retrieved. Starting Download..."))
        fileName = "minecraft-server" + fServerVersion+".jar"
        downloadFile(fileName, serverUrl)
        print(yellow("Preparing Server Setup..."))
        subprocess.run(["java", "-jar", fileName]) if Verbose else subprocess.run(["java", "-jar", fileName], stdout=subprocess.PIPE)
        eula = open("eula.txt", "w")
        eula.write("eula=true")
        eula.close()
        print(green("Your server is now set up!"))
        print("Would you like to make an easy start script? [Y/N]")
        ezstart = input(">")
        if ezstart.lower() == "y":
            ezstartfile = open("start.sh", "w+")
            ezstartfile.write("java -jar " + fileName)
            ezstartfile.close()
            print(green("Easy Start Script Complete"))
        print("Click enter to go to the main menu")
        input()


    elif prompt == 2:
        print(green("Preparing to create a SpigotMC server."))
        gitVersion = subprocess.run(["git", "--version"], stdout=subprocess.PIPE)
        gitVersion = gitVersion.stdout.decode('UTF-8')
        if "git version" not in gitVersion:
            print(red("Git is not installed. Installation can not continue until git is installed."))
            quit()
        print(yellow("Would you like to continue? [Y/N]"))
        toContinue = input(">")
        if toContinue.lower() != 'y':
            print(red("User prompted to quit."))
            quit()
        print(yellow("Creating Directory."))
        try:
            directoryName = os.path.dirname(os.path.realpath(sys.argv[0]))
            subprocess.run(["mkdir", directoryName + "/" + folderName])
            os.chdir(directoryName + f"/{folderName}")
        except Exception as e:
            print(red("Error Creating Directory"))
            print(red(str(e)))
            quit()
        print(yellow("Beginning BuildTools Download..."))
        downloadFile("BuildTools.jar", "https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar")
        print(green("BuildTools was downloaded. Building your server..."))
        subprocess.run(["java", "-jar", "BuildTools.jar", "--rev", "latest"]) if Verbose else subprocess.run(["java", "-jar", "BuildTools.jar", "--rev", "latest"], stdout=subprocess.PIPE)
        f = []
        for (dirpath, dirnames, filenames) in os.walk("./"):
            f.extend(filenames) 
            break
        fileName = ""
        for file in f:
            if "spigot" in file:
                fileName = file
        subprocess.run(["java", "-jar", fileName]) if Verbose else subprocess.run(["java", "-jar", fileName], stdout=subprocess.PIPE)
        print(yellow("Signing EULA"))
        eula = open("eula.txt", "w+")
        eula.write("eula=true")
        eula.close()
        print(green("Server Setup Complete!"))
        print("Would you like to make an easy start script? [Y/N]")
        ezstart = input(">")
        if ezstart.lower() == "y":
            ezstartfile = open("start.sh", "w+")
            ezstartfile.write("java -jar " + fileName)
            ezstartfile.close()
            print(green("Easy Start Script Complete"))

        print("Click enter to go to the main menu")
        input()
    
    elif prompt == 3:
        print(green("Preparing to create a Minecraft Bedrock server (Alpha)"))
        print(yellow("Would you like to continue? [Y/N]"))
        toContinue = input(">")
        if toContinue.lower() != 'y':
            print(red("User prompted to quit."))
            quit()
        print(yellow("Creating Directory."))
        try:
            directoryName = os.path.dirname(os.path.realpath(sys.argv[0]))
            subprocess.run(["mkdir", directoryName + "/" + folderName]) if Verbose else subprocess.run(["mkdir", directoryName + "/" + folderName], stdout=subprocess.PIPE)
            os.chdir(directoryName + f"/{folderName}")
        except Exception as e:
            print(red("Error Creating Directory"))
            print(red(str(e)))
            quit()
        print(yellow("Starting Download."))
        
        r = requests.get("https://MinecraftGenerator.brysonvan1.repl.co/v1/bedrock")
        if r.status_code != requests.codes.ok:
            print(red("Failed to get download, trying again..."))
            r = requests.get("https://MinecraftGenerator.brysonvan1.repl.co/v1/bedrock")
            if r.status_code != requests.codes.ok:
                print(red("Failed to get Minecraft Bedrock Server Install - HTTP Code " + str(r.status_code)))
                quit()
        serverUrl = r.text
        r = requests.get("https://MinecraftGenerator.brysonvan1.repl.co/v1/bedrock.version")
        if r.status_code == requests.codes.ok:
            serverVersion = r.text
            fServerVersion = "-"+serverVersion
        else:
            serverVersion = ""
            fServerVersion = ""
        print(green("Download URL Retrieved. Starting Download..."))
        fileName = "bedrock-server" + fServerVersion+".zip"
        downloadFile(fileName, serverUrl)
        print(yellow("Preparing Server Setup..."))
        subprocess.run(["unzip", fileName]) if Verbose else subprocess.run(["unzip", fileName], stdout=subprocess.PIPE)
        print(green("Your server is now set up!"))
        print("Click enter to go to the main menu")
        input()
        

        








        


