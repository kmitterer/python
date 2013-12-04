import math
from Tkinter import *

def errorCheck(numlines, anc_pre, anc_post, result, label):
    eof_pdu = [ ['NA', 'NA', 'NA'], ['NA', 'NA', 'NA'], ['NA', 'NA', 'NA'] ]
    error = [ ['None', 'None', 'None'], ['None', 'None', 'None'], ['None', 'None', 'None'] ]
    errorBool = False
    
    tirs_lines_per_sec = 70
    
    num_subfiles = "%.3f" % ((36 + (numlines + 1)*17644 + ( (numlines + 1)/tirs_lines_per_sec + anc_pre + anc_post )*4118)/(1048555*1022))
    linecnt_1 = 0
    
    print "Number of lines =", str(numlines) 
    print "Pre-image ancillary data =", str(anc_pre), "seconds" 
    print "Post-image ancillary data =", str(anc_post), "seconds" 
    print "Number of subfiles =", str(num_subfiles) 

    num_subfiles = math.ceil(float(num_subfiles))
    
    if (num_subfiles == 1):
        for inc in [-1, 0, 1]:
            # spreadsheet shows round, SUM shows subtract 1, difference leads to issue evaluating 17677, 8, 8,202 case
            num_anc_packets = float("%.0f" % ((numlines + 1)/tirs_lines_per_sec + anc_pre + anc_post + inc))
            eof_pdu[0][inc+1] = ( 36 + (numlines + 1)*17644 + num_anc_packets*4118 ) % 1022
    else:
        # calculate the EOF PDU for the first subfile where the ancillary data length is incremented +0 and +1 packets
        linecnt_1 = math.ceil(((1071622188 - 36 - (anc_pre * 4118))/1239198) * tirs_lines_per_sec)
        for inc in [-1, 0, 1]:
            num_anc_packets_subf_0 = float("%.0f" % ((linecnt_1)/tirs_lines_per_sec + anc_pre + inc))
            eof_pdu[0][inc+1] = (36 + linecnt_1*17644 + (num_anc_packets_subf_0*4118)) % 1022
        
    if (num_subfiles == 2):
        # calculate the EOF PDU for the second where the ancillary data length is incremented +0 and +1 packets
        linecnt_2 = numlines + 1 - linecnt_1
        for inc in [-1, 0, 1]:
            num_anc_packets_subf_1 = float("%.0f" % (linecnt_2/tirs_lines_per_sec + anc_post + inc))
            eof_pdu[1][inc+1] = (36 + (linecnt_2*17644) + (num_anc_packets_subf_1*4118)) % 1022
    
    elif (num_subfiles == 3):
        # calculate the EOF PDU for the second where the ancillary data length is incremented +0 and +1 packets
        linecnt_3 = numlines + 1 - linecnt_1 - 60535
        for inc in [-1, 0, 1]:
            num_anc_packets_subf_2 = float("%.0f" % (linecnt_3/tirs_lines_per_sec + anc_post + inc))
            eof_pdu[2][inc+1] = (36 + (linecnt_3*17644) + (num_anc_packets_subf_2*4118)) % 1022
    
    
    for subfile in range(3):
        for index in range(3):
            if not (str(eof_pdu[subfile][index]) == 'NA'):
                print "Subfile", subfile, "ancillary increment", index-1, "EOF PDU =", eof_pdu[subfile][index]
                if eof_pdu[subfile][index] <= 30 or eof_pdu[subfile][index] >= 938:
                    error[subfile][index] = 'Error'
                    errorBool = True
    
    print "----------------------------------"

    if (errorBool):
        result.set("ERROR")
        label.configure(fg="white", bg="red")
    else:
        result.set("OK")
        label.configure(fg="white", bg="darkgreen")
        


def buildGUI():
    ui = Tk()
    ui.title("PIBT Error Check")

    numlines = IntVar()
    anc_pre = DoubleVar()
    anc_post = DoubleVar()
    
    result = StringVar()
    result_color = "white"
    
    frame1 = Frame(ui)
    frame1.pack(anchor = "e")

    frame2 = Frame(ui)
    frame2.pack(anchor = "e")

    frame3 = Frame(ui)
    frame3.pack(anchor = "e")
    
    frame4 = Frame(ui)
    frame4.pack(anchor = "e")

    l1 = Label(frame1, text="Image Number of Lines")
    e1 = Entry(frame1, bd=5, textvariable=numlines)

    l1.pack(side = LEFT)
    e1.pack(side = RIGHT)
    
    l2 = Label(frame2, text="Pre-Image Ancillary (secs)")
    e2 = Entry(frame2, bd=5, textvariable=anc_pre)

    l2.pack(side = LEFT)
    e2.pack(side = RIGHT)
    
    l3 = Label(frame3, text="Post-Image Ancillary (secs)")
    e3 = Entry(frame3, bd=5, textvariable=anc_post)

    l3.pack(side = LEFT)
    e3.pack(side = RIGHT)
    
    l4 = Label(frame4, bd=5, textvariable=result, width=20)
    
    b4 = Button(frame4, text="Check", command=lambda: errorCheck(numlines.get(), anc_pre.get(), anc_post.get(), result, l4), width=8)    
    
    b4.pack(side = LEFT)
    l4.pack(side = RIGHT)
    
    return ui
    

def run():
    gui = buildGUI()
    gui.mainloop()


run()

