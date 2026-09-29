import os, shutil, sys
S=sys.argv[1] + '/smali/'
INIT='Landroid/content/Intent;-><init>(Ljava/lang/String;)V'
# (file, intent reg, action reg in init, scratch reg, package, occurrence index)
P=[('com/apportable/iap/BillingService.smali','v1','v2','v2','com.android.vending'),
   ('com/apportable/iab/IabHelper.smali','v0','v1','v1','com.android.vending'),
   ('com/google/android/gms/internal/v.smali','v3','p1','v4','com.google.android.gms'),
   ('com/google/android/gms/internal/v.smali','v2','p1','v3','com.google.android.gms'),
   ('com/google/android/vending/licensing/LicenseChecker.smali','v2','v3','v3','com.android.vending'),
   ('com/android/vending/licensing/LicenseChecker.smali','v2','v3','v3','com.android.vending')]
for f,ir,ar,sr,pkg in P:
    if not os.path.exists(S+f):
        print('skip (absent)',f); continue
    t=open(S+f).read()
    old='    invoke-direct {%s, %s}, %s\n'%(ir,ar,INIT)
    if t.count(old)==0:
        print('skip (already explicit in this version)',f); continue
    assert t.count(old)==1,(f,old,t.count(old))
    new=old+'\n    const-string %s, "%s"\n\n    invoke-virtual {%s, %s}, Landroid/content/Intent;->setPackage(Ljava/lang/String;)Landroid/content/Intent;\n'%(sr,pkg,ir,sr)
    open(S+f,'w').write(t.replace(old,new)); print('patched',f,ir)

# Library loading failures used to finish() the activity silently: show the error.
f = S + 'com/apportable/activity/VerdeActivity$3$2.smali'
t = open(f).read()
old = '    invoke-virtual {v0}, Lcom/apportable/activity/VerdeActivity;->finish()V\n'
assert t.count(old) == 1
open(f, 'w').write(t.replace(old, '    invoke-static {v0, p1}, Lcom/apportable/LoadErrorDialog;->show(Landroid/app/Activity;Ljava/lang/Throwable;)V\n'))
shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'smali/com/apportable/LoadErrorDialog.smali'),
            S + 'com/apportable/LoadErrorDialog.smali')
print('patched load error dialog')

# 1.22: IabHelper.startSetup() resolves a misspelled billing action
# ("...InAppBillingService.BINN"), so createExplicitIntent() returns null and
# queryIntentServices(null) throws a NullPointerException on modern Android.
# Treat a null intent as "billing service unavailable" (the existing :cond_2 path).
f = S + 'com/apportable/iab/IabHelper.smali'
t = open(f).read()
old = ('    invoke-static {v0, v1}, Lcom/apportable/iab/IabHelper;->createExplicitIntent'
       '(Landroid/content/Context;Landroid/content/Intent;)Landroid/content/Intent;\n\n'
       '    move-result-object v0\n')
if t.count(old) == 1:
    open(f, 'w').write(t.replace(old, old + '\n    if-eqz v0, :cond_2\n'))
    print('patched IabHelper null billing intent')
else:
    print('skip IabHelper null billing intent (not in this version)')
