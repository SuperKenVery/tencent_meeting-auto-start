#!/usr/bin/python3
import pyautogui,cv2,os,time,sys,subprocess,multiprocessing
import numpy as np

def starttm():
    def start_block():
        subprocess.run("/opt/ukylin-wine/apps/wine-tencentmeeting/run.sh",stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    a=multiprocessing.Process(target=start_block)
    a.start()

def locate(imageName):
    screenshot_filename='screenshot.png'
    subprocess.run(["/usr/bin/gnome-screenshot","--file="+screenshot_filename],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    screenshot=cv2.imread(screenshot_filename)
    template=cv2.imread(filename(imageName))
    screenshot_gray=cv2.cvtColor(screenshot,cv2.COLOR_BGR2GRAY)
    template_gray=cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)
    match_result=cv2.matchTemplate(screenshot_gray,template_gray,cv2.TM_CCOEFF_NORMED)
    (minVal,maxVal,minLoc,maxLoc)=cv2.minMaxLoc(match_result)
    if(maxVal<=0.8):
        return False
    (left,top)=maxLoc
    center=np.array([left,top])+np.array([template.shape[1],template.shape[0]])/2
    return center

def waitAndLocate(imageName,interval=0.3):
    result=locate(imageName)
    while type(result)==bool and result==False:
        time.sleep(interval)
        result=locate(imageName)
    return result


def click(imageName,offset=np.array([0,0])):
    print("Trying to click "+imageName)
    center=waitAndLocate(imageName)
    if type(center)==bool and center==False:
        raise ValueError("Can't locate the image on screen")
    print("clicked ",imageName)
    center=center+offset
    pyautogui.click(center[0],center[1])

def filename(name):
    return os.path.join(os.path.dirname(sys.argv[0]),name)
    
def main():
    #os.system("/opt/ukylin-wine/apps/wine-tencentmeeting/run.sh >> /dev/null")
    starttm()
    locate_res=waitAndLocate('quick_meeting.png')
    time.sleep(0.5)
    locate_recover=locate('recover.png')
    if type(locate_recover)!=bool:#locate!=False
        #exist, recover
        click('recover.png')
    else:
        click('quick_meeting.png')
    waitAndLocate('share_screen.png')
    time.sleep(0.5)
    click('share_screen.png')
    click('share_sound.png')
    click('confirm_sharing.png')
    #click('caption_bar.png',np.array([66,0]))

if __name__=='__main__':
    main()
