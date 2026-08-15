def mount_powerx_drive(mount_point="/content/drive"):
    from google.colab import drive
    drive.mount(mount_point,force_remount=False)
    return f"{mount_point}/MyDrive/PowerX/Models"
