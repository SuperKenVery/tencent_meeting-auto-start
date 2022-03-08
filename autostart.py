import pyautogui,cv2,os,time,sys
import numpy as np

def locate(imageName):
    screenshot_filename='screenshot.png'
    pyautogui.screenshot(screenshot_filename)
    screenshot=cv2.imread(screenshot_filename)
    template=cv2.imread(imageName)
    screenshot_gray=cv2.cvtColor(screenshot,cv2.COLOR_BGR2GRAY)
    template_gray=cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)
    match_result=cv2.matchTemplate(screenshot_gray,template_gray,cv2.TM_CCOEFF_NORMED)
    (minVal,maxVal,minLoc,maxLoc)=cv2.minMaxLoc(match_result)
    if(maxVal<=0.8):
        return False
    (left,top)=maxLoc
    center=np.array([left,top])+np.array([template.shape[1],template.shape[0]])/2
    return center


def click(imageName,offset=np.array([0,0])):
    imageName=filename(imageName)
    center=locate(imageName)
    if type(center)==bool and center==False:
        raise ValueError("Can't locate the image on screen")
    print("click",imageName)
    center=center+offset
    pyautogui.click(center[0],center[1])

def filename(name):
    return os.path.join(r'D:\boot\tencent_meeting',name)
    
def main():
    os.startfile(r"C:\Program Files (x86)\Tencent\WeMeet\wemeetapp.exe")
    time.sleep(10)
    locate_res=locate(filename('recover.png'))
    if type(locate_res)!=bool:#locate!=False
        #exist, recover
        click('recover.png')
    else:
        click('quick_meeting.png')
    time.sleep(6)
    click('open_camera.png')
    time.sleep(1)
    click('share_screen.png')
    time.sleep(0.5)
    click('share_sound.png')
    time.sleep(3.5)
    click('confirm_sharing.png')
    time.sleep(3)
    click('caption_bar.png',np.array([66,0]))

if __name__=='__main__':
    main()