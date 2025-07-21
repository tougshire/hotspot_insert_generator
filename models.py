from django.db import models

class DeviceModel(models.Model):
    modelname = models.CharField("model name")
    instructions = models.TextField(default="""
        <ul>
            <li>Charge the device with the included charger and cable</li>
            <li>Power on this device by pressing the button on the front panel.</li>  
            <li>Connect your device to this device using the SSID and password printed in this documentation</li>
        </ul>
        """)
    instructions_photo = models.ImageField("photo for instructions", upload_to="hotspot_insert_generator", blank=True, null=True)

    def __str__(self):
        return self.modelname
    
    