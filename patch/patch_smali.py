import sys
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
    t=open(S+f).read()
    old='    invoke-direct {%s, %s}, %s\n'%(ir,ar,INIT)
    assert t.count(old)==1,(f,old,t.count(old))
    new=old+'\n    const-string %s, "%s"\n\n    invoke-virtual {%s, %s}, Landroid/content/Intent;->setPackage(Ljava/lang/String;)Landroid/content/Intent;\n'%(sr,pkg,ir,sr)
    open(S+f,'w').write(t.replace(old,new)); print('patched',f,ir)
