.class public Lcom/apportable/LoadErrorDialog;
.super Ljava/lang/Object;
.source "LoadErrorDialog.java"

# Shows why native library loading failed instead of silently finishing.

.implements Landroid/content/DialogInterface$OnClickListener;

.field private final activity:Landroid/app/Activity;

.method private constructor <init>(Landroid/app/Activity;)V
    .locals 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    iput-object p1, p0, Lcom/apportable/LoadErrorDialog;->activity:Landroid/app/Activity;
    return-void
.end method

.method public onClick(Landroid/content/DialogInterface;I)V
    .locals 1
    iget-object v0, p0, Lcom/apportable/LoadErrorDialog;->activity:Landroid/app/Activity;
    invoke-virtual {v0}, Landroid/app/Activity;->finish()V
    return-void
.end method

.method public static show(Landroid/app/Activity;Ljava/lang/Throwable;)V
    .locals 4

    :try_start_0
    new-instance v0, Ljava/lang/StringBuilder;
    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V
    invoke-virtual {p1}, Ljava/lang/Throwable;->toString()Ljava/lang/String;
    move-result-object v1
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {p1}, Ljava/lang/Throwable;->getCause()Ljava/lang/Throwable;
    move-result-object v1
    if-eqz v1, :cond_0
    const-string v2, "\n\nCause: "
    invoke-virtual {v0, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {v1}, Ljava/lang/Throwable;->toString()Ljava/lang/String;
    move-result-object v1
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    :cond_0
    new-instance v1, Landroid/app/AlertDialog$Builder;
    invoke-direct {v1, p0}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;)V
    const-string v2, "Erreur de chargement"
    invoke-virtual {v1, v2}, Landroid/app/AlertDialog$Builder;->setTitle(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v2
    invoke-virtual {v1, v2}, Landroid/app/AlertDialog$Builder;->setMessage(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;
    const/4 v2, 0x0
    invoke-virtual {v1, v2}, Landroid/app/AlertDialog$Builder;->setCancelable(Z)Landroid/app/AlertDialog$Builder;
    const-string v2, "OK"
    new-instance v3, Lcom/apportable/LoadErrorDialog;
    invoke-direct {v3, p0}, Lcom/apportable/LoadErrorDialog;-><init>(Landroid/app/Activity;)V
    invoke-virtual {v1, v2, v3}, Landroid/app/AlertDialog$Builder;->setPositiveButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;
    invoke-virtual {v1}, Landroid/app/AlertDialog$Builder;->show()Landroid/app/AlertDialog;
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception v0
    invoke-virtual {p0}, Landroid/app/Activity;->finish()V
    return-void
.end method
