#!/usr/bin/env python

import os
import platform
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser(description="MP4/M4V track disabler.")
    parser.add_argument('-t', '--track', help='Track type to disable AAC or  AC-3.')
    parser.add_argument('-i', '--input', help='The source file or directory.')
    args = vars(parser.parse_args())

    print
    print '----------------------'
    print 'MP4/M4V track disabler'
    print '----------------------'
    print

    if not args['input']:
        print "No input file/directory specified"
        exit(0)
    if not args['track']:
        print "No track type specified"
        exit(0)

    trackType = args['track'].upper().replace('AC3', 'AC-3')

    if trackType not in ('AAC', 'AC-3'):
        print "Track type must be either AAC or AC-3"
        exit(0)

    # Look to see if the input has an extension
    # This will determine weather we have a single file or a directory

    baseName = os.path.basename(str(args['input']))
    ext = baseName.split('.')[1:]

    if not ext:
        print "Processing directory " + args['input']
        print
        processDirectory(args['input'], trackType)
        print
        print "Finished....."
        exit(0)
    else:
        ext = ext[0].lower()
        if ext not in ('mp4', 'm4v'):
            print "Input file must be .mp4 or .m4v"
            exit(0)
        else:
            processFile(args['input'], trackType)
            print
            print "Finished....."
            exit(0)


def processDirectory(inputDirectory, trackType):
    for root, directory, files in os.walk(inputDirectory):
        for filename in files:
            if filename.lower().endswith(('.mp4', '.m4v')):
                processFile(root + os.path.sep + filename, trackType)


def processFile(inputFile, trackType):
    cmd = "mp4box"
    if platform.system() == 'Darwin':
        cmd = "/Applications/Osmo4.app/Contents/MacOS/MP4Box"
    elif platform.system() != 'Windows':
        print "Unsupported OS! Exiting."
        exit(0)

    print "--------------------------------------------------------------------------------"
    print "Input file: " + inputFile + "\n"
    p = subprocess.Popen([cmd, '-info', inputFile], shell=False, stderr=subprocess.PIPE)

    o = ''
    while True:
        out = p.stderr.read(1)
        if out == '' and p.poll() is not None:
            break
        if out != '':
            o = o + out

    tracks = o.split("Track # ")
    if not tracks:
        print "No tracks found... Something went wrong."
        exit(0)

    ac3 = "None"
    aac = "None"
    for track in tracks:
        if track.find('AC-3') != -1:
            ac3 = track[0]
        if track.find('AAC') != -1:
            aac = track[0]

    if trackType == 'AC-3':
        track = ac3
    else:
        track = aac

    if track == 'None':
        print "No " + trackType + " track found, exiting."
        exit(0)

    print "Found " + trackType + " audio at track " + track

    print "Disabling track " + track
    subprocess.call([cmd, "-disable", track, inputFile], shell=False)
    print "Finished disabling track."
    print "--------------------------------------------------------------------------------"
    print


if __name__ == '__main__':
    main()
