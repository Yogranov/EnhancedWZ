import EnhancedWZ

def airstrike_callback():
    print('This is airstrike callback')

def redalert_callback():
    print('This is red alert callback')

if __name__ == '__main__':
    enhanced_wz = EnhancedWZ.EnhancedWZ()
    enhanced_wz.Subscribe_to_precision_airstrike(airstrike_callback)
    enhanced_wz.Subscribe_to_red_alert(redalert_callback)
    enhanced_wz.Start()
