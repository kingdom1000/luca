'''
This little application is a CLI for downloading files
'''

# os is a set of module that work with the Operating system
# urllib is one of many modules that will do http stuff
import os
import urllib
import sys
import time
import argparse


# Settings for the application are just gonna go here
defaultDir = '.'                # The default directory where downloads will go
defaultMsg = 'Running ...'      # The default message for the progress bar


'''
This method will take the progress of tasks and send a progress bar to the console
Required Arguments: part (integer) - the count of the completed tasks
                    whole (integer) - the total amount of tasks
Optional Arguments: message (string) - what is currently happening
            Output: n/a
'''
def progressBar(part, whole, message=defaultMsg):
    # Clear the last printed line in the console
    clear = '\r'
    sys.stdout.write(clear)


    # Calculate the fraction of part to whole and then calculate bar length, space in bar and the percentage
    fraction = float(part) / float(whole)
    completedBarLength = int(50 * fraction)
    nonCompletedBarLength = 50 - completedBarLength
    percentage = int(fraction * 100)

    # Form the string for the output to the console, \x1b[K hex code will move the cursor to the start of line
    # eg [##########                                        ]  20%  Running number 6
    outputString = "[" + "#" * completedBarLength + " " * nonCompletedBarLength + "]  " + str(percentage) + "%  " + message
    sys.stdout.write(outputString + '\x1b[K')
    sys.stdout.flush()

    # When 100% is reached (part equals whole) then move to the next line and print completed
    if part == whole:
        sys.stdout.write("\n" + "Completed" + "\n")

'''
This first method is callled to take the urls and downloads to a directory
Required Arguments: url (string)
Optional Arguments: directory (string)
            Output: (boolean)
'''
def downloadFile(url, directory=defaultDir):
    # Create a file name by spliting the url at each '/' and then taking
    # the last item in the list.
    # eg http://example.com/file.txt -> ['http', 'example.com', 'file.txt'] to get file.txt
    filename =  url.split('/')[-1].replace('%20', ' ')

    # Check that the directory exists, if not create
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Download the file, is success return True, otherwise send False
    try:
        urllib.urlretrieve(url, directory + '/' + filename)
        return True
    except:
        return False

'''
Here a file can be passed with a list of urls, one per line. By default a
directory of the same name of the file will be used.
Required Arguments: file (string)
Optional Arguments: directory (string)
            Output: n/a
'''
def downloadFileList(file, directory=''):
    # if the directory argument is passed then move on, if not then get the
    # filename and use that instead. Get file name by split by '/' and taking
    # the last item, and then remove the extension by split by '.' and taking
    # the first item.
    if directory:
        pass
    else:
        filename = file.split('/')[-1]
        directory = filename.split('.')[0]

    # Open the file for reading and copy the file to a string, split by newline
    # to get a list of urls to download
    fileOpen = open(file, 'r')
    fileContents = fileOpen.read()
    urls = fileContents.splitlines()


    # Loop through the list of urls and call the download method on each one
    # Get the part for the progress bar by getting the index of the url in the
    # list and adding 1, i.e. first download is index 0 and last is length - 1
    for url in urls:
        downloadNumber = urls.index(url) + 1
        downloadTotal = len(urls)
        truncateUrl = url[-15:]
        progressBar(downloadNumber, downloadTotal, 'downloading ...' + truncateUrl)
        downloadFile(url, directory)
        time.sleep(0.5)


parser = argparse.ArgumentParser(description="A quick command line download tool")
# Add arguments to download
parser.add_argument('-u', '--url',       help="Download a file from a given url")
parser.add_argument('-d', '--directory', help="Location to download to")
parser.add_argument('-f', '--file',      help="Download a batch of file from a file, each url on a new line")

# Run the arguments through the parser
args = parser.parse_args()

# For a single url and directory
if args.url and args.directory:
    downloadFile(args.url, args.directory)

# For a file and directory
elif args.file and args.directory:
    downloadFileList(args.file, args.directory)

# For a single url to default directory
elif args.url and not args.directory:
    downloadFile(args.url)

# For a file to default directory
elif args.file and not args.directory:
    downloadFileList(args.file)

# For when there is no file or url provided
elif not args.file and not args.url:
    sys.stdout.write("\n" + "Error: File or URL not provided" + "\n")
